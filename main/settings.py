import yaml
import psycopg2

def get_config(path):
	global doc_table_name
	doc_table_name = "documents"
	global index_table_name
	index_table_name = "index"

	global config
	with open(path) as file:
		config=yaml.load(file)
	global conn 
	conn = psycopg2.connect("dbname="+config['database']+" password="+config['password']+" user="+config['user'])