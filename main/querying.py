from aiohttp import web
import psycopg2
import json
from main import settings

async def get(request):
	"""
	get ==>
	{
		"url": string[]
	}

	response: ==>
	{
		"data":
		[
			{
				"docId": string,
				"url": string,
				"title": string,
				"header": string[],
				"body": string[]
			},
			...
		]
	}
	"""
	try:
		request = await request.json()
		cur = settings.conn.cursor()

		urls = request["url"]

		data = []

		for url in urls:
			sql_statement = "SELECT id, url, title, sect_headings, paragraphs\
							FROM "+ settings.doc_table_name +"\
							WHERE url='%s'" %(url)
			cur.execute(sql_statement)
			answer = cur.fetchone()
			if answer:
				print(answer)
				answer_resp = {"docId": answer[0], "url": answer[1], "title": answer[2], "header": answer[3], "body": answer[4]}
				data.append(answer_resp)
			else:
				data.append({})

		settings.conn.commit()
		cur.close()
		response_obj = {"status": 200,
						"data": data}
		return web.Response(text=json.dumps(response_obj), status=200)

	except Exception as e:
		print(e)
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)