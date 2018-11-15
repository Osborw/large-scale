import signal
import sys
import asyncio
import aiohttp
import json
import os

#This was just a temporary client test for link analysis

async def main1():
    print(data)
    async with aiohttp.ClientSession(loop=loop) as client:
    	async with client.post('http://127.0.0.3:5433/la',data=data) as response:
        	#Do stuff here
        	print(response)

f=open(os.path.dirname(os.path.realpath(__file__))+"\\test_helper\\link_analysis_input1.json")
data=f.read()

loop = asyncio.get_event_loop()
loop.run_until_complete(main1())