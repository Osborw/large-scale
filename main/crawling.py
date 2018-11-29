from aiohttp import web
import psycopg2
import json
import hashlib
from main import settings

async def post(request):
	"""
	{
		"url": string,
		"error_code": int,
		"redirect": string
	}
	"""
	try:

		cur = None

		print("Recieved Crawling POST request from " + request.remote)
		request = await request.json()
		url = request["url"]
		doc_id = hashlib.md5(url.encode('utf-8')).hexdigest()
		error_code = request["error_code"]
		redirect = request["redirect"]

		cur = settings.conn.cursor()

		#feel free to add or change html error codes
		if (int(error_code) == 403):
			redirect_id = hashlib.md5(redirect.encode('utf-8')).hexdigest()

			#Update in doc_store
			sql_statement = "UPDATE "+ settings.doc_table_name +" SET url = '%s', id = '%s' WHERE url = '%s';" %(redirect,redirect_id,url)
			cur.execute(sql_statement)

			#Update in index
			sql_statement = "UPDATE "+ settings.index_table_name +" SET docid = '%s' WHERE docid = '%s';" %(redirect_id, doc_id)
			cur.execute(sql_statement)

		#feel free to add or change html error codes
		elif (int(error_code) == 404):
			sql_statement = "DELETE FROM "+ settings.doc_table_name +" WHERE url = '%s';" %(url)
			cur.execute(sql_statement)
			sql_statement = "DELETE FROM "+ settings.index_table_name +" WHERE docid = '%s';" %(doc_id)
			cur.execute(sql_statement)

		#For debugging purposes, I like to see what the DB looks like after the request
		cur.execute("SELECT * FROM "+ settings.doc_table_name +" LIMIT 15")
		db_result = cur.fetchall()
		print(db_result)

		response_obj = {"status": "Successfully modified data"}

		settings.conn.commit()
		cur.close()
		return web.Response(text=json.dumps(response_obj), status=200)

	except Exception as e:
		print(e)
		if cur!=None: cur.close()
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)