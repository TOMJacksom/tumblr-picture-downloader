import json
import requests
import math
from time import sleep
import urllib
import re
import threading
import time
import Queue, thread
from requests_oauthlib import OAuth1
import os
									   
oauth = OAuth1('LavgbZzW1LV2skL5EMhhrEucUPikpP4Ag6KKNBJB77dojfzfaw',
                            client_secret='6JQ50VNpMgNeUxkRHy8eXzCTg48CyK1cbLzkxrKOm1MFnV5yvH',
                            resource_owner_key='resource_owner_key',
                            resource_owner_secret='resource_owner_secret')

script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'images')

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
clear = "\n" * 100
offset = 0
request_count = 0
loading = 0
loadingtwo = 0
problem = 0

tumblr = raw_input('Enter the tumblr url: ')
tumblr = tumblr.split('/', 1)[-1]
tumblr = tumblr.split('/', 1)[-1]
tumblr = re.sub('[/]', '', tumblr)
tumblr.strip()
#print tumblr

dick_url = 'http://api.tumblr.com/v2/blog/'+tumblr+'/info?api_key=LavgbZzW1LV2skL5EMhhrEucUPikpP4Ag6KKNBJB77dojfzfaw'
info = requests.get(dick_url, auth=oauth).json()
#print info["response"]["blog"]["total_posts"]
rangeR = info["response"]["blog"]["total_posts"]
loadingtwo = rangeR
rangeR = int(rangeR / 20) + 1



def download_url(str, file):
	while True:
		try:
			urllib.urlretrieve(str, file)
			global loading
			loading = loading + 1
		
		except IOError:
			continue
		else:
			break



def find_url(r, nused):
	while True:
		try:
			for i in r["response"]["posts"]:
			
				id = i["id"]
				id = str(id)
				#print id
				test_url = 'http://api.tumblr.com/v2/blog/'+tumblr+'/posts?id='
				test_url += str(i["id"]) + "&api_key=LavgbZzW1LV2skL5EMhhrEucUPikpP4Ag6KKNBJB77dojfzfaw"
				#print test_url
				testinfo = requests.get(test_url, auth=oauth).json()
				for aa in testinfo["response"]["posts"]:
					if 'photos' not in aa:
						continue
					else:
						for bb in aa["photos"]:
							#print bb["original_size"]["url"]
							filename = str(bb["original_size"]["url"])
							filename = filename.split('_', 1)[-1]
							filename = os.path.join(dest_dir, filename)
							while threading.activeCount() >= 100:
								sleep(2)
							else:
								thread.start_new(download_url, (bb["original_size"]["url"], filename))

		except requests.exceptions.RequestException:
			global problem
			problem = problem + 1
			sleep(5)
			continue
		else:
			break


for x in range (1, rangeR):
	if loading > loadingtwo:
		break
	else:
		while True:
			try:
				fuck = 2
				time = None
				request_url = 'http://api.tumblr.com/v2/blog/'+tumblr+'/posts?api_key=LavgbZzW1LV2skL5EMhhrEucUPikpP4Ag6KKNBJB77dojfzfaw&limit=20'
				request_url += "&offset=" + str(offset)
				#print request_url
				r = requests.get(request_url, auth=oauth).json()
	
	

				pass
				offset += 20
				request_count += 1
				perc = (float(loading) / loadingtwo) * 100
				tidy = float("{0:.2f}".format(perc))
				print clear
				print str(loading)+' out of '+str(loadingtwo)+'  %'+str(tidy)+' done.'

				#print offset
				if request_count == 900:
					sleep(60)
					request_count = 0
		
				if r["meta"]["status"] != 200:
					raise Exception
			
				if problem >= 1:
					sleep(5)
					problem = 0
				else:
					while threading.activeCount() >= 100:
						sleep(5)
					else:
						thread.start_new(find_url,(r, "n"))
		
			except Exception:
					continue
				
			else:
				break