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
    PartitionConstraintError
)


class Partition(BasePartition):
    def prepare(self):
        """
        Prepares needed triggers and functions for those triggers.
        """
        indentation = {'declarations': 5, 'variables': 6}
        definitions, formatters = self._get_definitions()

        for definition in indentation:
            for index, _ in enumerate(definitions.setdefault(definition, [])):
                if index > 0:
                    definitions[definition][index] = '    ' * indentation[definition] + definitions[definition][index]

            definitions[definition] = '\n'.join(definitions[definition]).format(**formatters)

        return self.database.execute("""
            -- We need to create a before insert function
            CREATE OR REPLACE FUNCTION {{parent_table}}_insert_child()
            RETURNS TRIGGER AS $$
                DECLARE
                    match {{parent_table}}."{{column}}"%TYPE;
                    tablename VARCHAR;
                    checks TEXT;
                    {declarations}
                BEGIN
                    IF NEW.{{column}} IS NULL THEN
                        tablename := '{{parent_table}}_null';
                        checks := '{{column}} IS NULL';
                    ELSE
                        {variables}
                    END IF;

                    IF NOT EXISTS(
                        SELECT 1 FROM information_schema.tables WHERE table_name=tablename)
                    THEN
                        BEGIN
                            EXECUTE 'CREATE TABLE ' || tablename || ' (
                                CHECK (' || checks || '),
                                LIKE "{{parent_table}}" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES
                            ) INHERITS ("{{parent_table}}");';
                        EXCEPTION WHEN duplicate_table THEN
                            -- pass
                        END;
                    END IF;

                    EXECUTE 'INSERT INTO ' || tablename || ' VALUES (($1).*);' USING NEW;
                    RETURN NEW;
                END;
            $$ LANGUAGE plpgsql;

            -- Then we create a trigger which calls the before insert function
            DO $$
            BEGIN
            IF NOT EXISTS(
                SELECT 1
                FROM information_schema.triggers
                WHERE event_object_table = '{{parent_table}}'
                AND trigger_name = 'before_insert_{{parent_table}}_trigger'
            ) THEN
                CREATE TRIGGER before_insert_{{parent_table}}_trigger
                    BEFORE INSERT ON "{{parent_table}}"
                    FOR EACH ROW EXECUTE PROCEDURE {{parent_table}}_insert_child();
            END IF;
            END $$;

            -- Then we create a function to delete duplicate row from the master table after insert
            CREATE OR REPLACE FUNCTION {{parent_table}}_delete_master()
            RETURNS TRIGGER AS $$
                BEGIN
                    DELETE FROM ONLY "{{parent_table}}" WHERE {{pk}};
                    RETURN NEW;
                END;
            $$ LANGUAGE plpgsql;

            -- Lastly we create the after insert trigger that calls the after insert function
            DO $$
            BEGIN
            IF NOT EXISTS(
                SELECT 1
                FROM information_schema.triggers
                WHERE event_object_table = '{{parent_table}}'
                AND trigger_name = 'after_insert_{{parent_table}}_trigger'
            ) THEN
                CREATE TRIGGER after_insert_{{parent_table}}_trigger
                    AFTER INSERT ON "{{parent_table}}"
                    FOR EACH ROW EXECUTE PROCEDURE {{parent_table}}_delete_master();
            END IF;
            END $$;
        """.format(**definitions).format(
            pk=' AND '.join('{pk} = NEW.{pk}'.format(pk=pk) for pk in self.pks),
            parent_table=self.table,
            column=self.column_name
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

    def _get_definitions(self):
        """
        Returns needed definitions for chosen partition type/subtype.
        """
        raise NotImplementedError('Method "_get_definitions" not implemented in: {0}'.format(self.__class__.__name__))


class RangePartition(Partition):
    """
    Range partition type implementation.
    """
    def __init__(self, model, **meta):
        super(RangePartition, self).__init__(model, **meta)
        self.constraint = meta['constraint']
        self.subtype = meta['subtype']

    def _get_definitions(self):
        """
        Dynamically returns needed definitions depending on the partition subtype.
        """
        try:
            definitions = getattr(self, '_get_{0}_definitions'.format(self.subtype))()
            formatters = dict(constraint=self.constraint, subtype=self.subtype, **definitions.pop('formatters', {}))
            return definitions, formatters
        except AttributeError:
            import re
            expression = '_get_(\w+)_function'
            raise PartitionRangeSubtypeError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.subtype,
                allowed=[re.match(expression, c).group(1) for c in dir(self) if re.match(expression, c) is not None])

    def _get_date_definitions(self):
        """
        Returns definitions for date partition subtype.
        """
        patterns = {
            'day': '"y"YYYY"d"DDD',
            'week': '"y"IYYY"w"IW',
            'month': '"y"YYYY"m"MM',
            'year': '"y"YYYY',
        }

        try:
            pattern = patterns[self.constraint]
        except KeyError:
            raise PartitionConstraintError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.constraint,
                allowed=patterns.keys())

        return {
            'formatters': {'pattern': pattern},
            'variables': [
                "match := DATE_TRUNC('{constraint}', NEW.{{column}});",
                "tablename := '{{parent_table}}_' || TO_CHAR(NEW.{{column}}, '{pattern}');",
                "checks := '{{column}} >= ''' || match || ''' AND {{column}} < ''' || (match + INTERVAL '1 {constraint}') || '''';"
            ]
        }

    def _get_integer_definitions(self):
        """
        Returns definitions for integer partition subtype.
        """
        if not self.constraint.isdigit() or int(self.constraint) < 1:
            raise PartitionConstraintError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.constraint,
                allowed=['positive integer'])

        return {
            'variables': [
                "IF NEW.{{column}} = 0 THEN",
                "    tablename := '{{parent_table}}_0';",
                "    checks := '{{column}} = 0';",
                "ELSE",
                "    IF NEW.{{column}} > 0 THEN",
                "        match := ((NEW.{{column}} - 1) / {constraint}) * {constraint} + 1;",
                "        tablename := '{{parent_table}}_' || match || '_' || (match + {constraint}) - 1;",
                "    ELSE",
                "        match := FLOOR(NEW.{{column}} :: FLOAT / {constraint} :: FLOAT) * {constraint};",
                "        tablename := '{{parent_table}}_m' || ABS(match) || '_m' || ABS((match + {constraint}) - 1);",
                "    END IF;",
                "    checks := '{{column}} >= ' || match || ' AND {{column}} <= ' || (match + {constraint}) - 1;",
                "END IF;"
            ]
        }

    def _get_string_firstchars_definitions(self):
        """
        Returns definitions for string firstchars partition subtype.
        """
        if not self.constraint.isdigit() or int(self.constraint) < 1:
            raise PartitionConstraintError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.constraint,
                allowed=['positive integer'])

        return {
            'variables': [
                "match := LOWER(SUBSTR(NEW.{{column}}, 1, {constraint}));",
                "tablename := QUOTE_IDENT('{{parent_table}}_' || match);",
                "checks := 'LOWER(SUBSTR({{column}}, 1, {constraint})) = ''' || match || '''';"
            ]
        }

    def _get_string_lastchars_definitions(self):
        """
        Returns definitions for string lastchars partition subtype.
        """
        if not self.constraint.isdigit() or int(self.constraint) < 1:
            raise PartitionConstraintError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.constraint,
                allowed=['positive integer'])

        return {
            'variables': [
                "match := LOWER(SUBSTRING(NEW.{{column}} FROM '.{{{{{constraint}}}}}$'));",
                "tablename := QUOTE_IDENT('{{parent_table}}_' || match);",
                "checks := 'LOWER(SUBSTRING({{column}} FROM ''.{{{{{constraint}}}}}$'')) = ''' || match || '''';"
            ]
        }
