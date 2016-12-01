#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import requests
import re, json, os

logging.basicConfig(format='%(message)s')#, filename='m.html')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PLAYER_NAME = 'audioplay.exe'

class Spider(object):
	"""web spider"""
	host_url = 'http://y.qq.com/portal/search.html'
	search_url = 'http://c.y.qq.com/soso/fcgi-bin/search_cp'
	base_url = 'http://y.qq.com/portal/song/'
	media_url = 'http://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid=003OUlho2HcRHC&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback&g_tk=938407465&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
	lyric_url = 'http://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid=107192078&callback=jsonp1&g_tk=938407465&jsonpCallback=jsonp1&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
	header = {'User-Agent': '''Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36''',
				'Connection': 'keep-alive',
				'Upgrade-Insecure-Requests': '1',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Encoding': 'gzip, deflate, sdch',
				'Accept-Language': 'zh-CN,zh;q=0.8'}

	search_data = {
			'remoteplace': 'txt.yqq.center',
			't': '0',
			'aggr': '1',
			'cr': '1',
			'catZhida': '1',
			'lossless': '0',
			'flag_qc': '0',
			'g_tk': '5381',
			'jsonpCallback': 'searchCallbacksong5460',
			'loginUin': '0',
			'hostUin': '0',
			'format': 'jsonp',
			'inCharset': 'utf8',
			'outCharset': 'utf-8',
			'notice': '0',
			'platform': 'yqq',
			'needNewCode': '0',
			'searchid': '155151',
			'p': '1',
			'n': '20',
			'w': ''
		}


	def __init__(self):
		super(Spider, self).__init__()
#		httpHandler = r.HTTPHandler(debuglevel=1)

	def getMediaStream(self, mid):
		data = {
			'songmid': mid, #'003OUlho2HcRHC',
			'tpl': 'yqq_song_detail',
			'format': 'jsonp',
			'callback': 'getOneSongInfoCallback',
			'g_tk': '938407465',
			'jsonpCallback': 'getOneSongInfoCallback',
			'loginUin': '0',
			'hostUin': '0',
			'format': 'jsonp',
			'inCharset': 'utf8',
			'outCharset': 'utf-8',
			'notice': '0',
			'platform': 'yqq',
			'needNewCode': '0'
		}
		media_url = 'http://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg'
		r = requests.get(media_url, headers=self.header, params=data)
		logger.info(r.url)
		logger.info(r.text)
		result = re.findall(r'\S+\((.*)\)', r.text)
		result = json.loads(result[0])
		logger.info(result['url'])
		id = result['data'][0]['id']
		return 'http://' + result['url'][str(id)]
#		logger.info(r.url)
#		logger.info(r.text)

	def startStream(self, url):
		r = requests.get(url, headers=self.header)
#		logger.info(r.text)
		f = open('music.mp3', 'wb+')
		f.write(r.content)
		f.close()
		os.system(PLAYER_NAME + ' music.mp3')
		#os.system('music.mp3')

	def getSong(self, name):
		self.search_data['w'] = name
		r = requests.get(self.search_url, headers=self.header, params=self.search_data)
		logger.info(r.url)
		result = re.findall(r'\S+\((.*)\)', r.text)
		result = json.loads(result[0])

		try:
			if result:
				totalNum = result['data']['song']['totalnum']
				if (0 == totalNum) :
					logger.info('%s was not found.' % name)
					return None
				logger.info('total number: %d' % totalNum)
		
				l = result['data']['song']['list']
				#logger.info(l[0])

				base_url = 'http://y.qq.com/portal/song/'
#				r = requests.get(base_url + l[0]['strMediaMid'] + '.html', headers=self.header)
				media_url = 'http://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid=003OUlho2HcRHC&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback&g_tk=938407465&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
				lyric_url = 'http://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid=107192078&callback=jsonp1&g_tk=938407465&jsonpCallback=jsonp1&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
				logger.info(l[0])
				#media = self.getMediaStream(l[0]['strMediaMid'])
				media = self.getMediaStream(l[0]['songmid'])
				logger.info(media)
				if media:
					self.startStream(media)
	#			result = r.text
	#			logger.info(r.url)
	#			logger.info(result)
		except KeyError as e:
			logger.error(e)


	def request(self, url, data=None):
		req = r.Request(url, data=data, headers=header, method='GET')
		response = r.urlopen(req)
		return response
		#logger.info(response.read().decode('utf-8'))

def main():
	spider = Spider()
	#songName = '告白气球'
	songName = '龙卷风'
	while True :
		songName = input('你想听什么：')
		spider.getSong(songName)
	return

if __name__ == '__main__':
	main()
