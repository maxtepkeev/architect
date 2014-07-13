"""
PostgreSQL supports table partitioning via inheritance. The whole magic is
implemented at the database level via triggers and functions which create
and execute dynamic SQL. That means that after preparing the database for
partitioning, one can safely work with it via raw SQL statements without
using any kind of the ORM or anything else.
"""

from architect.databases import BasePartition
from architect.exceptions import (
    PartitionRangeError,
    PartitionRangeSubtypeError
)


class Partition(BasePartition):
    """Common methods for all partition types"""
    def prepare(self):
        """Prepares needed triggers and functions for those triggers"""
        return self.execute("""
            -- We need to create a before insert function
            CREATE OR REPLACE FUNCTION {parent_table}_insert_child()
            RETURNS TRIGGER AS $$
                {partition_function}
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
            partition_function=self._get_partition_function()
        ))

    def exists(self):
        """Checks if partition exists. Not used in this backend because everything is done at the database level"""
        return True

    def create(self):
        """Creates new partition. Not used in this backend because everything is done at the database level"""
        pass


class RangePartition(Partition):
    """Range partition type implementation"""
    def __init__(self, **kwargs):
        super(RangePartition, self).__init__(**kwargs)
        self.partition_range = kwargs['partition_range']
        self.partition_subtype = kwargs['partition_subtype']

    def _get_partition_function(self):
        """Dynamically loads needed before insert function body depending on the partition subtype"""
        try:
            return getattr(self, '_get_{0}_partition_function'.format(self.partition_subtype))()
        except AttributeError:
            import re
            raise PartitionRangeSubtypeError(
                model=self.model,
                database=self.__module__.split('.')[-2],
                current=self.partition_subtype,
                allowed=[re.match('_get_(\w+)_partition_function', c).group(1) for c in dir(
                    self) if re.match('_get_\w+_partition_function', c) is not None]
            )

    def _get_date_partition_function(self):
        """Contains a before insert function body for date partition subtype"""
        patterns = {
            'day': '"y"YYYY"d"DDD',
            'week': '"y"IYYY"w"IW',
            'month': '"y"YYYY"m"MM',
            'year': '"y"YYYY',
        }

        try:
            partition_pattern = patterns[self.partition_range]
        except KeyError:
            raise PartitionRangeError(
                model=self.model,
                database=self.__module__.split('.')[-2],
                current=self.partition_range,
                allowed=patterns.keys()
            )

        return """
            DECLARE tablename TEXT;
            DECLARE columntype TEXT;
            DECLARE startdate TIMESTAMP;
            BEGIN
                startdate := date_trunc('{partition_range}', NEW.{partition_column});
                tablename := '{parent_table}_' || to_char(NEW.{partition_column}, '{partition_pattern}');

                IF NOT EXISTS(
                    SELECT 1 FROM information_schema.tables WHERE table_name=tablename)
                THEN
                    SELECT data_type INTO columntype
                    FROM information_schema.columns
                    WHERE table_name = '{parent_table}' AND column_name = '{partition_column}';

                    EXECUTE 'CREATE TABLE ' || tablename || ' (
                        CHECK (
                            {partition_column} >= ''' || startdate || '''::' || columntype || ' AND
                            {partition_column} < ''' || (startdate + '1 {partition_range}'::interval) || '''::' || columntype || '
                        ),
                        LIKE "{parent_table}" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES
                    ) INHERITS ("{parent_table}");';
                END IF;

                EXECUTE 'INSERT INTO ' || tablename || ' VALUES (($1).*);' USING NEW;
                RETURN NEW;
            END;
        """.format(
            parent_table=self.table,
            partition_range=self.partition_range,
            partition_column=self.column_name,
            partition_pattern=partition_pattern,
        )
