from aiohttp import web
import psycopg2
import json

async def post(request):

	request = await request.json()

	response_obj = {"status": 200}
	return web.Response(text=json.dumps(response_obj), status=200)