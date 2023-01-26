import json, hashlib, hmac, base64
from PredefinedUdcRequests import UdcCredentialLoginRequest
from UdcRestCall import UdcRestCall

class UdcAuthorizator(object):
    def __init__(self, udcServer, userName, password, isLdapLogin = False):
        self.UdcServer = udcServer
        self.UserName = userName
        self.Password = password
        self.IsLdapLogin = isLdapLogin
        self.Key = None
        
    def isConnected(self):
        return False if self.Key is None else True

    def connect(self):
        loginRequest = UdcCredentialLoginRequest(self.UserName, self.Password, self.IsLdapLogin)
        response = loginRequest.send(self.UdcServer)
        token = json.loads(response.text)["Token"]
        if token is None or token == '':
            self.Key = None
            return self.Key
        self.Key = base64.b64decode(token)
        return self.Key
    
    @staticmethod
    def authorizeRequestUsingKey(userName, authorizationKey, udcRequest):
        stringToSign = UdcAuthorizator.__prepareStringToSign(udcRequest)
        udcAuthorization = "SIGNED_REQ " + userName + ":" + UdcAuthorizator.__sign(authorizationKey, stringToSign)
        udcRequest.addCustomHeader("Authorization", udcAuthorization)
        udcRequest.addCustomHeader("UdcAuthorization", udcAuthorization)
        return udcRequest
    
    def authorizeRequest(self, udcRequest):
        return UdcAuthorizator.authorizeRequestUsingKey(self.UserName, self.Key, udcRequest)
    
    @staticmethod
    def __prepareStringToSign(udcRequest):
        contentMd5 = udcRequest.contentMd5()
        contentType = "application/json"
        udcDate = udcRequest.date
        restCallString = UdcAuthorizator.__prepareRestCallString(udcRequest)
        stringToSign = udcRequest.method + "\n" 
        if udcRequest.method in ['POST', 'PUT']:
            stringToSign += contentMd5 + "\n" + contentType + "\n"
        stringToSign += udcDate + "\n" + restCallString
        return stringToSign
    
    @staticmethod
    def __prepareRestCallString(udcRequest):
        restCall = UdcRestCall(udcRequest.restCall.withPrefix()).withoutPrefix() 
        return restCall.lower()
    
    @staticmethod
    def __sign(authorizationKey, text):
        hashed = hmac.new(authorizationKey, text.encode('utf-8'), hashlib.sha1)
        return base64.b64encode(hashed.digest()).decode("ascii")
