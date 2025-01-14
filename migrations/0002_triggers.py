from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circuit', '0001_initial'),
    ]

    operations = [
        # ############################################################################## #
        #               Calculate the reference_number for a Circuit                     #
        # ############################################################################## #
        migrations.RunSQL("""
            CREATE OR REPLACE FUNCTION insert_circuit_reference_number()
                RETURNS TRIGGER AS
            $BODY$
            DECLARE
                new_reference_number integer;
            BEGIN
                SELECT COALESCE(MAX(reference_number), 0) + 1 INTO new_reference_number
                FROM circuit
                WHERE deleted IS NULL AND address_id = NEW.address_id;
                NEW.reference_number := new_reference_number;
                IF NEW.reference_number IS NULL THEN
                    NEW.reference_number := 1;
                END IF;
                RETURN NEW;
            END;
            $BODY$

            LANGUAGE plpgsql VOLATILE
            COST 100;
        """),

        # ############################################################################## #
        #                                    Triggers                                    #
        # ############################################################################## #
        migrations.RunSQL("""
            CREATE TRIGGER insert_circuit_reference_number
                BEFORE INSERT ON circuit
                FOR EACH ROW EXECUTE PROCEDURE insert_circuit_reference_number();
        """),
    ]
