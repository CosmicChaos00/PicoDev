import math

class VectorMagnitude:
    def __init__(self, x_raw, y_raw, z_raw):
        self.x_raw = x_raw
        self.y_raw = y_raw
        self.z_raw = z_raw
    
    def getVectorMagnitude(self):
        total = (self.x_raw ** 2) + (self.y_raw ** 2) + (self.z_raw ** 2)
        return math.sqrt(total)
    
    def checkVectMag(self):
        if self.getVectorMagnitude() >= 5:
            return True
        else:
            return False
        
    def getTheta(self):
        # Calculate the angle in the x-y plane from the positive x-axis
        theta = math.atan2agar(self.y_raw, self.x_raw)  # atan2 automatically handles the division by zero
        return theta

    def getPhi(self):
        # Calculate the angle from the positive z-axis
        vectorMag = self.getVectorMagnitude()  # Get the vector magnitude
        if vectorMag == 0:
            return 0  # Avoid division by zero if the vector is zero
        temp = self.z_raw / vectorMag
        phi = math.acos(temp)  # acos returns the angle in radians
        return phi

