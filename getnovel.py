# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import socket

import time

import sys

import urlparse


section_num = 1;

def html_process(html_file,url,text_name):
	'''
	use bs to get the titile && contain && next link from html_file
	'''
	global host_name
	global section_num

	#soup = BeautifulSoup(open(html_file),"html_parser")
	soup = BeautifulSoup(html_file,"html.parser")

	#####################################################
	file = open(text_name,'a')
	file.write('第 ' + str(section_num) + ' 章')
	section_num = section_num + 1

	#####################################################
	#get title
	title_ret = soup.title.string.split('-')[0].strip()
	file.write(' '+ title_ret+ '\r\n')

	file.write('\r\n' + url + '\r\n')
	#####################################################
	#get context
	#####################################################
	##MODIFY THIS TO MATCH DIFFERENT PAGE################
	print '######################################'
	
	file.write(soup.find_all("div",class_='temp22')[-1].get_text())
	file.close()

	#####################################################
	#get next href
	next_url = soup.find("span",class_='dcs1').a['href']
	print 'get next url' + next_url
	if len(next_url) >= 10:
		next_href = "http://" + host_name + next_url
		return next_href
	else:
		print 'get next url error'
		exit(1)

def html_get(url,retry=0):
	#user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0"
	user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0"
	headers = {'User-Agent':user_agent}
	print 'now to get ' + url
	req = urllib2.Request(url,headers = headers)
	try:
		page = urllib2.urlopen(req,timeout=90).read()
		return page
	except urllib2.URLError,e:
		print "error while loading" + url
		exit(1)
        except socket.timeout:
                #do retry
                print 'time out to fetch: ',url
                if retry == 0:
                        return html_get(url,retry = 1)
        except socket.error:
                print "socket error occured: ",url

def test(url,text_name):
	while None != url:
		html_file = html_get(url)
		if None == html_file:
			print 'ERROR OF READING ',url
			exit(1)
		url = html_process(html_file,url,text_name)
		time.sleep(1)


if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding( "utf-8" )

	if 3 != len(sys.argv):
		print 'input parate error. Need url txt'
		exit(1)

	url = sys.argv[1]
	txt = sys.argv[2]

	text_name = '/dev/shm/novel_'+ txt

	print 'dump url: '+url + ' to file: ' + text_name
	global host_name 
	host_name = urlparse.urlparse(url).hostname

	test(url,text_name)
