import yaml
import psycopg2

# config/config.yaml specifies the default settings for the database.
# This method reads that file and sets global variables that the rest
#   of the code will use to communicate with the database.
# INPUT : the path to the config.yaml file in the package
# OUTPUT : none
# SIDE EFFECTS : global variables are set: 
#                - doc_table_name for the document store db name
#                - index_table_name for the inverse index db name
#                - config for the loaded config.yaml file
#                - conn for the connection object to our database
#                    from psychopg2
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
