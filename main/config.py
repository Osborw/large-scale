import yaml

def get_config(path):
	global config
	with open(path) as file:
		config=yaml.load(file)