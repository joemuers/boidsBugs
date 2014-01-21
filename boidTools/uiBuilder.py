import boidAttributes.attributeTypes as at
import util

import pymel.core as pm
import sys
from boidAttributes.attributeTypes import LocationAttribute, MayaObjectAttribute




__LEFT_COLUMN_WIDTH__ = 190
__MIDDLE_COLUMN_WIDTH__ = 75
__RIGHT_COLUMN_WIDTH__ = 235
__FOURTH_COLUMN_WIDTH__ = 23

__OPTIONS_MENUS_WIDTH__ = 100



#################################################
#########           WINDOWS         #############
#################################################

def WindowExists(windowReference):
    return(windowReference is not None and pm.window(windowReference, exists=True))

#####################
def MakeWindow(title, widthHeight=None):
    if(widthHeight is None):
        return pm.window(title, menuBar=True)
    else:
        return pm.window(title, menuBar=True, widthHeight=widthHeight)

#####################
def DestroyWindow(windowReference):
    pm.deleteUI(windowReference, window=True)

#############################



#################################################
#########             MENUS         #############
#################################################

def SetParentMenuLayout(parentMenuLayout):
    if(not IsCurrentMenuParent(parentMenuLayout)):
        pm.setParent(parentMenuLayout, menu=True)

#####################        
def SetAsChildMenuLayout(*childLayouts):
    for _ in childLayouts:
        pm.setParent("..", menu=True)

#####################
def IsCurrentMenuParent(menuControl):
    return (menuControl == pm.currentMenuParent())

#####################
def MakeMenu(menuTitle):
    return pm.menu(menuTitle)
    
#####################    
def MakeMenuItem(itemLabel, onSelectCommand, annotation=None):
    newMenuItem = pm.menuItem(label=itemLabel)
    
    if(onSelectCommand is not None):
        newMenuItem.setCommand(onSelectCommand)
    if(annotation is not None):
        newMenuItem.setAnnotation(annotation)
    
    return newMenuItem

#####################
def MakeMenuItemWithSubMenu(itemLabel, annotation=None):
    newMenuItem = pm.menuItem(label=itemLabel, subMenu=True)
    if(annotation is not None):
        newMenuItem.setAnnotation(annotation)
    
    return newMenuItem

def MakeMenuSubItem(itemLabel):
    return pm.menuItem(label=itemLabel)

#####################
def MakeMenuSeparator():
    return pm.menuItem(divider=True)

#########################



#################################################
#########             LAYOUTS       #############
#################################################

def SetParentLayout(parentLayout):
    if(not IsCurrentParent(parentLayout)):
        pm.setParent(parentLayout)

#####################
def SetAsChildLayout(*childLayouts):
    for _ in childLayouts:
        pm.setParent("..")

#####################        
def IsCurrentParent(control):
    return (control == pm.currentParent())

##################### 
def MakeScrollLayout(title):
    if(title is not None):
        return pm.scrollLayout(title, childResizable=True)
    else:
        return pm.scrollLayout(childResizable=True)

#####################
def MakeBorderingLayout():
    return pm.frameLayout(labelVisible=False, borderStyle='etchedIn', marginWidth=2, marginHeight=3)

#####################
def MakeFrameLayout(title, makeCollapsable=True):
    frame = pm.frameLayout(title, borderStyle='out')
    if(makeCollapsable):
        frame.setCollapsable(True)
    return frame

#####################
def MakeTabLayout(height):
    tabs = pm.tabLayout(height=height)
    return tabs

##################### 
def MakeColumnLayout():
    return pm.columnLayout(adjustableColumn=True)

