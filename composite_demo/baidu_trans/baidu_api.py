#/usr/bin/env python
# -*- coding:utf-8 -*-
import http.client
import hashlib
import urllib.request, urllib.parse, urllib.error
import random
import traceback
import json
import time
from baidu_trans.setting import (API_URL, APP_ID, BASE_URL, SECRET_KEY)


class Translator(object):
    def __init__(self):
       pass

    def translate(self, from_lang, to_lang, query_text):
        httpClient = None
        url = self.get_url(from_lang, to_lang, query_text)
        try:
            # API HTTP请求
            httpClient = http.client.HTTPConnection(BASE_URL)
            httpClient.request('GET', url)
        
            #response是HTTPResponse对象
            response = httpClient.getresponse()
            result = json.loads(response.read())
            result_list = []
            for ret in result["trans_result"]:
                result_list.append(ret["dst"])
            trans_result = "".join(result_list)
            return trans_result 
        except:
            try:
                time.sleep(1)
                # API HTTP请求
                httpClient = http.client.HTTPConnection(BASE_URL)
                httpClient.request('GET', url)
            
                #response是HTTPResponse对象
                response = httpClient.getresponse()
                result = json.loads(response.read())
                result_list = []
                for ret in result["trans_result"]:
                    result_list.append(ret["dst"])
                trans_result = "".join(result_list)
                return trans_result 
            except Exception as e:
                print("[BAIDU API ERROR] Unable to translate due to API limitation!")
                print('[BAIDU API INFO]', result)
                traceback.print_exc()
            finally:
                if httpClient:
                    httpClient.close()

    @staticmethod
    def get_url(from_lang, to_lang, query_text):
        # 随机数据
        salt = random.randint(32768, 65536)
        # MD5生成签名
        sign = APP_ID + query_text + str(salt) + SECRET_KEY
        file_hash = hashlib.md5()
        file_hash.update(bytes(sign, 'utf-8'))
        sign = file_hash.hexdigest()
        # 拼接URL
        url = API_URL +'?appid=' + APP_ID + '&q=' + urllib.parse.quote(query_text) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(salt) + '&sign=' + sign
        return url


def test():
    # 译文语言，zh：中文，en：英文，不支持auto
    from_lang = "auto"
    to_lang = "zh"
    # 需要翻译的text
    query_text = "Today is fathers' day, when I went to school, I heard my classmates were discussing about what to buy for their fathers."
    translator = Translator()
    trans_result = translator.translate(from_lang, to_lang, query_text)
    print(trans_result)


if __name__ == "__main__":
    test()

