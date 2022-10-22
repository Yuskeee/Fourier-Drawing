import numpy as np

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    
    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __length(self):
        """
        Get the length of the vector.

        ### Returns:
        - `float`
        """

        return np.sqrt(self.x**2 + self.y**2)

    def __le__(self, other):
        return self.__length() <= other.__length()

    def __ge__(self, other):
        return self.__length() >= other.__length()

    def __lt__(self, other):
        return self.__length() < other.__length()
    
    def __gt__(self, other):
        return self.__length() > other.__length()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def scale(self, factor):
        """
        Scale the vector by the given factor.

        ### Args:
        - factor: the factor to scale the vector by
        
        ### Returns:
        - None
        """

        self.x *= factor
        self.y *= factor
    
    def rotate(self, angle):
        """
        Rotate the vector by the given angle counterclockwise.

        ### Args:
        - angle: in radians
        
        ### Returns:
        - None
        """

        # Rotate the vector counterclockwise by the given angle using the rotation matrix
        # [cos(angle) -sin(angle)]
        # [sin(angle)  cos(angle)]
        # however as the y axis is inverted, the rotation matrix is
        # [cos(angle)  sin(angle)]
        # [-sin(angle) cos(angle)]
        x = self.x
        y = self.y
        self.x = x * np.cos(angle) + y * np.sin(angle)
        self.y = -x * np.sin(angle) + y * np.cos(angle)
