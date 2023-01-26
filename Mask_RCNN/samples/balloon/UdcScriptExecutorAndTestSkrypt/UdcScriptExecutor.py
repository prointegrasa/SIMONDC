import base64, json, sys
sys.path.append(r'C:\Users\mkrol\IdeaProjects\smartlink_server\Mask_RCNN\samples\balloon\UdcScriptExecutorAndTestSkrypt\udchttp')
sys.path.append(r'C:\Users\mkrol\IdeaProjects\smartlink_server\Mask_RCNN\samples\balloon\UdcScriptExecutorAndTestSkrypt')
from udchttp.UdcAuthorizator import UdcAuthorizator
from udchttp.UdcRequest import UdcRequest
from udchttp.UdcRestCall import UdcRestCall


class UdcScriptExecutorRequest(UdcRequest):
    def __init__(self, script, inputData=''):
        restCall = UdcRestCall('scriptExecutor')
        script = script.encode('ascii')
        data = {
            'Script'   : base64.b64encode(script).decode('utf-8'),
            'InputData': inputData
        }
        UdcRequest.__init__(self, "POST", restCall, jsonData=data)


class UdcScriptExecutorResult(object):
    def __init__(self, udcResponse):
        self.response = udcResponse

    def scriptOut(self):
        return self.response.scriptOut()

    def scriptErr(self):
        return self.response.scriptErr()

    def outputData(self):
        return self.response.JsonResponse['OutputData']

    def outputDataAsJson(self):
        return json.loads(self.outputData())

    def hasOutputData(self):
        if self.response.JsonResponse is None: return ''
        return 'OutputData' in self.response.JsonResponse

    def isSuccess(self):
        if self.hasOutputData():
            return self.outputDataAsJson()
        return False


class UdcScriptExecutor(object):
    def __init__(self, udcServer, udcUsername, udcPassword, isLdapLogin=False):
        self.udcServer = udcServer
        self.udcAuthorizator = UdcAuthorizator(udcServer, udcUsername, udcPassword, isLdapLogin)
        self.udcAuthorizator.connect()

    def __prepareRequest(self, script, inputData):
        udcRequest = UdcScriptExecutorRequest(script, inputData)
        self.udcAuthorizator.authorizeRequest(udcRequest)
        return udcRequest

    @staticmethod
    def __prepareRequestUsingKey(udcUserName, authorizationKey, script, inputData):
        udcRequest = UdcScriptExecutorRequest(script, inputData)
        return UdcAuthorizator.authorizeRequestUsingKey(udcUserName, authorizationKey, udcRequest)

    @staticmethod
    def __readScriptFromFile(scriptFileName):
        scriptFile = open(scriptFileName)
        script = ''.join(scriptFile.readlines())
        scriptFile.close()
        return script

    @staticmethod
    def getAuthorizationKey(udcServer, udcUserName, udcPassword, isLdapLogin=False):
        udcAuthorizator = UdcAuthorizator(udcServer, udcUserName, udcPassword, isLdapLogin)
        return udcAuthorizator.connect()

    @staticmethod
    def executeScriptFromFileUsingKey(udcServer, udcUserName, authorizationKey, scriptFileName, inputData='', queue=None, timeout=None):
        script = UdcScriptExecutor.__readScriptFromFile(scriptFileName)
        result = UdcScriptExecutor.executeScriptUsingKey(udcServer, udcUserName, authorizationKey, script, inputData, timeout)
        if queue: queue.put(result)
        return result

    @staticmethod
    def executeScriptUsingKey(udcServer, udcUserName, authorizationKey, script, inputData='', timeout=None):
        udcRequest = UdcScriptExecutor.__prepareRequestUsingKey(udcUserName, authorizationKey, script, inputData)
        udcResponse = udcRequest.trySend(udcServer, timeout)
        return UdcScriptExecutorResult(udcResponse)

    def executeScript(self, script, inputData='', timeout=None):
        udcRequest = self.__prepareRequest(script, inputData)
        udcResponse = udcRequest.trySend(self.udcServer, timeout)
        return UdcScriptExecutorResult(udcResponse)

    def executeScriptFromFile(self, scriptFileName, inputData='', queue=None, timeout=None):
        try:
            script = UdcScriptExecutor.__readScriptFromFile(scriptFileName)
            result = self.executeScript(script, inputData, timeout)
        except IOError:
            result = None
        if queue: queue.put(result)
        return result

    def outputData(self, udcResponse):
        if udcResponse.JsonResponse is not None and 'OutputData' in udcResponse.JsonResponse:
            return str(udcResponse.JsonResponse['OutputData'])
        return ''


if __name__ == '__main__':
    udcServer = sys.argv[1]
    udcUserName = sys.argv[2]
    udcPassword = sys.argv[3]
    scriptPath = sys.argv[4]
    scriptParameter = sys.argv[5]
    isLdap = sys.argv[6] if len(sys.argv) > 5 else 'false'

    """example of script execution using authorization key"""
    """
    print 'Authorization by key'
    authorizationKey = UdcScriptExecutor.getAuthorizationKey(udcServer, udcUserName, udcPassword)
    result = UdcScriptExecutor.executeScriptFromFileUsingKey(udcServer, udcUserName, authorizationKey, scriptPath, scriptParameter)
    """

    executor = UdcScriptExecutor(udcServer, udcUserName, udcPassword, isLdap == 'True')
    result = executor.executeScriptFromFile(scriptPath, scriptParameter)

    if not result.hasOutputData():
        print('Error occured while running script.')
        print('ScriptErr: ' + result.scriptErr())
        print('ScriptOut: ' + result.scriptOut())
    else:
        print(unicode(result.outputData()))

    sys.exit(0)
