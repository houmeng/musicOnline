#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import json, base64

def speechRec(pcmdata):
    apiKey = "NumMMqncilPZNdal1T7enA2t"
    secretKey = 'c168e5ada66182c494e88f3966fd7e5d'

    # get access token from baidu
    url = ("""https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"""
           % (apiKey, secretKey))
    req = requests.get(url)
    #print(req.text)
    accessToken = req.json()['access_token']

    # send speech data
    url_upload = 'http://vop.baidu.com/server_api'
    data = {
        'format': 'pcm',
        'rate': 8000,
        'channel': 1,
        'cuid': '12332424',
        'token': accessToken,
        'speech': base64.b64encode(pcmdata).decode('utf-8'),
        'len': len(pcmdata)
        }
    req = requests.put(url_upload, data = json.dumps(data))
    #print(req.headers)
    result = req.json()
    if 0 == result['err_no']:
        return result['result']
    print('speech recognition failed:%d' % result['err_no'])

def main():
    f = open('test.pcm', mode='rb')
    pcmdata = f.read()
    inst = speechRec(pcmdata)
    print(inst)
    f.close()

if __name__ == '__main__':
    main()
