'''
Created on 13 lip 2015

@author: trzepka
'''
import json
from UdcRequest import UdcRequest
from UdcRestCall import UdcRestCall, UdcGuiRestCall

class UdcCredentialLoginRequest(UdcRequest):
    def __init__(self, udcUsername, udcPassword, isLdapLogin = False):
        restCall = UdcGuiRestCall('/user/credentialLogin')
        data = {
            "UserName" : udcUsername,
            "Password" : udcPassword,
            "IsLdapLogin" : isLdapLogin
        }
        UdcRequest.__init__(self, "POST", restCall, jsonData=data)

class UdcCustomProceduresRequest(UdcRequest):
    def __init__(self, udcLocationUri):
        restCall = UdcGuiRestCall(udcLocationUri + '/customProcedures')
        UdcRequest.__init__(self, "GET", restCall, '')
        
class UdcInvokeProcedureRequest(UdcRequest):
    def __init__(self, udcProcedureUri):
        restCall = UdcGuiRestCall(udcProcedureUri + '/invoke')
        UdcRequest.__init__(self, "GET", restCall, '')
        

if __name__ == '__main__':
    pass