import json

#--------------------------------------------------------------
class JsonParser():
    """JSON Parser Class
       The argument given for class insantiation is a JSON file.
       The object provides variables to access the JSON data
       as a hash map.
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.json_data = self.initData()
        self.object_map = self.jsonMap()

    def initData(self):
        """Read file data and return the same."""
        file_stream =  open(self.file_name)
        return file_stream 

    def jsonMap(self):
        """Converts JSON data to hash map based. """
        return json.load(self.json_data)

    def jsonKeys(self):
        """Gives list of keys in hash map of JSON data """
        return self.object_map.keys()

    def objectValue(self, key):
        """For a key as argument returns the value in the hash map """
        return self.object_map[key]

    def isJson(self):
        try:
            json_object = json.load(self.json_data)
        except ValueError, e:
            return False
        return True
#-----------------------------------------------------------
			





