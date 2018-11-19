from aiohttp import web
import json
import os
from main import data,settings,index
import psycopg2

def init_db():
	cur = settings.conn.cursor()

	#Check if doc_store table exists
	cur.execute("SELECT to_regclass('" + settings.doc_table_name + "')")
	#print(cur.fetchall())
	if cur.fetchall()[0][0] == None:
		create_db(cur)
		print("Initialized DBs 'doc_store' and 'index'")
		return
	print("DBs 'documents' and 'index' already initialized")
	return

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

def init_routes(app):
	app.router.add_get('/', index.index)
	app.router.add_post('/crawling', data.crawling.post)
	app.router.add_post('/tt', data.text_transformation.post)
	app.router.add_post('/la', data.link_analysis.post)

	#This is technically a GET i guess, but it's not good pratice to put json in a GET request
	#Option 1: Make this a post instead and just return a lot of data
	#Option 2: Make docId a parameter in the URL instead and not have it be an array
	app.router.add_post('/querying', data.querying.get)

#Load config.yaml settings. Can be accessed with app['config']. config.yaml is located in .\config\

if __name__ == "__main__":
	app = web.Application()
	settings.get_config(os.path.dirname(os.path.realpath(__file__))+"/config/config.yaml")
	init_db()
	init_routes(app)
	web.run_app(app, host=settings.config['host'], port=settings.config['port'])