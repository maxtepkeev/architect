"""
PostgreSQL supports table partitioning via inheritance. The whole magic is
implemented at the database level via triggers and functions which create
and execute dynamic SQL. That means that after preparing the database for
partitioning, one can safely work with it via raw SQL statements without
using any kind of the ORM or anything else.
"""

from ..bases import BasePartition
from ...exceptions import (
    PartitionRangeSubtypeError,
    PartitionRangeError
)


class Partition(BasePartition):
    def prepare(self):
        """
        Prepares needed triggers and functions for those triggers.
        """
        return self.database.execute("""
            -- We need to create a before insert function
            CREATE OR REPLACE FUNCTION {parent_table}_insert_child()
            RETURNS TRIGGER AS $$
                {function}
            $$ LANGUAGE plpgsql;

            -- Then we create a trigger which calls the before insert function
            DO $$
            BEGIN
            IF NOT EXISTS(
                SELECT 1
                FROM information_schema.triggers
                WHERE event_object_table = '{parent_table}'
                AND trigger_name = 'before_insert_{parent_table}_trigger'
            ) THEN
                CREATE TRIGGER before_insert_{parent_table}_trigger
                    BEFORE INSERT ON "{parent_table}"
                    FOR EACH ROW EXECUTE PROCEDURE {parent_table}_insert_child();
            END IF;
            END $$;

            -- Then we create a function to delete duplicate row from the master table after insert
            CREATE OR REPLACE FUNCTION {parent_table}_delete_master()
            RETURNS TRIGGER AS $$
                BEGIN
                    DELETE FROM ONLY "{parent_table}" WHERE {pk};
                    RETURN NEW;
                END;
            $$ LANGUAGE plpgsql;

            -- Lastly we create the after insert trigger that calls the after insert function
            DO $$
            BEGIN
            IF NOT EXISTS(
                SELECT 1
                FROM information_schema.triggers
                WHERE event_object_table = '{parent_table}'
                AND trigger_name = 'after_insert_{parent_table}_trigger'
            ) THEN
                CREATE TRIGGER after_insert_{parent_table}_trigger
                    AFTER INSERT ON "{parent_table}"
                    FOR EACH ROW EXECUTE PROCEDURE {parent_table}_delete_master();
            END IF;
            END $$;
        """.format(
            pk=' AND '.join('{pk} = NEW.{pk}'.format(pk=pk) for pk in self.pks),
            parent_table=self.table,
            function=self._get_function()
        ))

    def exists(self):
        """
        Checks if partition exists. Not used in this backend because everything is done at the database level.
        """
        return False

    def create(self):
        """
        Creates new partition. Not used in this backend because everything is done at the database level.
        """
        pass


class RangePartition(Partition):
    """
    Range partition type implementation.
    """
    def __init__(self, model, **meta):
        super(RangePartition, self).__init__(model, **meta)
        self.range = meta['range']
        self.subtype = meta['subtype']

    def _get_function(self):
        """
        Dynamically loads needed before insert function body depending on the partition subtype.
        """
        try:
            return getattr(self, '_get_{0}_function'.format(self.subtype))()
        except AttributeError:
            import re
            expression = '_get_(\w+)_function'
            raise PartitionRangeSubtypeError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.subtype,
                allowed=[re.match(expression, c).group(1) for c in dir(self) if re.match(expression, c) is not None])

    def _get_date_function(self):
        """
        Contains a before insert function body for date partition subtype.
        """
        patterns = {
            'day': '"y"YYYY"d"DDD',
            'week': '"y"IYYY"w"IW',
            'month': '"y"YYYY"m"MM',
            'year': '"y"YYYY',
        }

        try:
            pattern = patterns[self.range]
        except KeyError:
            raise PartitionRangeError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.range,
                allowed=patterns.keys())

        return """
            DECLARE tablename TEXT;
            DECLARE columntype TEXT;
            DECLARE startdate TIMESTAMP;
            BEGIN
                startdate := date_trunc('{range}', NEW.{column});
                tablename := '{parent_table}_' || to_char(NEW.{column}, '{pattern}');

                IF NOT EXISTS(
                    SELECT 1 FROM information_schema.tables WHERE table_name=tablename)
                THEN
                    BEGIN
                        SELECT data_type INTO columntype
                        FROM information_schema.columns
                        WHERE table_name = '{parent_table}' AND column_name = '{column}';

                        EXECUTE 'CREATE TABLE ' || tablename || ' (
                            CHECK (
                                {column} >= ''' || startdate || '''::' || columntype || ' AND
                                {column} < ''' || (startdate + '1 {range}'::interval) || '''::' || columntype || '
                            ),
                            LIKE "{parent_table}" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES
                        ) INHERITS ("{parent_table}");';
                    EXCEPTION WHEN duplicate_table THEN
                        -- pass
                    END;
                END IF;

                EXECUTE 'INSERT INTO ' || tablename || ' VALUES (($1).*);' USING NEW;
                RETURN NEW;
            END;
        """.format(parent_table=self.table, range=self.range, column=self.column_name, pattern=pattern)
