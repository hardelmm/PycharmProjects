import requests
import json


class HttpUtils:
    @staticmethod
    def http_post(headers, url, parameters):
        print("接口请求url：" + url)
        print("接口请求headers：" + json.dumps(headers))
        print("接口请求parameters：" + json.dumps(parameters))
        res = requests.post(url, data=parameters, headers=headers)
        print("接口返回结果："+res.text)
        if res.status_code != 200:
            raise Exception(u"请求异常")
        result = json.loads(res.text)
        return result

    @staticmethod
    def http_get(headers, url):
        req_headers = json.dumps(headers)
        print("接口请求url：" + url)
        print("接口请求headers：" + req_headers)
        res = requests.get(url, headers=headers)
        print("接口返回结果：" + res.text)
        if res.status_code != 200:
            raise Exception(u"请求异常")
        result = json.loads(res.text)
        return result
