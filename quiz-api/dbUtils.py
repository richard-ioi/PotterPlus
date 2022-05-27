import sqlite3
#création d'un objet connection
db_connection = sqlite3.connect('../db.db')
# set the sqlite connection in "manual transaction mode"
# (by default, all execute calls are performed in their own transactions, not what we want)
db_connection.isolation_level = None

# start transaction
sqlite3.cursor.execute("begin")

# save the question to db
insertion_result = sqlite3.cursor.execute(
	f"insert into Question (title) values"
	f"('{input_question.title}')")

#send the request
sqlite3.cursor.execute("commit")

#in case of exception, roolback the transaction
sqlite3.cursor.execute('rollback')
