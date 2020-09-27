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
        command_str = self._get_command_str()
        return self.database.execute(command_str)

    def _get_command_str(self):
        indentation = {'declarations': 5, 'variables': 5}
        definitions, formatters = self._get_definitions()

        for definition in indentation:
            for index, _ in enumerate(definitions.setdefault(definition, [])):
                if index > 0:
                    definitions[definition][index] = '    ' * indentation[definition] + definitions[definition][index]

            definitions[definition] = '\n'.join(definitions[definition]).format(**formatters)

        return """
            -- We need to create a before insert function
            CREATE OR REPLACE FUNCTION {{parent_table}}_insert_child()
            RETURNS TRIGGER AS $$
                DECLARE
                    {declarations}
                    tablename VARCHAR;
                    checks TEXT;

                BEGIN
                    {variables}

                    BEGIN
                        EXECUTE 'CREATE TABLE IF NOT EXISTS ' || tablename || ' (
                            CHECK (' || checks || '),
                            LIKE "{{parent_table}}" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES
                        ) INHERITS ("{{parent_table}}");';
                    EXCEPTION WHEN duplicate_table THEN
                        -- pass
                    END;

                    EXECUTE 'INSERT INTO ' || tablename || ' VALUES (($1).*);' USING NEW;
                    RETURN NEW;
                END;
            $$ LANGUAGE plpgsql SECURITY DEFINER;

            -- Then we create a trigger which calls the before insert function
            DO $$
            BEGIN
            IF NOT EXISTS(
                SELECT 1
                FROM information_schema.triggers
                WHERE event_object_table = '{{parent_table}}'
                AND trigger_name = LOWER('before_insert_{{parent_table}}_trigger')
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
                AND trigger_name = LOWER('after_insert_{{parent_table}}_trigger')
            ) THEN
                CREATE TRIGGER after_insert_{{parent_table}}_trigger
                    AFTER INSERT ON "{{parent_table}}"
                    FOR EACH ROW EXECUTE PROCEDURE {{parent_table}}_delete_master();
            END IF;
            END $$;
        """.format(**definitions).format(
            pk=' AND '.join('{pk} = NEW.{pk}'.format(pk=pk) for pk in self.pks),
            parent_table=self.table,
            **{
                'column_{idx}'.format(idx=idx): '"{0}"'.format(column) for idx, column in enumerate(
                    self.columns
                )
            }
        )

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
        self.constraints = meta['constraints']
        self.subtypes = meta['subtypes']

    def _get_definitions(self):
        """
        Dynamically returns needed definitions depending on the partition subtype.
        """
        definitions = dict()
        for idx, subtype in enumerate(self.subtypes):
            try:
                if definitions:
                    definitions_temp = getattr(self, '_get_{0}_definitions'.format(subtype))(idx)
                    definitions['formatters'] = {**definitions['formatters'], **definitions_temp['formatters']}
                    definitions['declarations'] += definitions_temp['declarations']
                    definitions['variables'] += definitions_temp['variables']
                else:
                    definitions = getattr(self, '_get_{0}_definitions'.format(subtype))(idx)
            except AttributeError:
                import re
                expression = '_get_(\w+)_function'
                raise PartitionRangeSubtypeError(
                    model=self.model.__name__,
                    dialect=self.dialect,
                    current=subtype,
                    allowed=[re.match(expression, c).group(1) for c in dir(self) if
                             re.match(expression, c) is not None])

        formatters = dict(**definitions.pop('formatters', {}))
        tablename = "tablename := '{{parent_table}}'"
        checks = "checks := "
        for idx in range(len(self.constraints)):
            tablename += ' || tablename_{idx}'.format(idx=idx)
            formatters["constraint_{}".format(idx)] = self.constraints[idx]
            formatters["subtype_{}".format(idx)] = self.subtypes[idx]
        checks += " || ' AND ' || ".join(['checks_{idx}'.format(idx=idx) for idx in range(len(self.constraints))])
        definitions['variables'].append(tablename+';')
        definitions['variables'].append(checks+';')
        return definitions, formatters

    def _get_date_definitions(self, idx):
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
            pattern = patterns[self.constraints[idx]]
        except KeyError:
            raise PartitionConstraintError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.constraints[idx],
                allowed=patterns.keys())

        return {
            'formatters': {'pattern': pattern},
            'declarations': [
                'match_{idx} {{{{parent_table}}}}.{{{{column_{idx}}}}}%TYPE;'.format(idx=idx),
                'tablename_{idx} VARCHAR;'.format(idx=idx),
                'checks_{idx} TEXT;'.format(idx=idx),
            ],
            'variables': [
                "match_{idx} := DATE_TRUNC('{{constraint_{idx}}}', NEW.{{{{column_{idx}}}}});".format(idx=idx),
                "tablename_{idx} := '__' || TO_CHAR(NEW.{{{{column_{idx}}}}}, '{{pattern}}');".format(idx=idx),
                "checks_{idx} := '{{{{column_{idx}}}}} >= ''' || match_{idx} || ''' AND {{{{column_{idx}}}}} < ''' "
                "|| (match_{idx} + INTERVAL '1 {{constraint_{idx}}}') || '''';".format(idx=idx)
            ]
        }

    def _get_integer_definitions(self, idx):
        """
        Returns definitions for integer partition subtype.
        """
        if not self.constraints[idx].isdigit() or int(self.constraints[idx]) < 1:
            raise PartitionConstraintError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.constraints[idx],
                allowed=['positive integer'])

        return {
            'formatters': {'idx': idx},
            'declarations': [
                'match_{idx} {{{{parent_table}}}}.{{{{column_{idx}}}}}%TYPE;'.format(idx=idx),
                'tablename_{idx} VARCHAR;'.format(idx=idx),
                'checks_{idx} TEXT;'.format(idx=idx),
            ],
            'variables': [
                "IF NEW.{{{{column_{idx}}}}} IS NULL THEN".format(idx=idx),
                "    tablename_{idx} := '__null';".format(idx=idx),
                "    checks_{idx} := '{{{{column_{idx}}}}} IS NULL';".format(idx=idx),
                "ELSE",
                "    IF NEW.{{{{column_{idx}}}}} = 0 THEN".format(idx=idx),
                "        tablename_{idx} := '__0';".format(idx=idx),
                "        checks_{idx} := '{{{{column_{idx}}}}} = 0';".format(idx=idx),
                "    ELSE",
                "        IF NEW.{{{{column_{idx}}}}} > 0 THEN".format(idx=idx),
                "            match_{idx} := ((NEW.{{{{column_{idx}}}}} - 1) / "
                "{{constraint_{idx}}}) * {{constraint_{idx}}} + 1;".format(idx=idx),
                "            tablename_{idx} := '__' || match_{idx} || '_' || "
                "(match_{idx} + {{constraint_{idx}}}) - 1;".format(idx=idx),
                "        ELSE",
                "            match_{idx} := FLOOR(NEW.{{{{column_{idx}}}}} :: FLOAT / "
                "{{constraint_{idx}}} :: FLOAT) * {{constraint_{idx}}};".format(idx=idx),
                "            tablename_{idx} := '__m' || ABS(match_{idx}) || '_m' || "
                "ABS((match_{idx} + {{constraint_{idx}}}) - 1);".format(idx=idx),
                "        END IF;",
                "        checks_{idx} := '{{{{column_{idx}}}}} >= ' || match_{idx} || "
                "' AND {{{{column_{idx}}}}} <= ' || (match_{idx} + {{constraint_{idx}}}) - 1;".format(idx=idx),
                "    END IF;",
                "END IF;",

            ]
        }

    def _get_string_firstchars_definitions(self, idx):
        """
        Returns definitions for string firstchars partition subtype.
        """
        if not self.constraints[idx].isdigit() or int(self.constraints[idx]) < 1:
            raise PartitionConstraintError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.constraints[idx],
                allowed=['positive integer'])

        return {
            'formatters': {},
            'declarations': [
                'match_{idx} {{{{parent_table}}}}.{{{{column_{idx}}}}}%TYPE;'.format(idx=idx),
                'tablename_{idx} VARCHAR;'.format(idx=idx),
                'checks_{idx} TEXT;'.format(idx=idx),
            ],
            'variables': [
                "match_{idx} := LOWER(SUBSTR(NEW.{{{{column_{idx}}}}}, 1, {{constraint_{idx}}}));".format(idx=idx),
                "tablename_{idx} := QUOTE_IDENT('__' || match_{idx});".format(idx=idx),
                "checks_{idx} := 'LOWER(SUBSTR({{{{column_{idx}}}}}, 1, "
                "{{constraint_{idx}}})) = ''' || match_{idx} || '''';".format(idx=idx)
            ]
        }

    def _get_string_lastchars_definitions(self, idx):
        """
        Returns definitions for string lastchars partition subtype.
        """
        if not self.constraints[idx].isdigit() or int(self.constraints[idx]) < 1:
            raise PartitionConstraintError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.constraints[idx],
                allowed=['positive integer'])

        return {
            'formatters': {},
            'declarations': [
                'match_{idx} {{{{parent_table}}}}.{{{{column_{idx}}}}}%TYPE;'.format(idx=idx),
                'tablename_{idx} VARCHAR;'.format(idx=idx),
                'checks_{idx} TEXT;'.format(idx=idx),
            ],
            'variables': [
                "match_{idx} := LOWER(SUBSTRING(NEW.{{{{column_{idx}}}}} "
                "FROM '.{{{{{{{{{{constraint_{idx}}}}}}}}}}}$'));".format(idx=idx),
                "tablename_{idx} := QUOTE_IDENT('__' || match_{idx});".format(idx=idx),
                "checks_{idx} := 'LOWER(SUBSTRING({{{{column_{idx}}}}} FROM "
                "''.{{{{{{{{{{constraint_{idx}}}}}}}}}}}$'')) = ''' || match_{idx} || '''';".format(idx=idx)
            ]
        }
