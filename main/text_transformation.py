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
			"charset": string
			"url": string,
			"title": string,
			"timestamp" : string
			"description": string[],
			"keywords": string[],
			"docid": int
		},
		"text": {
			"headings": string[],
			"body": []
		},
		"ngrams": {
			"all" : {
				"1grams" : {
					"gram" : int (count),
					"gram2" : int (count)
				},
				"2grams" : {
					"gram" : int,
					"gram2" : int
				},
				... up to 5grams
			},
			"headers" : {
				...same format as above
			},
			"title" : {
				...same format as above
			}
		}
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
		metadata = request["metadata"]
		text = request["text"]
		ngrams = request["ngrams"]

		#Grab all metadata
		charset = metadata["charset"]
		url = metadata["url"]
		doc_id = hashlib.md5(url.encode('utf-8')).hexdigest()
		title = metadata["title"]
		timestamp = metadata["timestamp"]
		description = metadata["description"]
		keywords = metadata["keywords"]
		description_string = createArrayString(description)
		#docid = metadata["docid"]

		#Grab all text
		headings = text["headings"]
		body = text["body"]
		headings_string = createArrayString(headings)
		body_string = createArrayString(body)


		#Get total count of all ngrams to use later
		text_count = 0
		headers_count = 0
		for gram_size in ngrams["all"]:
			for gram in ngrams["all"][gram_size]:
				text_count += ngrams["all"][gram_size][gram]

		for gram_size in ngrams["headers"]:
			for gram in ngrams["headers"][gram_size]:
				headers_count += ngrams["headers"][gram_size][gram]

		#Grab all ngrams
		#Go through all ngrams, then go through heading ngrams and put in relevant information		
        # As above, but we need to loop over each n-gram in the POST
        # Note that we re-use the info from above - the inverse index
        #   is stored with the n-grams as keys, so we need to make sure
        #   we add the other info for each page to each entry.
		#Go through all ngrams
		for gram_size in ngrams["all"]:
			for gram in ngrams["all"][gram_size]:
				ngram = gram
				in_title = ngram in title
				in_desc = ngram in description
				in_keywords = ngram in keywords
				freq_text = ngrams["all"][gram_size][gram] / (text_count * 1.0)

				#Add all to database
				cur.execute("SELECT 1 FROM "+ settings.index_table_name +" WHERE ngram='%s' and docid='%s';" %(ngram, doc_id))
				if len(cur.fetchall()) == 0:
					sql_statement = "INSERT INTO "+ settings.index_table_name +"\
								VALUES ('%s', '%s', '%r', '%r', '%r', '%.8f', '%.8f');" %(ngram, doc_id, in_title, in_desc, in_keywords, 0.0, freq_text)
					cur.execute(sql_statement)
				else:
					sql_statement = "UPDATE "+ settings.index_table_name +" SET (in_title, in_desc, in_keywords, freq_text) = ('%r', '%r', '%r', '%.8f') \
								WHERE ngram='%s' and docid='%s';" %(in_title, in_desc, in_keywords, freq_text, ngram, doc_id)
					cur.execute(sql_statement)

		#Go through header ngrams
		for gram_size in ngrams["headers"]:
			for gram in ngrams["headers"][gram_size]:
				ngram = gram
				freq_headings = ngrams["headers"][gram_size][gram] / (headers_count * 1.0)

				#Add all to database
				cur.execute("SELECT 1 FROM "+ settings.index_table_name +" WHERE ngram='%s' and docid='%s';" %(ngram, doc_id))
				if len(cur.fetchall()) == 0:
					in_title = ngram in title
					in_desc = ngram in description
					in_keywords = ngram in keywords
					sql_statement = "INSERT INTO "+ settings.index_table_name +"\
								VALUES ('%s', '%s', '%r', '%r', '%r', '%.8f', '%.8f');" %(ngram, doc_id, in_title, in_desc, in_keywords, freq_headings, 0.0)
					cur.execute(sql_statement)
				else:
					sql_statement = "UPDATE "+ settings.index_table_name +" SET freq_headings = '%.8f' \
								WHERE ngram='%s' and docid='%s';" %(freq_headings, ngram, doc_id)
					cur.execute(sql_statement)

        
        # SQL to make the updates
		cur.execute("SELECT 1 FROM "+ settings.doc_table_name +" WHERE id='%s';" %(doc_id))
		if(len(cur.fetchall())==0):
			sql_statement = "INSERT INTO "+ settings.doc_table_name +" (id, url, title, description, sect_headings, paragraphs, date_updated)\
							VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s');" %(doc_id,url, title, description_string, headings_string, body_string, timestamp)
		else:
			sql_statement = "UPDATE "+ settings.doc_table_name +"\
							SET title='%s', description='%s', sect_headings='%s', paragraphs='%s'\
							WHERE id='%s';" %(title, description_string, headings_string, body_string, doc_id)
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
