import psycopg

def get_connection():
    # read password from a file (pw.txt)
    with open("pw.txt", "r") as f:
        password = f.read().strip()

    # connect to the database
    conn = psycopg.connect(f"postgresql://neondb_owner:{password}@ep-muddy-poetry-aqy0ko1l-pooler.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
    
    return conn