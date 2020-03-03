# Database

## Database of OKTAV webgui

For the OKTAV Django application the default sqlite3 database is used. At the moment there is
no need for a more robust database like PostgreSQL or MySQL because from the user side it's not
planned to write anything to the database.

## sqlite3 commands
Here is a very basic list of the most useful commands for sqlite3

    'python manage.py dbshell' # Enter sqlite db shell, you must be in the directory where manage.py is

Inside the db shell:

    '.tables' # Get a list of tables
    '.schema {table_name}' # Get scheme of a table
    'CREATE TABLE IF NOT EXISTS "table_name" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "field1" varchar(10) NOT NULL, "field2" varchar(20) NOT NULL);' # Insert new table

    'DELETE FROM "table_name";' # reset table id counter, step 1
    'DELETE FROM sqlite_sequence WHERE name = "table_name";' # reset table id counter, step 2
    
    '.quit' # Quit db shell
