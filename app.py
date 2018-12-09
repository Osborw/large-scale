from aiohttp import web
import json
import os
from main import data,settings,index
import psycopg2

# Creates and initializes the databases
# INPUT : none
# OUTPUT : none (helpful dev notes to the console, though)
# SIDE EFFECTS : If the databases already exist and are initialized,
#                  does nothing but make note of this in the console.
#                Otherwise, creates and initializes the dbs using the
#                  create_db method below
def init_db():
    # Fetches the client-side cursor from our db's connection
    # For more inforation, see http://initd.org/psycopg/docs/connection.html#connection.cursor
	cur = settings.conn.cursor()

	# Check if doc_store table exists
	cur.execute("SELECT to_regclass('" + settings.doc_table_name + "')")
	#print(cur.fetchall())
    # if the doc_store table does not exist, create it
	if cur.fetchall()[0][0] == None:
		create_db(cur)
		print("Initialized DBs 'doc_store' and 'index'")
		return
    # otherwise, let us know that the dbs are already initialized
	print("DBs 'documents' and 'index' already initialized")
	return
# /init_db()


# Creates the initial databases: one for the document store, and one for
#   the inverse index.
# Note that we are assuming in the above method that we have already checked
#   to make sure the databases don't already exist.
# INPUT : the db connection's cursor
# OUTPUT : none
# SIDE EFFECTS : Two tables are created, one for document store, and one for
#                  the inverse index. These are committed to the postgres db
def create_db(cur):
	sql_statement = "CREATE TABLE " + settings.doc_table_name + " ( \
						id VARCHAR PRIMARY KEY, \
						url VARCHAR NOT NULL, \
						pagerank real, \
						norm_pagerank real, \
						title VARCHAR, \
						description VARCHAR, \
						sect_headings VARCHAR[], \
						paragraphs VARCHAR[], \
						date_crawled DATE, \
						date_updated DATE );"

	#print(sql_statement);
	cur.execute(sql_statement)

	sql_statement = "CREATE TABLE " + settings.index_table_name +" ( \
						ngram VARCHAR NOT NULL, \
						docid VARCHAR NOT NULL, \
						in_title BOOLEAN NOT NULL, \
						in_desc BOOLEAN NOT NULL, \
						in_keywords BOOLEAN NOT NULL, \
						freq_headings REAL NOT NULL, \
						freq_text REAL NOT NULL, \
						PRIMARY KEY(ngram, docid));"

	cur.execute(sql_statement)

	settings.conn.commit()
	cur.close()
# /create_db()


# Initializes the routes on the server, namely the separate endpoints
#   for crawling, text transformation, and link analysis teams to access
#   the database.
# INPUT : the web Application object
# OUTPUT : none
# SIDE EFFECTS : The web app is configured with the endpoint routes for 
#                  other teams' API calls and queries
def init_routes(app):
	app.router.add_get('/', index.index)
	app.router.add_post('/crawling', data.crawling.post)
	app.router.add_post('/tt', data.text_transformation.post)
	app.router.add_post('/la', data.link_analysis.post)

	#This is technically a GET i guess, but it's not good pratice to put json in a GET request
	#Option 1: Make this a post instead and just return a lot of data
	#Option 2: Make docId a parameter in the URL instead and not have it be an array
	app.router.add_get('/querying', data.querying.get)

#Load config.yaml settings. Can be accessed with app['config']. config.yaml is located in .\config\


# Run this to initialize the webapp and the database
if __name__ == "__main__":
	app = web.Application()
	settings.get_config(os.path.dirname(os.path.realpath(__file__))+"/config/config.yaml")
	init_db()
	init_routes(app)
	web.run_app(app, host=settings.config['host'], port=settings.config['port'])
