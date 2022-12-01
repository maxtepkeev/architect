"""
Tests database specific behaviour which is independent from ORM being used.
"""
from . import unittest, mock

from architect.databases.postgresql.partition import RangePartition


class SingleColumnPartitionTestCase(object):
    def setUp(self):
        model = mock.Mock(__name__='Foo')
        defaults = {
            'table': 'shipping_volume_predictedvolume',
            'column_values': [1],
            'columns': ['source_file_id'],
            'pk': 'id'
        }
        self.range_partition = RangePartition(model, **dict(constraints=['1'], subtypes=['integer'], **defaults))


class PostgresqlPartitionSingleColumnTestCase(SingleColumnPartitionTestCase, unittest.TestCase):
    def test__get_command_str_single_column(self):
        command_str = self.range_partition._get_command_str()
        target_command_str = """
            -- We need to create a before insert function
            CREATE OR REPLACE FUNCTION shipping_volume_predictedvolume_insert_child()
            RETURNS TRIGGER AS $$
                DECLARE
                    match_0 shipping_volume_predictedvolume."source_file_id"%TYPE;
                    tablename_0 VARCHAR;
                    checks_0 TEXT;
                    tablename VARCHAR;
                    checks TEXT;

                BEGIN
                    IF NEW."source_file_id" IS NULL THEN
                        tablename_0 := '__null';
                        checks_0 := '"source_file_id" IS NULL';
                    ELSE
                        IF NEW."source_file_id" = 0 THEN
                            tablename_0 := '__0';
                            checks_0 := '"source_file_id" = 0';
                        ELSE
                            IF NEW."source_file_id" > 0 THEN
                                match_0 := ((NEW."source_file_id" - 1) / 1) * 1 + 1;
                                tablename_0 := '__' || match_0 || '_' || (match_0 + 1) - 1;
                            ELSE
                                match_0 := FLOOR(NEW."source_file_id" :: FLOAT / 1 :: FLOAT) * 1;
                                tablename_0 := '__m' || ABS(match_0) || '_m' || ABS((match_0 + 1) - 1);
                            END IF;
                            checks_0 := '"source_file_id" >= ' || match_0 || ' AND "source_file_id" <= ' || (match_0 + 1) - 1;
                        END IF;
                    END IF;
                    tablename := 'shipping_volume_predictedvolume' || tablename_0;
                    checks := checks_0;

                    BEGIN
                        EXECUTE 'CREATE TABLE IF NOT EXISTS ' || tablename || ' (
                            CHECK (' || checks || '),
                            LIKE "shipping_volume_predictedvolume" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES
                        ) INHERITS ("shipping_volume_predictedvolume");';
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
                WHERE event_object_table = 'shipping_volume_predictedvolume'
                AND trigger_name = LOWER('before_insert_shipping_volume_predictedvolume_trigger')
            ) THEN
                CREATE TRIGGER before_insert_shipping_volume_predictedvolume_trigger
                    BEFORE INSERT ON "shipping_volume_predictedvolume"
                    FOR EACH ROW EXECUTE PROCEDURE shipping_volume_predictedvolume_insert_child();
            END IF;
            END $$;

            -- Then we create a function to delete duplicate row from the master table after insert
            CREATE OR REPLACE FUNCTION shipping_volume_predictedvolume_delete_master()
            RETURNS TRIGGER AS $$
                BEGIN
                    DELETE FROM ONLY "shipping_volume_predictedvolume" WHERE id = NEW.id;
                    RETURN NEW;
                END;
            $$ LANGUAGE plpgsql;

            -- Lastly we create the after insert trigger that calls the after insert function
            DO $$
            BEGIN
            IF NOT EXISTS(
                SELECT 1
                FROM information_schema.triggers
                WHERE event_object_table = 'shipping_volume_predictedvolume'
                AND trigger_name = LOWER('after_insert_shipping_volume_predictedvolume_trigger')
            ) THEN
                CREATE TRIGGER after_insert_shipping_volume_predictedvolume_trigger
                    AFTER INSERT ON "shipping_volume_predictedvolume"
                    FOR EACH ROW EXECUTE PROCEDURE shipping_volume_predictedvolume_delete_master();
            END IF;
            END $$;
        """

        assert command_str == target_command_str


