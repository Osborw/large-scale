from aiohttp import web
import psycopg2
import json
import hashlib
from main import settings

async def post(request):
	"""
	{
		"metadata": {
			"url": string,
			"title": string,
			"description": string,
			"keywords": string[],
			"authors": string[]
		},
		"text": {
			"headings": string[],
			"body": []
		},
		"grams": [{
			"gram": string,
			"headingfreq": double,
			"bodyfreq": double
		}]
	}
	"""
	try:
		request = await request.json()
		cur = settings.conn.cursor()

		url = request["metadata"]["url"] #Doc store
		doc_id = hashlib.md5(url.encode('utf-8')).hexdigest()
		title = request["metadata"]["title"] #Doc store
		description = request["metadata"]["description"] #Doc store
		headings = request["text"]["headings"] #Doc store
		headings_string = createArrayString(headings)
		body = request["text"]["body"] #Doc store
		body_string = createArrayString(body)

		
		keywords = request["metadata"]["keywords"]
		keywords_string = createArrayString(keywords)
		authors = request["metadata"]["authors"]
		authors_string = createArrayString(authors)

		grams = request["grams"]
		for gram in grams:
			ngram = gram["gram"]
			headingfreq = gram["headingfreq"]
			bodyfreq = gram["bodyfreq"]
			in_title = ngram in title
			in_description = ngram in description
			in_keywords = ngram in keywords
			cur.execute("SELECT 1 FROM "+ settings.index_table_name +" WHERE ngram='%s' and docid='%s';" %(ngram, doc_id))
			if len(cur.fetchall()) == 0:
				sql_statement = "INSERT INTO "+ settings.index_table_name +"\
								VALUES ('%s', '%s', '%r', '%r', '%r', '%.8f', '%.8f');" %(ngram, doc_id, in_title, in_description, in_keywords, headingfreq, bodyfreq)
				cur.execute(sql_statement)

		cur.execute("SELECT 1 FROM "+ settings.doc_table_name +" WHERE id='%s';" %(doc_id))
		if(len(cur.fetchall())==0):
			sql_statement = "INSERT INTO "+ settings.doc_table_name +" (id, url, title, description, sect_headings, paragraphs)\
							VALUES ('%s','%s', '%s', '%s', '%s', '%s');" %(doc_id,url, title, description, headings_string, body_string)
		else:
			sql_statement = "UPDATE "+ settings.doc_table_name +"\
							SET title='%s', description='%s', sect_headings='%s', paragraphs='%s'\
							WHERE id='%s';" %(title, description, headings_string, body_string, doc_id)
		cur.execute(sql_statement)

		settings.conn.commit()
		cur.close()

		response_obj = {"status": "Successfully input data"}
		return web.Response(text=json.dumps(response_obj), status=200)

	except Exception as e:
		print(e)
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)

def createArrayString(array):
	string = "{"
	for item in array:
		string += '"%s", ' %(item)
	string = string.strip(", ")
	string += "}"
	return string