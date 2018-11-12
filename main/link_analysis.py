from aiohttp import web
import psycopg2
import json

async def post(request):
	"""
	{
		"url": string[],
		"pagerank": double[],
		"normalized_pagerank": double[]
	}
	"""
	try:
		request = await request.json()
		url = request["url"]
		pagerank = request["pagerank"]
		normalized_pagerank = request["normalized_pagerank"]

		"""
		So right now, every section has to do this individually, and it's not a great practice tbh.
		I'll likely subclass all these sections so that I only have to put imports once
		and only have to connect once, but there's not enough time right now to refactor all this.
		"""
		#Connnect to DB
		"""TODO: The connection parameters should be in a config file for safety and loaded from there"""
		conn = psycopg2.connect("dbname=wosborn user=wosborn")
		cur = conn.cursor()

		for i in range(0,len(url)):
			i_url = url[i]
			i_pagerank = pagerank[i]
			i_normalized_pagerank = pagerank[i]
			sql_statement = "INSERT INTO doc_store (url, pagerank, norm_pagerank) VALUES ('%s', %.8f, %.8f);" %(i_url, i_pagerank, i_normalized_pagerank)
			cur.execute(sql_statement)

		#For debugging purposes, I like to see what the DB looks like after the request
		cur.execute("SELECT * FROM doc_store LIMIT 15")
		db_result = cur.fetchall()
		print(db_result)

		response_obj = {"status": "Successfully added data"}

		cur.close()
		return web.Response(text=json.dumps(response_obj), status=200)

	except Exception as e:
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)