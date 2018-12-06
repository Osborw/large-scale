from aiohttp import web
import psycopg2
import json


#Interaction with Ranking

# Aynchronous handling method for POST requests from Ranking
# INPUT : The post request
# OUTPUT : A web response, with HTTP code 200 on success
# SIDE EFFECTS : the inverse index database and doc store are updated with
#                the item(s) provided in the POST request JSON
async def post(request):
	request = await request.json()

	response_obj = {"status": 200}
	return web.Response(text=json.dumps(response_obj), status=200)
    # TODO: more error handling here?
