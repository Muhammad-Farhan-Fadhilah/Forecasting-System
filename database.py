import psycopg2

# Connect to the database
with open("anomalies.sql", "r") as file:
    sql_script = file.read()

database = 'flying_farmer'
user = 'azmihasan'
password = 'mypassword'

try:
    # make sure to check out that the default port 5432 available.
    # If it is in use, basically brew package manager operate automatically the server.
    # To stop it just put this command in the terminal "brew services stop postgresql"
    conn = psycopg2.connect(
        host="localhost",
        user=user,
        password=password
    )

    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE " + database)
    cursor.execute(sql_script)

    conn.commit()
    print("Database created successfully.")
except psycopg2.errors.DuplicateDatabase:
    print("Database already exists.")

def identify_anomalies(result):
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        sql_query = "SELECT * FROM anomalies;"
        cursor.execute(sql_query)
        anomalies = cursor.fetchall()

        # Commit changes to the database
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        for anomalie in anomalies:
            if anomalie[1] == result:
                return anomalie



def extract_info(data):
    causes = extract_causes(data)
    cure = extract_cure(data)
    prevention = extract_prevention(data)
    resource = extract_resource(data)
    return causes, cure, prevention, resource

def extract_causes(result):
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        sql_query = "SELECT * FROM causes;"
        cursor.execute(sql_query)
        causes = cursor.fetchall()
        print(causes)
        # Commit changes to the database
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        for cause in causes:
            if cause[1] == result:
                return cause[2]

def extract_cure(result):
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        sql_query = "SELECT * FROM cures;"
        cursor.execute(sql_query)
        cures = cursor.fetchall()
        print(cures)
        # Commit changes to the database
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        for cure in cures:
            if cure[1] == result:
                return cure[2]


def extract_prevention(result):
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        sql_query = "SELECT * FROM preventions;"
        cursor.execute(sql_query)
        preventions = cursor.fetchall()
        # Commit changes to the database
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        for prevention in preventions:
            if prevention[1] == result:
                return prevention[2]

def extract_resource(result):
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        sql_query = "SELECT * FROM resources;"
        cursor.execute(sql_query)
        resources = cursor.fetchall()
        # Commit changes to the database
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        for resource in resources:
            if resource[1] == result:
                return resource[2]

def delete_database(database):
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        sql_query = "DROP DATABASE " + database +";"
        cursor.execute(sql_query)
        # Commit changes to the database
        conn.commit()
        print("Database deleted")
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

#delete_database(database)

# tester database

def extract_data():
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        sql_query = """SELECT * FROM anomalies.cures;"""
        cursor.execute(sql_query)
        result = cursor.fetchall()

        # Commit changes to the database
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        print(result)

extract_data()

def close_sql():
    cursor = conn.cursor
    # Close the cursor
    cursor.close()

    # Close the connection
    conn.close()
