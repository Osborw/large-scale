import yaml
import psycopg2

def get_config(path):
	global config
	with open(path) as file:
		config=yaml.load(file)
	global conn 
	conn = psycopg2.connect("dbname="+config['database']+" password="+config['password']+" user="+config['user'])