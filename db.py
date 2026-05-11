import psycopg

def get_connection():
    # read password from a file (pw.txt)
    with open("pw.txt", "r") as f:
        password = f.read().strip()

    # connect to the database
    conn = psycopg.connect(f"postgresql://neondb_owner:{password}@ep-hidden-lake-apcmtur5-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

    return conn





# read the DDL file
# with open("snack_overflow_pg.sql", "r") as f:
#     ddl = f.read()

# execute the DDL
# with conn.cursor() as cur:
#     cur.execute(ddl)

# commit the changes
# conn.commit()

# close the connection
# conn.close()
