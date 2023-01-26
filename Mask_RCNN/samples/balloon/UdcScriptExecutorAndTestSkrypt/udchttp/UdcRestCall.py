
class UdcRestCall(object):

    def __init__(self, restCall):
        self.restCall = self.parseRestCall(restCall)
    
    def withPrefix(self):
        return self.restPrefix() + self.restCall
    
    def withoutPrefix(self):
        return self.restCall
    
    def toUrl(self, udcServer):
        return self.parseServerAddress(udcServer) + self.withPrefix()
    
    def restPrefix(self):
        return '/rest'
    
    def parseServerAddress(self, udcServer):
        udcServer = udcServer.strip().rstrip('/') 
        if not udcServer.startswith('http://') and not udcServer.startswith('https://'):
            udcServer = 'http://' + udcServer
        if not udcServer.endswith('/udc'):
            udcServer += '/udc'
        return udcServer
    
    def parseRestCall(self, restCall):
        while restCall.startswith('/'):
            restCall = restCall[1:]
        if restCall.startswith('rest/'):
            restCall = restCall[5:]
        return '/' + restCall
    
    def __repr__(self): return self.restCall
    def __str__(self): return self.restCall
    
class UdcGuiRestCall(UdcRestCall):
    def __init__(self, restCall):
        UdcRestCall.__init__(self, restCall)
        
    def restPrefix(self):
        return '/rest/gui'
    
    def parseRestCall(self, restCall):
        restCall = UdcRestCall.parseRestCall(self, restCall)
        if restCall.startswith('/gui/'):
            return restCall[4:]
        return restCall
    

import unittest

class TestUdcRestCall(unittest.TestCase):
    def test_parseServerAddress(self):
        restCall = UdcRestCall('')
        self.assertEqual('http://localhost:8080/udc', restCall.parseServerAddress('http://localhost:8080/udc'))
        self.assertEqual('http://localhost:8080/udc', restCall.parseServerAddress('localhost:8080'))
        self.assertEqual('http://localhost:8080/udc', restCall.parseServerAddress('localhost:8080/udc/'))

    def test_parseRestCall(self):
        restCall = UdcRestCall('')
        self.assertEqual('/', restCall.parseRestCall(''))
        self.assertEqual('/execute', restCall.parseRestCall('/execute'))
        self.assertEqual('/execute', restCall.parseRestCall('execute'))
        self.assertEqual('/gui/execute', restCall.parseRestCall('/rest/gui/execute'))
        self.assertEqual('/gui/execute', restCall.parseRestCall('gui/execute'))
        
    def test_restPrefix(self):
        restCall = UdcRestCall('')
        self.assertEqual('/rest', restCall.restPrefix())
        
    def test_toUrl(self):
        restCall = UdcRestCall('')
        self.assertEqual('http://localhost:8080/udc/rest/', restCall.toUrl('http://localhost:8080/udc'))
        
        restCall = UdcRestCall('/execute')
        self.assertEqual('http://localhost:8080/udc/rest/execute', restCall.toUrl('localhost:8080'))
    
    
class TestUdcGuiRestCall(TestUdcRestCall):
    def test_parseServerAddress(self):
        restCall = UdcRestCall('')
        self.assertEqual('http://localhost:8080/udc', restCall.parseServerAddress('http://localhost:8080/udc'))
        self.assertEqual('http://localhost:8080/udc', restCall.parseServerAddress('localhost:8080'))
        self.assertEqual('http://localhost:8080/udc', restCall.parseServerAddress('localhost:8080/udc/'))

    def test_parseRestCall(self):
        restCall = UdcGuiRestCall('')
        self.assertEqual('/', restCall.parseRestCall(''))
        self.assertEqual('/execute', restCall.parseRestCall('/execute'))
        self.assertEqual('/execute', restCall.parseRestCall('execute'))
        self.assertEqual('/execute', restCall.parseRestCall('/rest/gui/execute'))
        self.assertEqual('/execute', restCall.parseRestCall('gui/execute'))
        
    def test_restPrefix(self):
        restCall = UdcGuiRestCall('')
        self.assertEqual('/rest/gui', restCall.restPrefix())
        
    def test_toUrl(self):
        restCall = UdcGuiRestCall('')
        self.assertEqual('http://localhost:8080/udc/rest/gui/', restCall.toUrl('http://localhost:8080/udc'))
        
        restCall = UdcGuiRestCall('/execute')
        self.assertEqual('http://localhost:8080/udc/rest/gui/execute', restCall.toUrl('localhost:8080'))
        
        restCall = UdcGuiRestCall('/rest/gui/user/credentialLogin')
        self.assertEqual('http://localhost:8080/udc/rest/gui/user/credentialLogin', restCall.toUrl('localhost:8080'))
    
    
if __name__ == '__main__':
    unittest.main()