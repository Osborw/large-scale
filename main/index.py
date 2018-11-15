from aiohttp import web
import psycopg2
import json
import hashlib
from main import settings

async def index(request):
	return web.Response(text="WORKING")