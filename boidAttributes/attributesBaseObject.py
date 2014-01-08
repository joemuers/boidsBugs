import attributeTypes as at

import weakref



class AttributesListener(object):
    
    def onAttributeChanged(self, sectionObject, attributeName):
        raise NotImplemented

#END OF CLASS - AttributesListener
########################################



########################################
class DataBlobBaseObject(object):
    """Convenience class to provide common agentId accessor for dataBlob objects.
    """
    def __init__(self, agent):
        self._agentId = agent.particleId

#####################        
    def _getAgentId(self):
        return self._agentId
    agentId = property(_getAgentId)

#END OF CLASS - AttributesListener
########################################



########################################
class AttributesBaseObject(at.SingleAttributeDelegate):
    
    def __init__(self):
        self._dataBlobs = []
        self._listeners = []
        self._inBulkUpdate = False

#####################    
    def populateUiLayout(self):
        raise NotImplemented

#####################     
    def _createDataBlobForAgent(self, agent):
        raise NotImplemented
    
#     def _updateDataBlob(self, dataBlob):
#         raise NotImplemented
    
    def _updateDataBlobWithAttribute(self, dataBlob, attribute):
        raise NotImplemented
        
#####################        
    def getDefaultsFromConfigReader(self, configReader):
        self._inBulkUpdate = True
        
        print("Reading default values for section \"%s\"..." % self.sectionTitle())
        
        attributeLookup = {}
        for attributeName in dir(self):
            attribute = getattr(self, attributeName)
            if(issubclass(type(attribute), at._SingleAttributeBaseObject)):
                attributeLookup[attribute.attributeLabel] = attribute
        
        attributeReadCount = 0
        try:
            for attributeLabel, attributeValueStr in configReader.items(self.sectionTitle()):
                try:
                    attributeLookup[attributeLabel].value = attributeValueStr
                    attributeReadCount += 1
                except Exception as e:
                    print("WARNING - could not read attribute: %s (%s), ignoring..." % (attributeLabel, e))
                else:
                    print("Re-set attribute value: %s = %s" % (attributeLabel, attributeValueStr))
        except Exception as e:
            print("ERROR - %s" % e)
                
        self._inBulkUpdate = False
        
#         for blobRef in self._dataBlobs:
#             self._updateDataBlob(blobRef())
        self._notifyListeners(None)
        
        return (attributeReadCount > 0 and attributeReadCount == len(attributeLookup))

#####################    
    def setDefaultsToConfigWriter(self, configWriter):
        print("Saving default values for section \"%s\"..." % self.sectionTitle())
        
        try:
            if(configWriter.has_section(self.sectionTitle())):
                configWriter.remove_section(self.sectionTitle())
                print("Replacing previous values...")
            
            configWriter.add_section(self.sectionTitle())
        except Exception as e:
            print("ERROR - %s" % e)
        else:
            for attributeName in dir(self):
                attribute = getattr(self, attributeName)
                
                if(issubclass(type(attribute), at._SingleAttributeBaseObject)):
                    try:
                        configWriter.set(self.sectionTitle(), attribute.attributeLabel, attribute.value)
                        print("Changed default attribute value: %s = %s" % (attribute.attributeLabel, attribute.value))
                    except Exception as e:
                        print("WARNING - Could not write attribute to defaults file: %s (%s)" % (attributeName, e))

#####################    
    def sectionTitle(self):
        raise NotImplemented

#####################     
    def getNewDataBlobForAgent(self, agent):
        newBlob = self._createDataBlobForAgent(agent)
        
        for attributeName in dir(self):
            attribute = getattr(self, attributeName)
            if(issubclass(type(attribute), at._SingleAttributeBaseObject)):
                try:
                    self._updateDataBlobWithAttribute(newBlob, attribute)
                except Exception:
                    pass
                
        self._dataBlobs.append(weakref.ref(newBlob, self._removeDeadBlobReference))
        
        return newBlob

#####################               
    def _removeDeadBlobReference(self, deadReference):
        self._dataBlobs.remove(deadReference)

#####################    
    def addListener(self, listener):
        if(type(listener) != AttributesListener):
            raise TypeError
        else:
            self._listeners.append(weakref.ref(listener, self._removeDeadListenerReference))

#####################    
    def removeListener(self, listener):
        toRemove = None
        for listenerRef in self._listeners:
            if listenerRef() is listener:
                toRemove = listenerRef
                break
        self._listeners.remove(toRemove)    

#####################    
    def _removeDeadListenerReference(self, deadReference):
        self._listeners.remove(deadReference)

#####################        
    def _notifyListeners(self, changedAttributeName):
        if(not self._inBulkUpdate):
            for listenerRef in self._listeners:
                listenerRef().onAttributeChanged(self, changedAttributeName)

#####################            
    def _onAttributeChanged(self, changedAttribute): # overridden SingleAttributeDelegate method
#         if(not self._inBulkUpdate):
        for blobRef in self._dataBlobs:
            self._updateDataBlobWithAttribute(blobRef(), changedAttribute)
        
        self._notifyListeners(changedAttribute.attributeLabel)


# END OF CLASS
#############################