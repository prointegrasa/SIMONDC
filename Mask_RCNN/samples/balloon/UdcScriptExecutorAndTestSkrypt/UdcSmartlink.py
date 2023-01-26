from udchttp.UdcAuthorizator import UdcAuthorizator
from udchttp.UdcRequest import UdcRequest
from udchttp.UdcRestCall import UdcRestCall


class UdcSmartlinkRequest(UdcRequest):
    def __init__(self, base64, data):
        restCall = UdcRestCall('scriptExecutor')
        data = {
            'Script'   : base64,
            'InputData': data
        }
        UdcRequest.__init__(self, "POST", restCall, jsonData=data)

class UdcSmartlink(object):
    def __init__(self, udcServer, udcUsername, udcPassword, isLdapLogin=False):
        self.udcServer = udcServer
        self.udcAuthorizator = UdcAuthorizator(udcServer, udcUsername, udcPassword, isLdapLogin)
        self.udcAuthorizator.connect()

    def __prepareRequest(self, base64, data):
        udcRequest = UdcSmartlinkRequest(base64, data)
        self.udcAuthorizator.authorizeRequest(udcRequest)
        return udcRequest

    @staticmethod
    def Send(self, base64, data, timeout=None):
        udcRequest = self.__prepareRequest(base64, data)
        udcResponse = udcRequest.trySend(self.udcServer, timeout)
        return udcResponse