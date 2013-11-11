from boidBaseObject import BoidBaseObject

import random as rand
import math as mth


class Vector2(BoidBaseObject):
    """2D vector with various trig functions.
    Initial implementation of boid system used surface UV coordinates rather than 3D position, hence 
    this class.  However still comes in handy...
    
    Note that angle inputs/outputs, currently, are in degrees, NOT radians.
    """
    
    def __init__(self, u=0, v=0):
        """Note that you can either: 
        - pass in a vector object as an argument to create a (deep) copy
        - pass in numerical values for each axis
        - pass nothing for default values (0,0).
        """
        if(hasattr(u, "u")): # check if first argument is a Vector2/3 instance or not
            self._u = u.u
            self._v = u.v
        else:
            self._u = float(u)
            self._v = float(v)
        
        self._needsMagCalc = True
        self._magnitude = -1.0

####################### 
    def __str__(self):
        return "<u=%.4f, v=%.4f>" % (self.u, self.v)

##################### 
    def __add__(self, other):
        return Vector2(self.u + other.u, self.v + other.v)

    def __sub__(self, other):
        return Vector2(self.u - other.u, self.v - other.v)
   
    def __imul__(self, value):
        self.u *= value
        self.v *= value
        return self

    def __idiv__(self, value):
        self.u /= value
        self.v /= value
        return self

    def __eq__(self, other):
        return self.u == other.u and self.v == other.v

####################### 
    def _get_u(self):
        return self._u
    def _set_u(self, value):
        if(value != self._u):
            self._needsMagCalc = True
            self._u = value
    u = property(_get_u, _set_u)
    
    def _get_v(self):
        return self._v
    def _set_v(self, value):
        if(value != self._v):
            self._needsMagCalc = True
            self._v = value
    v = property(_get_v, _set_v)
    
#######################     
    def isNull(self):
        return (self._u == 0 and self._v == 0)

#######################         
    def reset(self, u = 0, v = 0):
        self.u = float(u)
        self.v = float(v)

####################### 
    def resetVec(self, otherVector):
        self.u = otherVector.u
        self.v = otherVector.v
        if(not otherVector._needsMagCalc and isinstance(otherVector, Vector2)):
            self._magnitude = otherVector._magnitude
            self._needsMagCalc = False

####################### 
    def invert(self):
        self._u = -(self._u) # magnitude won't change, so don't use accessor
        self._v = -(self._v) #
    
##################### 
    def inverseVector(self):
        return Vector2(-(self.u), -(self.v))

####################### 
    def magnitude(self, dummy=False): # dummy- so magnitude can be called interchangeably for Vector2/3. Very hacky, I know...
        if(self._needsMagCalc):
            self._magnitude = mth.sqrt((self._u **2) + (self._v **2))
            self._needsMagCalc = False and dummy # pseudo usage stops Eclipse complaining about unused argument
        return self._magnitude

####################### 
    def dot(self, otherVector):
        return (self.u * otherVector.u) + (self.v * otherVector.v)

#######################
    def normalise(self, scaleFactor = 1.0):
        if(not self.isNull()):
            multiple = scaleFactor / self.magnitude()
            self.u *= multiple
            self.v *= multiple

#######################
    def normalisedVector(self, scaleFactor = 1.0):
        retVal = Vector2(self.u, self.v)
        retVal.normalise(scaleFactor)
        return retVal

#######################
    def degreeHeading(self):
        zeroDegrees = Vector2(0, 1)
        return zeroDegrees.angleFrom(self)

####################### 
    def angleFrom(self, otherVector):
        """angle between direction vectors in DEGREES (negative for anti-clockwise)"""
        if(self.isNull() or otherVector.isNull()):
            return 0
        else:    
            temp = self.dot(otherVector) / (self.magnitude() * otherVector.magnitude())
            if(temp < -1): #this shouldn't be happening, but it does (rounding errors?) so...
                temp = -1
            elif(temp > 1):
                temp = 1
            
            angle = mth.degrees(mth.acos(temp))
            if(0 < angle and angle < 180):
                cross = (self.u * otherVector.v) - (self.v * otherVector.u)
                if(cross > 0):  # anti-clockwise
                    return -angle
                else: # clockwise
                    return angle
            else:
                return angle

#######################     
    def distanceFrom(self, otherVector):
        tempU = (self.u - otherVector.u) ** 2
        tempV = (self.v - otherVector.v) ** 2
        return mth.sqrt(tempU + tempV)

#######################
    def add(self, otherVector):
        self.u += otherVector.u
        self.v += otherVector.v

#######################                 
    def divide(self, scalarVal):
        self.u /= scalarVal
        self.v /= scalarVal

#######################  
    def rotate(self, angle):
        theta = mth.radians(-angle) #formula I'm using gives a reversed angle for some reason...??
        cosTheta = mth.cos(theta)
        sinTheta = mth.sin(theta)
        uTemp = self.u

        self.u = (self.u * cosTheta) - (self.v * sinTheta)
        self.v = (uTemp * sinTheta) + (self.v * cosTheta)

####################### 
    def moveTowards(self, toVector, byAmount):
        diffVec = toVector - self
        diffMag = diffVec.magnitude()

        if(diffMag < byAmount):
            self.resetVec(toVector)
        else:
            diffVec.normalise()
            diffVec *= byAmount
            self.u += diffVec.u
            self.v += diffVec.v

#######################                 
    def jitter(self, maxAmount):
        self.u += rand.uniform(-maxAmount, maxAmount)
        self.v += rand.uniform(-maxAmount, maxAmount)

################################################################################