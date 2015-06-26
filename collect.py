# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from urlparse import urlparse
from os.path import splitext,basename,isdir
from os import makedirs
import re
import urllib2


def crawl(topic_id,folder_name,page = 0):
	base_url = "http://onehallyu.com/index.php?showtopic=%s&page=%s"
	#make the directory if not exist
	if not isdir(folder_name):
		makedirs(folder_name)

	base_path = folder_name + "/page_%s/"
	#loop until no more page left
	while True:
		page = page + 1
		crawl_link  = base_url % (topic_id,page)
		#load the page
		r = requests.get(crawl_link.encode('utf-8'))
		
		#end if no more page
		if r.status_code != 200:
			break
		print "crawling page %s" %page,
		soup = BeautifulSoup(r.text)
		#retrieve all links in the page
		image_tag = soup.findAll("img")
		
		image_links = []
		#filter the images
		for i in image_tag:
			src = i.get('src')
			#remove pics with 'onehallyu' in link(internal images)
			#remove pics with 'public' in link(style images)
			if ('onehallyu' not in src) and ('public' not in src):
				image_links.append(src)

		#make path for current page
		path = base_path % (page)
		if not isdir(path) :
			makedirs(path)

		for i in image_links:
			r = requests.get(i, stream=True)
			if r.status_code == 200:
				try:
					filename = re.findall("filename=(\S+)", r.headers['Content-Disposition'])[0][1:-1]
					filename = urllib2.unquote(filename).decode('utf-8')
				except:
					filename = splitext(basename(urlparse(i).path))
					filename = filename[0] + filename[1]
				with open(path + filename, 'wb') as f:
					for chunk in r.iter_content(1024):
						f.write(chunk)
		print "images saved: %s" % len(image_links),
		print "DONE."

#modify this line to collect data
#    crawl(topic_id,folder_name)
# this will crawl the topic with the correcponding id, and save all the images into folder 'folder_name', arranged by page number
crawl(88119,"irene",7)