class DoubleColumnPartitionTestCase(object):
    def setUp(self):
        model = mock.Mock(__name__='Foo')
        defaults = {
            'table': 'shipping_volume_predictedvolume',
            'column_values': [None, None],
            'columns': ['source_file_id', 'date'],
            'pk': 'id'
        }
        self.range_partition = RangePartition(model, **dict(constraints=['1', 'month'], subtypes=['integer', 'date'], **defaults))


class PostgresqlPartitionDoubleColumnTestCase(DoubleColumnPartitionTestCase, unittest.TestCase):
    def test__get_command_str_single_column(self):
        command_str = self.range_partition._get_command_str()
        target_command_str = """
            -- We need to create a before insert function
            CREATE OR REPLACE FUNCTION shipping_volume_predictedvolume_insert_child()
            RETURNS TRIGGER AS $$
                DECLARE
                    match_0 shipping_volume_predictedvolume."source_file_id"%TYPE;
                    tablename_0 VARCHAR;
                    checks_0 TEXT;
                    match_1 shipping_volume_predictedvolume."date"%TYPE;
                    tablename_1 VARCHAR;
                    checks_1 TEXT;
                    tablename VARCHAR;
                    checks TEXT;

                BEGIN
                    IF NEW."source_file_id" IS NULL THEN
                        tablename_0 := '__null';
                        checks_0 := '"source_file_id" IS NULL';
                    ELSE
                        IF NEW."source_file_id" = 0 THEN
                            tablename_0 := '__0';
                            checks_0 := '"source_file_id" = 0';
                        ELSE
                            IF NEW."source_file_id" > 0 THEN
                                match_0 := ((NEW."source_file_id" - 1) / 1) * 1 + 1;
                                tablename_0 := '__' || match_0 || '_' || (match_0 + 1) - 1;
                            ELSE
                                match_0 := FLOOR(NEW."source_file_id" :: FLOAT / 1 :: FLOAT) * 1;
                                tablename_0 := '__m' || ABS(match_0) || '_m' || ABS((match_0 + 1) - 1);
                            END IF;
                            checks_0 := '"source_file_id" >= ' || match_0 || ' AND "source_file_id" <= ' || (match_0 + 1) - 1;
                        END IF;
                    END IF;
                    match_1 := DATE_TRUNC('month', NEW."date");
                    tablename_1 := '__' || TO_CHAR(NEW."date", '"y"YYYY"m"MM');
                    checks_1 := '"date" >= ''' || match_1 || ''' AND "date" < ''' || (match_1 + INTERVAL '1 month') || '''';
                    tablename := 'shipping_volume_predictedvolume' || tablename_0 || tablename_1;
                    checks := checks_0 || ' AND ' || checks_1;

                    BEGIN
                        EXECUTE 'CREATE TABLE IF NOT EXISTS ' || tablename || ' (
                            CHECK (' || checks || '),
                            LIKE "shipping_volume_predictedvolume" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES
                        ) INHERITS ("shipping_volume_predictedvolume");';
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
                WHERE event_object_table = 'shipping_volume_predictedvolume'
                AND trigger_name = LOWER('before_insert_shipping_volume_predictedvolume_trigger')
            ) THEN
                CREATE TRIGGER before_insert_shipping_volume_predictedvolume_trigger
                    BEFORE INSERT ON "shipping_volume_predictedvolume"
                    FOR EACH ROW EXECUTE PROCEDURE shipping_volume_predictedvolume_insert_child();
            END IF;
            END $$;

            -- Then we create a function to delete duplicate row from the master table after insert
            CREATE OR REPLACE FUNCTION shipping_volume_predictedvolume_delete_master()
            RETURNS TRIGGER AS $$
                BEGIN
                    DELETE FROM ONLY "shipping_volume_predictedvolume" WHERE id = NEW.id;
                    RETURN NEW;
                END;
            $$ LANGUAGE plpgsql;

            -- Lastly we create the after insert trigger that calls the after insert function
            DO $$
            BEGIN
            IF NOT EXISTS(
                SELECT 1
                FROM information_schema.triggers
                WHERE event_object_table = 'shipping_volume_predictedvolume'
                AND trigger_name = LOWER('after_insert_shipping_volume_predictedvolume_trigger')
            ) THEN
                CREATE TRIGGER after_insert_shipping_volume_predictedvolume_trigger
                    AFTER INSERT ON "shipping_volume_predictedvolume"
                    FOR EACH ROW EXECUTE PROCEDURE shipping_volume_predictedvolume_delete_master();
            END IF;
            END $$;
        """
        assert command_str == target_command_str
