import attributesBaseObject as abo
import attributeTypes as at
import boidTools.uiBuilder as uib



###########################################
class FollowPathDataBlob(abo.DataBlobBaseObject):
    
    def __init__(self, agent):
        super(FollowPathDataBlob, self).__init__(agent)
        
        self.pathDevianceThreshold = 0.0
        self.goalDistanceThreshold = 0.0
        
#####################
    def __str__(self):
        return ("<FOLLOW-PATH BHVR: pathDev=%.2f, goalDist=%.2f>" % 
                (self.pathDevianceThreshold, self.goalDistanceThreshold))
        
# END OF CLASS - ClassicBoidDataBlob
###########################################



###########################################
class FollowPathBehaviourAttributes(abo.AttributesBaseObject):
    
    def __init__(self):
        super(FollowPathBehaviourAttributes, self).__init__()
        
        self._pathDevianceThreshold = at.FloatAttribute("Path Deviance Threshold", 3.0, self)
        self._pathDevianceThreshold_Random = at.RandomizerAttribute(self._pathDevianceThreshold)
        self._goalDistanceThreshold = at.FloatAttribute("Goal Distance Threshold", 1.0, self)
        self._goalDistanceThreshold_Random = at.RandomizerAttribute(self._goalDistanceThreshold)
        self._pathInfluenceMagnitude = at.FloatAttribute("Path Influence Magnitude", 0.75, minimumValue=0.0, maximumValue=1.0)
        self._startingTaper = at.FloatAttribute("Starting Taper", 0.5)
        self._endingTaper = at.FloatAttribute("Ending Taper", 2.0)

#####################         
    def sectionTitle(self):
        return "Follow Path Behaviour"
    
#####################
    def populateUiLayout(self):
        uib.MakeSliderGroup(self._pathDevianceThreshold)
        uib.MakeRandomizerGroup(self._pathDevianceThreshold_Random)
        uib.MakeSeparator()
        uib.MakeSliderGroup(self._goalDistanceThreshold)
        uib.MakeRandomizerGroup(self._goalDistanceThreshold_Random)
        uib.MakeSeparator()
        uib.MakeSliderGroup(self._pathInfluenceMagnitude)
        uib.MakeSeparator()
        uib.MakeSliderGroup(self._startingTaper)
        uib.MakeSliderGroup(self._endingTaper)
        
#####################
    def _createDataBlobForAgent(self, agent):
        return FollowPathDataBlob(agent)
    
#####################
    def _updateDataBlobWithAttribute(self, dataBlob, attribute):
        if(attribute is self._pathDevianceThreshold):
            dataBlob.pathDevianceThreshold = self._getPathDevianceThresholdForBlob(dataBlob)
        elif(attribute is self._goalDistanceThreshold):
            dataBlob.goalDistanceThreshold = self._getGoalDistanceThresholdForBlob(dataBlob)

#####################     
    def _getPathDevianceThresholdForBlob(self, dataBlob):
        return self._pathDevianceThreshold_Random.getRandomizedValueForIntegerId(dataBlob.agentId)
     
    def _getGoalDistanceThresholdForBlob(self, dataBlob):
        return self._goalDistanceThreshold_Random.getRandomizedValueForIntegerId(dataBlob.agentId)

#####################     
    def _getPathInfluenceMagnitude(self):
        return self._pathDevianceThreshold.value
    pathInfluenceMagnitude = property(_getPathInfluenceMagnitude)

#####################    
    def _getTaperStart(self):
        return self._startingTaper.value
    taperStart = property(_getTaperStart)
    
    def _getTaperEnd(self):
        return self._endingTaper.value
    taperEnd = property(_getTaperEnd)

    
# END OF CLASS
################################    