#####################    
def MakeRowLayout(numColumns, 
                  leftColumnWidth=__LEFT_COLUMN_WIDTH__, 
                  middleColumnWidth=__MIDDLE_COLUMN_WIDTH__, 
                  rightColumnWidth=__RIGHT_COLUMN_WIDTH__,
                  makeAdjustable=True):
    
    if(numColumns == 4):
        layout = pm.rowLayout(numberOfColumns=4, 
                              columnWidth4=(leftColumnWidth, middleColumnWidth, 
                                            rightColumnWidth - __FOURTH_COLUMN_WIDTH__, __FOURTH_COLUMN_WIDTH__), 
                              columnAlign=(1, 'right'), 
                              columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'right', 10)])
        if(makeAdjustable):
            layout.adjustableColumn(3)
        
        return layout
    if(numColumns == 3):
        layout = pm.rowLayout(numberOfColumns=3, 
                              columnWidth3=(leftColumnWidth, middleColumnWidth, rightColumnWidth), 
                              columnAlign=(1, 'right'), 
                              columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        if(makeAdjustable):
            layout.adjustableColumn(3)
        
        return layout
    elif(numColumns == 2):
        layout = pm.rowLayout(numberOfColumns=2, 
                              columnWidth2=(leftColumnWidth, rightColumnWidth), 
                              columnAlign=(1, 'right'), 
                              columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        if(makeAdjustable):
            layout.adjustableColumn(2)
            
        return layout
    elif(numColumns == 1):
        layout = pm.rowLayout(numberOfColumns=1, 
                              columnAlign=(1, 'left'), 
                              columnAttach=(1, 'left', leftColumnWidth))
        
        if(makeAdjustable):
            layout.adjustableColumn(1)
            
        return layout
    else:
        raise ValueError  
    
#########################
def MakeFormLayout():
    return pm.formLayout()

#########################
def DistributeControlsInFormLayout(formLayout, controls):
    formLayout.attachForm(controls[0], 'left', 2)

    numControls = len(controls)   
    stepSize = formLayout.getNumberOfDivisions() / numControls
    position = stepSize
    
    for i in range(numControls - 1):
        formLayout.attachPosition(controls[i], 'right', 1, position)
        formLayout.attachPosition(controls[i + 1], 'left', 1, position)
        position += stepSize
        
    formLayout.attachForm(controls[-1], 'right', 2)
        
#########################



#################################################
#########        INPUT FIELDS       #############
#################################################   
   
def MakeSliderGroup(attribute, annotation=None):
    isFloatField = None
    groupCreationMethod = None
    
    if(issubclass(type(attribute), at.FloatAttribute)):
        isFloatField = True
        groupCreationMethod = pm.floatSliderGrp
    elif(type(attribute) == at.IntAttribute):
        isFloatField = False
        groupCreationMethod = pm.intSliderGrp
    else:
        raise TypeError("Illegal attribute type for standard input field")
    
    
    kwargs = { "label" : attribute.attributeLabel, 
               "value": attribute.value, 
               "columnAlign" : (1, "right"),
               "columnAttach" : [(1, 'both', 0), (2, 'both', 0), (3, 'both', 10)], 
               "field" : True,
               "columnWidth3" : (__LEFT_COLUMN_WIDTH__, __MIDDLE_COLUMN_WIDTH__, __RIGHT_COLUMN_WIDTH__),
               "adjustableColumn" : 3,
               "minValue" : util.InitVal(attribute.minimumValue, 0)
               }

    if(isFloatField):
        kwargs["precision"] = 3

    if(attribute.maximumValue is not None):
        kwargs["maxValue"] = attribute.maximumValue
    else: # workaround for Pymel sliderGroup bug whereby 'fieldMaxValue' defaults to 100 if nothing specified
        kwargs["maxValue"] = attribute.value * 2
        kwargs["fieldMaxValue"] = float("inf") if(isFloatField) else sys.maxsize
    
    
    inputGroup = groupCreationMethod(**kwargs)
    inputGroup.changeCommand(lambda *args : attribute._setValue(inputGroup.getValue()))
    attribute.updateUiCommand = inputGroup.setValue
    attribute.uiEnableMethod = inputGroup.setEnable
    
    if(annotation is not None):
        inputGroup.setAnnotation(annotation)
    
    return inputGroup

#####################
def MakeFieldGroup(attribute, annotation=None):
    isFloatField = None
    groupCreationMethod = None
    
    if(issubclass(type(attribute), at.FloatAttribute)):
        isFloatField = True
        groupCreationMethod = pm.floatFieldGrp
    elif(type(attribute) == at.IntAttribute):
        isFloatField = False
        groupCreationMethod = pm.intFieldGrp
    else:
        raise TypeError("Illegal attribute type for standard input field. Got %s of type %s" % (attribute, type(attribute)))
    
    kwargs = { "label" : attribute.attributeLabel, 
               "value1": attribute.value, 
               "columnAlign" : (1, "right"),
               "columnWidth2" : (__LEFT_COLUMN_WIDTH__, __MIDDLE_COLUMN_WIDTH__)
               }
    # and another shitty Pymel bug - fieldGrps cannot have min/max values!!!
    if(isFloatField):
        kwargs["precision"] = 3

    inputGroup = groupCreationMethod(**kwargs)
    inputGroup.changeCommand(lambda *args : attribute._setValue(inputGroup.getValue1()))
    attribute.updateUiCommand = inputGroup.setValue1
    attribute.uiEnableMethod = inputGroup.setEnable
    
    if(annotation is not None):
        inputGroup.setAnnotation(annotation)
    
    return inputGroup

#####################
def MakeRandomizerGroup(randomizerAttribute, annotation=None):
    inputGroup = MakeSliderGroup(randomizerAttribute, annotation)
    
    return inputGroup
    
#####################
def MakeCheckboxGroup(attribute, extraLabel=None, annotation=None):
    if(type(attribute) != at.BoolAttribute):
        raise TypeError("Attempt to make checkbox group from non-boolean attribute.")
    
    rowLayout = MakeRowLayout(2 if(extraLabel is not None) else 1, rightColumnWidth=__MIDDLE_COLUMN_WIDTH__ + __RIGHT_COLUMN_WIDTH__)
    
    boxLabel = attribute.attributeLabel
    if(extraLabel is not None):
        MakeText(boxLabel + ':', annotation)
        boxLabel = extraLabel
    
    checkbox = pm.checkBox(label=boxLabel, value=attribute.value)
    checkbox.changeCommand(lambda *args: attribute._setValue(checkbox.getValue()))
    attribute.updateUiCommand = checkbox.setValue
    attribute.uiEnableMethod = checkbox.setEnable
    if(annotation is not None):
        checkbox.setAnnotation(annotation)
    
    SetAsChildLayout(rowLayout)
    
    return rowLayout

#####################
def MakeRandomizeOptionsMenu(randomizerController, annotation=None):
    if(type(randomizerController) != at.RandomizeController):
        raise TypeError("Attempt to make randomizer menu from non-randomizerController attribute.")
    
    rowLayout = MakeRowLayout(2, rightColumnWidth=__OPTIONS_MENUS_WIDTH__, makeAdjustable=False)
    
    MakeText(randomizerController.attributeLabel, annotation)
    
    optionMenu = pm.optionMenu()
    try:
        for i in xrange(sys.maxint):
            pm.menuItem(label=at.RandomizeController.StringForOption(i))
    except Exception:
        pass
    
    optionMenu.changeCommand(lambda *args: randomizerController._setValue(optionMenu.getValue()))
    randomizerController.updateUiCommand = optionMenu.setValue
    randomizerController.uiEnableMethod = optionMenu.setEnable
    if(annotation is not None):
        optionMenu.setAnnotation(annotation)
    
    SetAsChildLayout(rowLayout)
    
    return rowLayout

#####################
def MakeRandomizerFields(randomizerController, annotation=None):
    if(annotation is None):
        annotation = ("Input modes:\n\
Off = value taken directly from %s.\n\
By Agent ID = value offset by constant amount - which is randomized per-agent.\n\
Pure Random = value offset by random amount every time it is queried." 
% randomizerController._parentAttribute.attributeLabel)

    optionsMenuRowLayout = MakeRandomizeOptionsMenu(randomizerController, annotation)
    randomizerSliderGroup = MakeRandomizerGroup(randomizerController._randomizerAttribute, 
                                                ("Randomness multiplier for %s" % randomizerController.attributeLabel))
    randomizerController._updateInputUiComponents()
    
    return (optionsMenuRowLayout, randomizerSliderGroup)
    
#########################
def MakeStringOptionsField(stringAttribute, optionsListStrings, annotation=None):
    if(not isinstance(stringAttribute, at.StringAttribute)):
        raise TypeError("Attempted to make string options (expected:%s, got:%s)" % 
                        (at.StringAttribute, type(stringAttribute)))
    elif(stringAttribute.value not in optionsListStrings):
        raise ValueError("Initial value %s is not in options list." % stringAttribute.value)
    
    rowLayout = MakeRowLayout(2, rightColumnWidth=__OPTIONS_MENUS_WIDTH__ + 45, makeAdjustable=False)
    
    MakeText(stringAttribute.attributeLabel, annotation)
    
    optionMenu = pm.optionMenu()
    menuItemsList = []
    for option in optionsListStrings:
        menuItemsList.append(pm.menuItem(label=option))
    
    optionMenu.changeCommand(lambda *args: stringAttribute._setValue(optionMenu.getValue()))
    stringAttribute.updateUiCommand = optionMenu.setValue
    stringAttribute.uiEnableMethod = optionMenu.setEnable
    if(annotation is not None):
        optionMenu.setAnnotation(annotation)
    
    SetAsChildLayout(rowLayout)
    
    return (optionMenu, menuItemsList)
    
#########################
def MakeObjectSelectorField(objectAttribute, annotation=None):
    if(not isinstance(objectAttribute, at.MayaObjectAttribute)):
        raise TypeError("Attempted to make object selector (expected:%s, got:%s)" % 
                        (at.MayaObjectAttribute, type(objectAttribute)))
     
    rowLayout = MakeRowLayout(2)
     
    MakeText(objectAttribute.attributeLabel, annotation)
    
    nameField = pm.textFieldButtonGrp(editable=False, buttonLabel="...", 
                                      adjustableColumn=1, columnWidth2=(150, 50))
    if(annotation is not None):
        nameField.setAnnotation(annotation)
        
    objectAttribute.updateUiCommand = (lambda val: nameField.setText(val.name() if(val is not None) else "<None>"))
    objectAttribute._updateInputUiComponents()
    nameField.buttonCommand(lambda *args: _MakeObjectSelectionList(objectAttribute)) 

    SetAsChildLayout(rowLayout)
    
    return rowLayout

#########################
def _MakeObjectSelectionList(objectAttribute):
    objectAttribute._updateInputUiComponents()
    
    allowNone = objectAttribute.allowNoneType
    
    objectType = objectAttribute.objectType
    objectList = [None] if(allowNone) else []
    objectNamesList = ["<None>"] if(allowNone) else []
    
    objectList.extend(util.GetObjectsInSceneOfType(objectAttribute.objectType))
    objectNamesList.extend(map(lambda obj: obj.name(), objectList[1:] if(allowNone) else objectList))
    
    windowHandle = ("Select %s" % objectType.__name__)
    if(WindowExists(windowHandle)):
        DestroyWindow(windowHandle)

    window = pm.window(windowHandle)
    pm.paneLayout()
    
    def _onObjectSelect(objectAttribute, objectList, objectNamesList, objectMenu):
        index = objectNamesList.index(objectMenu.getSelectItem()[0])
        objectAttribute.value = objectList[index]
    
    objectMenu = pm.iconTextScrollList(allowMultiSelection=False, append=objectNamesList)

    if(objectAttribute.getRawAttribute() in objectList):
        objectMenu.setSelectItem(objectNamesList[objectList.index(objectAttribute.getRawAttribute())])
    
    objectMenu.selectCommand(lambda *args: _onObjectSelect(objectAttribute, objectList, objectNamesList, objectMenu))
    
    window.show()
    
#####################   
def MakeLocationField(locationAttribute, withButton=False, annotation=None):
    if(not isinstance(locationAttribute, at.LocationAttribute)):
        raise TypeError("Attempt to make location field with wrong type (expected:%s, got: %s)" % 
                        (at.LocationAttribute, type(locationAttribute)))
    
    if(not withButton):
        rowLayout = MakeRowLayout(2, rightColumnWidth=__MIDDLE_COLUMN_WIDTH__ + __RIGHT_COLUMN_WIDTH__)
    else:
        rowLayout = MakeRowLayout(3, middleColumnWidth=__RIGHT_COLUMN_WIDTH__, 
                                  rightColumnWidth=__FOURTH_COLUMN_WIDTH__, makeAdjustable=False)
        
    MakeText(locationAttribute.attributeLabel, annotation)
    
    locationField = pm.floatFieldGrp(numberOfFields=3, precision=3, columnWidth3=(__MIDDLE_COLUMN_WIDTH__, __MIDDLE_COLUMN_WIDTH__, __MIDDLE_COLUMN_WIDTH__),
                                     value1=locationAttribute.x, value2=locationAttribute.y, value3=locationAttribute.z)
    locationField.changeCommand(lambda *args: locationAttribute._setValue(locationField.getValue()))
    locationAttribute.updateUiCommand = (lambda *args: locationField.setValue((locationAttribute.x, locationAttribute.y, locationAttribute.z, 0.0)))
    locationAttribute.uiEnableMethod = locationField.setEnable
    if(annotation is not None):
        locationField.setAnnotation(annotation)
        
    if(withButton):
        button = pm.button(label="...", annotation=("Select/clear locator for %s" % LocationAttribute.attributeLabel), 
                           width=__FOURTH_COLUMN_WIDTH__)
        button.setCommand(lambda *args: _MakeObjectSelectionList(locationAttribute))
        
    SetAsChildLayout(rowLayout)
    
    return locationField

#########################
def MakePassiveTextField(stringAttribute, buttonCallback, annotation=None):
    if(not isinstance(stringAttribute, at.StringAttribute)):
        raise TypeError("Attempted to make text field (expected:%s, got:%s)" % 
                        (at.StringAttribute, type(stringAttribute)))
    
    rowLayout = MakeRowLayout(2)
    
    MakeText(stringAttribute.attributeLabel, annotation)

    textField = pm.textFieldButtonGrp(editable=False, text=stringAttribute.value,
                                      buttonLabel="...", buttonCommand=buttonCallback,
                                      adjustableColumn=1, columnWidth2=(130, __MIDDLE_COLUMN_WIDTH__))
    if(annotation is not None):
        textField.setAnnotation(annotation)
    
    stringAttribute.updateUiCommand = textField.setText
    stringAttribute.uiEnableMethod = textField.setEnableButton
    
    SetAsChildLayout(rowLayout)
    
    return rowLayout
    
    
#########################



#################################################
#########    MISCELLANEOUS ITEMS    #############
#################################################   

def MakeText(text, annotation=None):
    text = pm.text(text)
    if(annotation is not None):
        text.setAnnotation(annotation)
        
    return text

#####################
def MakeButton(text, callback, annotation=None):
    button = pm.button(label=text, command=callback)
    if(annotation is not None):
        button.setAnnotation(annotation)
        
    return button

#######################
def MakeButtonStandalone(label, callback, extraLabel=None, annotation=None):
    if(extraLabel is None):
        rowLayout = MakeRowLayout(1, makeAdjustable=False)
        button = MakeButton(label, callback, annotation)
        button.setWidth(__OPTIONS_MENUS_WIDTH__ - 10)
        
        SetAsChildLayout(rowLayout)
        
        return rowLayout
    else:
        rowLayout = MakeRowLayout(2, rightColumnWidth=__OPTIONS_MENUS_WIDTH__, makeAdjustable=False)
        MakeText(extraLabel, annotation)
        button = MakeButton(label, callback, annotation)
        button.setWidth(__OPTIONS_MENUS_WIDTH__ - 10)
        
        SetAsChildLayout(rowLayout)
        
        return rowLayout

#######################
def MakeButtonStrip(textCommandTupleList):
    formLayout = MakeFormLayout()
    controls = []
    
    for buttonTuple in textCommandTupleList:
        text = buttonTuple[0]
        command = buttonTuple[1]
        annotation = buttonTuple[2] if(len(buttonTuple) > 2) else None

        button = MakeButton(text, command, annotation)
        controls.append(button)
        
    DistributeControlsInFormLayout(formLayout, controls)
    SetAsChildLayout(formLayout)
    
    return formLayout

#####################
def MakeTextInputField(label, placeholderText=None, leftColumnWidth=__LEFT_COLUMN_WIDTH__, annotation=None):
    textField = pm.textFieldGrp(label=label, 
                                adjustableColumn=2, 
                                columnWidth=(1, leftColumnWidth),
                                columnAttach2=('both', 'both'),
                                columnOffset2=(0, 10))
    if(placeholderText is not None):
        textField.setText(placeholderText)
    if(annotation is not None):
        textField.setAnnotation(annotation)
        
    return textField

#####################
def MakeRadioButtonGroup(label, buttonTitlesTuple, onChangeCommand, 
                         leftColumnWidth=__LEFT_COLUMN_WIDTH__, annotation=None):
    numberOfButtons = len(buttonTitlesTuple)
    if(numberOfButtons < 1 or numberOfButtons > 4):
        raise ValueError("Attempt to create radioButtonGrp with %d buttons (expected 1-4)." % numberOfButtons)
    
    buttonKwargs = { "label" : label,
                     ("labelArray%d" % numberOfButtons) : buttonTitlesTuple,
                     "numberOfRadioButtons" : numberOfButtons,
                     "changeCommand" : onChangeCommand,
                     "columnAttach" : (2, "left", 10),
                     "select" : 1 }
    if(annotation is not None):
        buttonKwargs["annotation"] = annotation
    
    buttonGroup = pm.radioButtonGrp(**buttonKwargs)
    
    buttonGroup.columnWidth((1, leftColumnWidth))
    for index in xrange(numberOfButtons):
        buttonGroup.columnWidth((index + 2, 90))
    
    return buttonGroup

#####################
def MakeSeparator():
    return pm.separator(style='in')

#####################
def GetUserConfirmation(title, message):
    return pm.confirmBox(title, message, "OK", "Cancel")

#####################
def DisplayInfoBox(message, title=None):
    pm.informBox(title, message)

#####################
def DeleteComponent(uiComponent):
    pm.deleteUI(uiComponent)


####################################################################