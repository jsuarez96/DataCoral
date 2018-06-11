import json
import os

class JSONParser():

    def handleSingle(self, object):
        if len(object) == 1:
            key = object.keys()[0]
            del object[key]['index']

    def createFolder(self):
        if not os.path.exists('created'):
            os.makedirs('created')

    def convertToJSON(self, name, object, jsonFile):
        if name is None:
            filename = 'created/' + jsonFile
        else:
            filename = 'created/' + name + '.json'
        result = []
        self.handleSingle(object)
        for key in object:
            result.append(object[key])
        self.createFolder()
        with open(filename, 'w') as outfile:
            json.dump(result, outfile)

    def createDicts(self, value):
        objects = {}
        for tup in value:
            index, value, objectID, parentID = tup[0],tup[1],tup[2],tup[3]
            key = (index,objectID,parentID)
            if key in objects:
                dict = objects[key]
                dict[value[0]] = value[1]
            else:
                objects[key] = {value[0]: value[1],'index': index,'id': objectID,'p_id': parentID}
        return objects

    def getNewAttribute(self, prev_attribute, attribute):
        new_attribute = None
        if prev_attribute is not None:
            new_attribute = prev_attribute + '_' + attribute
        else:
            new_attribute = attribute
        return new_attribute

    def flattenJSON(self, object, current_attribute, prev_attribute, index, id, parent_id, jsonObjects):
        if type(object) == list:
            for i in range(len(object)):
                element = object[i]
                self.flattenJSON(element,current_attribute,prev_attribute,i,id,parent_id,jsonObjects)
        elif type(object) == dict:
            if 'id' in object:
                parent_id = id
                id = object['id']
            for attribute in object:
                parent_attribute = self.getNewAttribute(prev_attribute, current_attribute)
                self.flattenJSON(object[attribute],attribute,parent_attribute,index,id,parent_id,jsonObjects)
        else:
            key = (prev_attribute)
            value = (current_attribute,object)
            if key not in jsonObjects:
                jsonObjects[key] = [(index, value, id, parent_id)]
            else:
                jsonObjects[key].append((index, value, id, parent_id))

    def parse(self, jsonFile):
        with open(jsonFile) as json_data:
            object = json.load(json_data)
            jsonObjects = {}
            self.flattenJSON(object,None,None,0,None,None,jsonObjects)
            for objectName in jsonObjects:
                objects = self.createDicts(jsonObjects[objectName])
                self.convertToJSON(objectName,objects,jsonFile)

# Example Usage:
# Create Object
parser = JSONParser()
# Parse a JSON file
parser.parse('sample.json')
# Results will be in 'Created' directory
