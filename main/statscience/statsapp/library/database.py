import secrets

from .jsonfile import jmod, jsontemplates
import psycopg2.extensions
from docker import errors
import psycopg2
import logging
import inspect
import dotenv
import docker
import time
import os

dotenv.load_dotenv('.env')

class db:
    @staticmethod
    def setup_db():
        container_name="StatFlux-Postgres"
        image="postgres:15"
        user='postgres'
        password=str(secrets.token_hex(16))
        db_name="StatFlux"
        listening_port=6543

        client = docker.from_env()

        print(f"Installing PostgreSQL container '{container_name}'...")

        # Clean up the old container if it exists
        try:
            old_container = client.containers.get(container_name)
            old_container.stop()
            old_container.remove()
            print("Old container removed.")
        except docker.errors.NotFound:
            pass

        container = client.containers.run(
            image=image,
            name=container_name,
            environment={
                "POSTGRES_USER": user,
                "POSTGRES_PASSWORD": password,
                "POSTGRES_DB": db_name
            },
            ports={"5432/tcp": str(listening_port)},
            detach=True
        )

        # Wait for PostgreSQL to become ready
        print("Waiting for PostgreSQL to become ready...", end="", flush=True)
        for _ in range(30):
            try:
                conn = psycopg2.connect(
                    dbname=db_name,
                    user=user,
                    password=password,
                    host="localhost",
                    port=listening_port
                )
                conn.close()
                print(" ready!")
                break
            except psycopg2.OperationalError:
                time.sleep(1)
                print(".", end="", flush=True)
        else:
            print("\nFailed to connect to PostgreSQL.")
            container.stop()
            container.remove()
            raise RuntimeError("PostgreSQL did not become ready in time.")

        db.save_details(
            DB_HOST="localhost",
            DB_PORT=listening_port,
            DB_USERNAME=user,
            DB_PASSWORD=password,
            DB_DATABASE=db_name,
        )
        print(f"PostgreSQL container '{container_name}' is up and ready.")
        return container

    @staticmethod
    def db_accessible():
        jfile = jmod('settings.json', jsontemplates.SETTINGS)
        DB_HOST = jfile.get_value('database.host')
        DB_PORT = jfile.get_value('database.port')
        DB_USERNAME = jfile.get_value('database.user')
        DB_PASSWORD = jfile.get_value('database.password')
        DB_DATABASE = jfile.get_value('database.database')

        try:
            conn = psycopg2.connect(
                user=DB_USERNAME,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                database=DB_DATABASE,
            )
            conn.close()
            return True
        except psycopg2.OperationalError:
            return False

    @staticmethod
    def save_details(
            DB_HOST,
            DB_PORT,
            DB_USERNAME,
            DB_PASSWORD,
            DB_DATABASE,
    ):
        jfile = jmod('settings.json', jsontemplates.SETTINGS)
        jfile.set_value('database.host', DB_HOST)
        jfile.set_value('database.port', DB_PORT)
        jfile.set_value('database.user', DB_USERNAME)
        jfile.set_value('database.password', DB_PASSWORD)
        jfile.set_value('database.database', DB_DATABASE)
        return True

    @staticmethod
    def connect() -> psycopg2.extensions.connection:
        jfile = jmod('settings.json', jsontemplates.SETTINGS)
        DB_HOST = jfile.get_value('database.host')
        DB_PORT = jfile.get_value('database.port')
        DB_USERNAME = jfile.get_value('database.user')
        DB_PASSWORD = jfile.get_value('database.password')
        DB_DATABASE = jfile.get_value('database.database')

        if str(DB_PORT).isdigit() is False:
            raise ValueError(f"DB Port is Not a Number. Got {DB_PORT} (type: {type(DB_PORT)}")
        else:
            DB_PORT = int(DB_PORT)

        if DB_PASSWORD is None:
            raise KeyError("The DATABASE_PASSWORD key in environment variables or .env file is empty or non-existent. Cannot proceed")
        if DB_HOST is None:
            raise KeyError("The DATABASE_HOST key in environemnt variables or .env file is empty or non-existent. Cannot proceed. Need host without port")
        if DB_USERNAME == 'postgres':
            if bool(os.environ.get('SUPPRESS_POSTGRE_WARN', False)) is False:
                if DB_HOST != 'localhost':  # Don't send the warning if its securely on localhost.
                    warn_msg = ("Warning: You are using username 'postgres' for logging in to the database.\n"
                                "This is discouraged behavior as it is not good security practice.\n"
                                "Please only create an account with the appropriate permissions and use that account for logging in "
                                "IF this is not for debugging or otherwise on a secured, closed network.\n"
                                "Add the key `SUPPRESS_POSTGRE_WARN=True` to suppress further warnings.")

                    print(warn_msg)
                    logging.warning(warn_msg)

        conn = psycopg2.connect(
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE,
        )
        return conn

    @staticmethod
    def modernize():
        """
        Modernizes the PostgreSQL database schema to match the current table definition.
        """
        table_dict = {
            'statistics_table': {
                'name': 'TEXT PRIMARY KEY NOT NULL',
                'description': 'TEXT DEFAULT NULL',
                "type": "TEXT NOT NULL DEFAULT \'numeric\' CHECK (type IN ('daily', 'weekly', 'accumulative', 'delta'))",
            },
            'statistics_data': {
                'name': 'TEXT REFERENCES statistics_table(name)',
                'value': 'INTEGER NOT NULL',
                'date': 'DATE NOT NULL DEFAULT CURRENT_DATE',
            }
        }

        try:
            conn = db.connect()
            conn.autocommit = True
            cur = conn.cursor()

            for table_name, columns in table_dict.items():
                # Check if the table exists
                cur.execute("""
                            SELECT EXISTS (
                                SELECT FROM information_schema.tables
                                WHERE table_name = %s
                            );
                            """, (table_name,))
                table_exists = cur.fetchone()[0]

                if table_exists:
                    # Get existing columns
                    cur.execute("""
                                SELECT column_name
                                FROM information_schema.columns
                                WHERE table_name = %s;
                                """, (table_name,))
                    existing_columns = {row[0] for row in cur.fetchall()}

                    for column_name, column_type in columns.items():
                        if column_name not in existing_columns:
                            try:
                                cur.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};')
                            except Exception as e:
                                logging.error(f"Error adding column {column_name} to {table_name}: {e}")
                else:
                    # Create table
                    columns_str = ', '.join(f'{col} {dtype}' for col, dtype in columns.items())
                    try:
                        cur.execute(f'CREATE TABLE {table_name} ({columns_str});')
                    except Exception as err:
                        logging.error(f"Error creating table {table_name} with columns {columns_str}: {err}")
                        exit(1)

            cur.close()
            conn.close()
        except psycopg2.Error as e:
            logging.error(f"Database connection failed: {e}")
            exit(1)

if not db.db_accessible():
    db.setup_db()
db.modernize()

class db:
    @staticmethod
    def create_new_statistic(statistic_name: str, statistic_description: str, statistic_type: str):
        conn = db.connect()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO statistics_table (name, description, type)
                VALUES (%s, %s, %s)
                """,
                (statistic_name, statistic_description, statistic_type),
            )
            conn.commit()
            cur.close()
            return True
        except (psycopg2.OperationalError, psycopg2.ProgrammingError) as err:
            logging.error(f"Error on line {inspect.currentframe().f_lineno}! Error: {err}", err)
            conn.rollback()
            conn.close()
            return False