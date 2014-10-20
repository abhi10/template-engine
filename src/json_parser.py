import json

#--------------------------------------------------------------
class JsonParser():
    """JSON Parser Class """
    def __init__(self, file_name):
        self.file_name = file_name
        self.json_data = self.initData()
        self.object_map = self.jsonMap()

    def initData(self):
        file_stream =  open(self.file_name)
        return file_stream 

    def jsonMap(self):
        return json.load(self.json_data)

    def jsonKeys(self):
        return self.object_map.keys()

    def objectValue(self, key):
        return self.object_map[key]

    def isJson(self):
        try:
            json_object = json.load(self.json_data)
        except ValueError, e:
            return False
        return True
#-----------------------------------------------------------
			





