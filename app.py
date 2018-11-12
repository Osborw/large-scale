from aiohttp import web
import json
from main import data

app = web.Application()
app.router.add_post('/crawling', data.crawling.post)
app.router.add_post('/tt', data.text_transformation.post)
app.router.add_post('/la', data.link_analysis.post)

#This is technically a GET i guess, but it's not good pratice to put json in a GET request
#Option 1: Make this a post instead and just return a lot of data
#Option 2: Make docId a parameter in the URL instead and not have it be an array
app.router.add_post('/querying', data.querying.get)

if __name__ == "__main__":
	web.run_app(app)