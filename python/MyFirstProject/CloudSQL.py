import os
import sqlalchemy

db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

db = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_pass,
        database=db_name,
        # 文件上有，但實際上加上去會出現Can’t connect to MySQL server on ‘localhost’ ([Errno 2] No such file or directory)
        # query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
    ),
    pool_size=5,
    max_overflow=2,
    pool_timeout=30, 
    pool_recycle=1800,
)

def query():
    print('query!')
    with db.connect() as conn:
        # Execute the query and fetch all results
        recent_votes = conn.execute(
            "SELECT guestName,content FROM entries"
        ).fetchall()
        # Convert the results into a list of dicts representing votes
        for row in recent_votes:
            print("guestName=",row[0], "    content=",row[1])
    print('query end!')

def save(a,b):
    print('save')
    stmt = sqlalchemy.text(
        "INSERT INTO entries (guestName, content)" " VALUES (:a, :b)"
    )
    try:
        with db.connect() as conn:
            conn.execute(stmt, a=a, b=b)
    except Exception as e:
        print('insert error', e)


# save('python a', 'python b')
query()
