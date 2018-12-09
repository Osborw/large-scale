from aiohttp import web
import psycopg2
import json
import hashlib
from main import settings

# Checks on the status of the index
# INPUT : any request
# OUTPUT : "WORKING", assuming the index is up. Otherwise,
#            it's not like the server can respoond anyway....
# SIDE EFFECTS : None, though if the request is supposed to do
#                  anything else in terms of handling, this method
#                  is not responsible for forwarding it.
async def index(request):
	return web.Response(text="WORKING")
