from prointegra.udc.backend.server.scripting.objects import UdcUtils
from prointegra.udc.backend.server.scripting import UdcProcedure

output_data = None
class sampleProcedure(UdcProcedure):
    def __init__(self):
        pass
    
    def Execute(self):
        global output_data
        output_data = 'dane wyjsciowe'

sampleProcedure().Execute()
