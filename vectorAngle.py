import math
import vectorMagnitude

#calculate angle theta
def getTheta(y_raw, x_raw):
    
    temp= (y_raw / x_raw)+180
    
    theta = math.atan(temp)
    
    return theta

#calculate angle phi
def getPhi(x_raw, y_raw,z_raw):
    
    vectorMag = vectorMagnitude.getVectorMagnitude(x_raw,y_raw,z_raw) #get the vector manitude
    
    
    temp = (z_raw/vectorMag)
    
    temp = math.acos(temp) * (180/math.pi) + 180 # convert randian to degrees then add 180
    
    temp = temp * (math.pi/180) #convert degrees to radian return temp
    
    return temp

