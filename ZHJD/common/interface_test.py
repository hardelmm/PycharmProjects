import requests
import json


class InterfaceTest:

    def Post(self,url,param):
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        #headers = {"Content-Type": "application/json; charset=UTF-8"}
        response = requests.post(url, data=param, headers=headers).text
        r = json.loads(response)
        return r
