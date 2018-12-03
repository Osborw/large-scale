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
		urls = request["urls"]

		cur = settings.conn.cursor()

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

		response_obj = {"status": "Successfully modified data"}

		settings.conn.commit()
		cur.close()
		return web.Response(text=json.dumps(response_obj), status=200)

	except Exception as e:
		print(e)
		if cur!=None: cur.close()
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)