import base64, json
import urllib

class UdcResponse(object):

    def __init__(self, httpResponse):
        self.HttpResponse = httpResponse
        try:
            self.JsonResponse = json.loads(httpResponse.text)
        except:
            self.JsonResponse = None
            
    def scriptErr(self):
        scriptErr = ''
        if self.JsonResponse is not None:
            if 'RepositoryMessage' in self.JsonResponse:
                if 'ScriptErr' in self.JsonResponse['RepositoryMessage']:
                    scriptErr = base64.b64decode(self.JsonResponse['RepositoryMessage']['ScriptErr'])
        return scriptErr
    
    def scriptOut(self):
        scriptErr = ''
        if self.JsonResponse is not None:
            if 'RepositoryMessage' in self.JsonResponse:
                if 'ScriptOut' in self.JsonResponse['RepositoryMessage']:
                    scriptErr = base64.b64decode(self.JsonResponse['RepositoryMessage']['ScriptOut'])
        return scriptErr
            
    def duration(self):
        return self.HttpResponse.elapsed.total_seconds() * 1000.0
        
    def message(self):
        text = []
        codeAndReasonFormat = "%s: %s"
        try:
            text.append(self.readResponseAsJson())
        except ValueError:
            if len(self.HttpResponse.text) > 0:
                text.append("Raw response: " + self.HttpResponse.text)
        if not self.isSuccess():
            if 400 <= self.HttpResponse.status_code < 500:
                codeAndReasonFormat = '%s Client Error: %s'
            elif 500 <= self.HttpResponse.status_code < 600:
                codeAndReasonFormat = '%s Server Error: %s'
            else:
                codeAndReasonFormat = '%s: %s'
#         else:
#             text.append(self.HttpResponse.text)
        text.insert(0, codeAndReasonFormat % (self.HttpResponse.status_code, self.HttpResponse.reason))
        return '\n'.join(text)
    
    def errorMessage(self):
        if self.isSuccess():
            return ''
        text = []
        codeAndReasonFormat = "%s: %s"
        try:
            text.append(self.readResponseAsJson())
        except ValueError:
            if len(self.HttpResponse.text) > 0:
                text.append("Raw response: " + self.HttpResponse.text)
        if 400 <= self.HttpResponse.status_code < 500:
            codeAndReasonFormat = '%s Client Error: %s'
        elif 500 <= self.HttpResponse.status_code < 600:
            codeAndReasonFormat = '%s Server Error: %s'
        else:
            codeAndReasonFormat = '%s: %s'
        text.insert(0, codeAndReasonFormat % (self.HttpResponse.status_code, self.HttpResponse.reason))
        return '\n'.join(text)
        
    def readResponseAsJson(self):
        text = []
        scriptErr = ''
        errorMessage = ''
        jsonResponse = json.loads(self.HttpResponse.text)
        if 'RepositoryMessage' in jsonResponse:
            if 'ScriptErr' in jsonResponse['RepositoryMessage']:
                jsonResponse['RepositoryMessage']['ScriptErr'] = base64.b64decode(jsonResponse['RepositoryMessage']['ScriptErr'])
            if 'ScriptOut' in jsonResponse['RepositoryMessage']:
                jsonResponse['RepositoryMessage']['ScriptOut'] = base64.b64decode(jsonResponse['RepositoryMessage']['ScriptOut'])
            scriptErr = jsonResponse['RepositoryMessage']['ScriptErr']
        if 'Content' in jsonResponse:
            content = jsonResponse['Content']
            if content.startswith('/GridView?presentationData='):
                content = content[len('/GridView?presentationData='):]
                content = base64.b64decode(urllib.unquote(content))
            jsonResponse['Content'] = content
        text.append(json.dumps(jsonResponse, indent=4, separators=(',', ': ')))
        return '\n'.join(text)
        if 'errorMessage' in jsonResponse:
            errorMessage = jsonResponse['errorMessage']
        if not scriptErr and (not errorMessage or errorMessage.lower() == 'null'):
            text.append("Error details may be lost (either not received or not sent).")
        else:
            if scriptErr:
                text.append("ScriptErr:\n" + base64.b64decode(scriptErr))
            if errorMessage and errorMessage.lower() != 'null':
                text.append("errorMessage: " + errorMessage)
        return '\n'.join(text)
        
    def isSuccess(self):
        if self.HttpResponse is None:
            return False
        if 400 <= self.HttpResponse.status_code < 500:
            return False
        elif 500 <= self.HttpResponse.status_code < 600:
            return False
        return True
