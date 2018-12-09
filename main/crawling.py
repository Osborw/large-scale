from aiohttp import web
import psycopg2
import json
import hashlib
from main import settings

# Interaction with Crawling

# Aynchronous handling method for POST requests from Crawling
# INPUT : The post request
# OUTPUT : A web response, with HTTP code 200 on success, or 500 on failure
# SIDE EFFECTS : Item(s) specified in the request are removed from the 
#                  databases due to broken/invalid links
async def post(request):
    # The expected JSON format for requests coming in from Crawling
	"""
	{
		"url": string,
		"error_code": int,
		"redirect": string
	}
	"""
	try:
		cur = None

        # Let whomever is watching the console know that a request has been received
		print("Recieved Crawling POST request from " + request.remote)
		request = await request.json()
		urls = request["urls"]

        # Get the cursor
		cur = settings.conn.cursor()

        # Iterate over the URL's in the request json, hash the docID for reference within
        #   the db, and make updates where necessary.
        # Then make the DELETE sql queries to make the necessary updates
		for url in urls:
			doc_id = hashlib.md5(url.encode('utf-8')).hexdigest()
			sql_statement = "DELETE FROM "+ settings.doc_table_name +" WHERE url = '%s';" %(url)
			cur.execute(sql_statement)
			sql_statement = "DELETE FROM "+ settings.index_table_name +" WHERE docid = '%s';" %(doc_id)
			cur.execute(sql_statement)

		#For debugging purposes, I like to see what the DB looks like after the request
		cur.execute("SELECT * FROM "+ settings.doc_table_name +" LIMIT 15")
		db_result = cur.fetchall()
		print(db_result)
        
        # Here all the response needs to know is that we modified the data
		response_obj = {"status": "Successfully modified data"}
        # Commit updates and close the cursor
		settings.conn.commit()
		cur.close()
		return web.Response(text=json.dumps(response_obj), status=200)

        # If we have a problem performing the above, send a 500 instead
	except Exception as e:
		print(e)
		if cur!=None: cur.close()
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)
