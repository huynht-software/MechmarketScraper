#! usr/bin/env python3
import praw
import psycopg2
from configparser import ConfigParser

personal_key = "fN7PYFUt5Wmicg"
secret_key = "WWzdzOK4afXXgEMcQ7F32VeKzHFsLg"
app_name = "mechmarket parser"

reddit = praw.Reddit(client_id=personal_key, \
                     client_secret=secret_key, \
                     user_agent=app_name)

mechmarket = reddit.subreddit("mechmarket")
submissions = mechmarket.new(limit=50)


for submission in submissions:
    post = {}
    post["post_name"] = submission.title
    post["post_id"] = submission.id
    post["selftext"] = submission.selftext
    post[]

# implement following parsers:
#    post_name 
#    post_id 
#    selftext 
#    score 
#    region 
#    tag
#    have
#    want 
#    date


try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "Blutwurst1",
                                  database = "posts")
    cursor = connection.cursor()

    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
    
    # server loop goes here

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")