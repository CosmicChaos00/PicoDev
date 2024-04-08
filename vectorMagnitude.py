import math
#calculate the total Deceleration
def getVectorMagnitude(x_raw,y_raw,z_raw):
    total= (x_raw*x_raw) + (y_raw*y_raw) + (z_raw*z_raw)
    
    return math.sqrt(total)

