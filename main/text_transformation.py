from aiohttp import web
import psycopg2
import json
import hashlib
from main import settings

#Interaction with Text Transformation

# Aynchronous handling method for POST requests from Text Transformation
# INPUT : The post request
# OUTPUT : A web response, with HTTP code 200 on success, or 500 on failure
# SIDE EFFECTS : the inverse index database and doc store are updated with
#                the item(s) provided in the POST request JSON
async def post(request):
    # the JSON schema we are expecting
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
        # Let the developer/anyone watching the console to know that
        #   a request was received, and pick the JSON out of it
		print("Recieved TT POST request from " + request.remote)
		request = await request.json()

        # Get the cursor to our database
		cur = settings.conn.cursor()

        # Extract the different fields from the JSON in the request and
        #   store in variables. We also generate the docID here.
        # TODO: better error checking if fields here are blanck
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

        # As above, but we need to loop over each n-gram in the POST
        # Note that we re-use the info from above - the inverse index
        #   is stored with the n-grams as keys, so we need to make sure
        #   we add the other info for each page to each entry.
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
        
        # SQL to make the updates
		cur.execute("SELECT 1 FROM "+ settings.doc_table_name +" WHERE id='%s';" %(doc_id))
		if(len(cur.fetchall())==0):
			sql_statement = "INSERT INTO "+ settings.doc_table_name +" (id, url, title, description, sect_headings, paragraphs)\
							VALUES ('%s','%s', '%s', '%s', '%s', '%s');" %(doc_id,url, title, description, headings_string, body_string)
		else:
			sql_statement = "UPDATE "+ settings.doc_table_name +"\
							SET title='%s', description='%s', sect_headings='%s', paragraphs='%s'\
							WHERE id='%s';" %(title, description, headings_string, body_string, doc_id)
		cur.execute(sql_statement)

        # Commit changes and close cursor to the database
		settings.conn.commit()
		cur.close()

		response_obj = {"status": "Successfully input data"}
		return web.Response(text=json.dumps(response_obj), status=200)

    # If the above block encounters a problem along the way (parsing or updating),
    #   print the Exception to the console, and also return it to the requestor with
    #   an HTTP 500 to alert them of failure, too.
	except Exception as e:
		print(e)
		cur.close()
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)
# /post()

# JSON formatting method for turning a Python array into a JSON array
# INPUT : the array object
# OUTPUT : the array formatted as a string
# SIDE EFFECTS : none
def createArrayString(array):
	string = "{"
	for item in array:
		string += '"%s", ' %(item)
	string = string.strip(", ")
	string += "}"
	return string
