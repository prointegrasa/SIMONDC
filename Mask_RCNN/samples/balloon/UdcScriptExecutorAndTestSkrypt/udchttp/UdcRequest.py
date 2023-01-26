from datetime import datetime
import requests, hashlib, base64
from UdcRestCall import UdcRestCall, UdcGuiRestCall
from UdcResponse import UdcResponse

class UdcRequest(object):
    
    def __init__(self, method, restCall, headers=[], textData=None, jsonData=None, jsonDataList=None):
        assert method.upper() in ['GET', 'DELETE', 'POST', 'PUT']
        #assert isinstance(restCall, UdcRestCall)
        self.method = method.upper()
        self.restCall = restCall
        self.headers = headers if isinstance(headers, dict) else {}
        self.data = textData if textData is not None else json.dumps(jsonData) if jsonData is not None else ''
        self.date = datetime.now().strftime("%a, %d %b %Y %X GMT") #datetime.now().strftime("%c")
        
        self.dataList = ['']
        if jsonDataList is not None:
            for jsonData in jsonDataList:
                self.dataList.append(json.dumps(jsonData) if jsonData is not None else '')

    def defaultHeaders(self):
        return {
            "Accept": "*/*",
            "Accept-Language": "pl-PL",
            "Accept-Encoding": "identity",
            "UdcDate" : self.date
        }
        
    def allHeaders(self):
        headers = self.defaultHeaders()
        if (self.data is not None) and (len(self.data) > 0):
            headers["Content-MD5"] = self.contentMd5()
            headers["Content-Type"] = "application/json"
        headers.update(self.headers)
        return headers
        
    def addCustomHeader(self, key, value):
        self.headers[key] = value

    def send(self, udcServer = '', _timeout = None):
        url = self.restCall.toUrl(udcServer)
        requests.packages.urllib3.disable_warnings()
        response = requests.request(self.method, url, headers=self.allHeaders(), data=self.data, timeout=_timeout, verify=False)
        response.raise_for_status()
        return response
    
    def trySend(self, udcServer = '', timeout = None):
        try:
            url = self.restCall.toUrl(udcServer)
            requests.packages.urllib3.disable_warnings()
            response = requests.request(self.method, url, headers=self.allHeaders(), data=self.data, timeout=(None,timeout), verify=False)
            return UdcResponse(response)
        except requests.exceptions.ReadTimeout:
            return UdcResponse(None)
        except :
            raise
    
    def contentMd5(self):
        if self.data is None or len(self.data) == 0:
            return ''
        md5 = hashlib.md5()
        md5.update(self.data.encode('utf-8'))
        return base64.b64encode(md5.digest()).decode("ascii")

import unittest, json

class TestUdcRequest(unittest.TestCase):
    def setUp(self):
        self.restCall = UdcGuiRestCall('execute')
    
    def test_contentMd5(self):
        request = UdcRequest('GET', self.restCall)
        self.assertEqual('', request.contentMd5())

if __name__ == '__main__':
    unittest.main()