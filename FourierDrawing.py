import Vector
import Graphics
import numpy as np
from math import floor

def distance(point1, point2):
    return np.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def parse_command_line():
    """Parses the command line arguments.

    ### Returns
    - `str`
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The SVG file to draw")
    args = parser.parse_args()
    return args.filename

#read svg file
def read_svg(filename):
    """Reads an SVG file and returns a list of the data.

    ### Parameters
    - filename: `str`

    ### Returns
    - `list` of `str`
    """
    with open(filename, "r") as f:
        data = f.read()
    data.find("d=\"")
    data = data[data.find("d=\"")+3:]
    data = data[:data.find("\"")]
    data = data.split(" ")
    return data
    
def parse_svg(data):
    """Parses the SVG data and returns a list of points.
    
    ### Parameters
    - data: `list` of `str`

    ### Returns
    - `list` of `tuple` of `float`
    """
    curve = []
    
    lastPointX = 0
    lastPointY = 0
    for i in range(len(data)):
        if data[i] == "M":
            lastPointX = float(data[i+1])
            lastPointY = float(data[i+2])
            curve.append((lastPointX, lastPointY))
            i += 3
        elif data[i] == "L":
            dist = distance((lastPointX, lastPointY), (float(data[i+1]), float(data[i+2])))
            step = 1/dist if dist > 0 else 1
            j = 0
            while j < 1:
                curve.append((lastPointX + (float(data[i+1]) - lastPointX) * j, lastPointY + (float(data[i+2]) - lastPointY) * j))
                j += step
            lastPointX = float(data[i+1])
            lastPointY = float(data[i+2])
            i += 3
        elif data[i] == "C":
            dist = distance((lastPointX, lastPointY), (float(data[i+5]), float(data[i+6])))
            step = 1/dist if dist > 0 else 1
            j = 0
            while j < 1:
                curve.append((lastPointX + (float(data[i+5]) - lastPointX) * j, lastPointY + (float(data[i+6]) - lastPointY) * j))
                j += step
            lastPointX = float(data[i+5])
            lastPointY = float(data[i+6])
            i += 7
    
    return curve

def fourier_phasors(curve, n=61):
    """Returns the first n phasors of the Fourier series of the curve.

    ### Parameters
    - curve: `list` of `tuple` of `float`
    - n: `int`

    ### Returns
    - `list` of `complex`
    """
    phasors = []
    for i in range(n):
        phasors.append(0)
    for i in range(len(curve)):
        for j in range(len(phasors)):
            #curve[j] transformed to complex number
            phasors[j] += (curve[i][0] + curve[i][1] * 1j) * np.exp(-2j * np.pi * i * (j-len(phasors)//2) / len(curve))
    return phasors

def main():
    # Initialize graphics
    graphics = Graphics.Graphics(800, 600)

    # Parse command line
    filename = parse_command_line()

    # Read svg file
    # I used https://boxy-svg.com/app to draw some svg files
    data = read_svg(filename)

    # Get curve from data
    curve = parse_svg(data)

    # Numerically integrate the curve times e^(-i*2*pi*t)	
    phasors = fourier_phasors(curve, 31)

    # Create and set the vectors
    tipList = []
    vectorList = []
    velocityDictionary = {}
    for i in range(0, len(phasors)):
        vectorList.append(Vector.Vector(phasors[i].real, phasors[i].imag))
        vectorList[i].scale(1/len(curve)) #scale - you may have to adjust it to fit the screen
        velocityDictionary[id(vectorList[i])] = i-floor(len(phasors)/2)
    
    vectorList.sort(reverse=True)

    # Main loop
    while not graphics.update():

        graphics.refresh()

        # Draw the curve
        for point in curve:
            graphics.draw_point(point[0], point[1])

        # Tip of the sum of the vectors
        tip = Vector.Vector()

        # Rotate the vectors
        for i in range(len(vectorList)):
            vectorList[i].rotate(2*np.pi* velocityDictionary[id(vectorList[i])] / 60 / 10) #slowed rotation down by 10 to better see the curve
            tip += vectorList[i]

        tipList.append((tip.x, tip.y))

        # Render the trail and vectors
        for tip in tipList:
            xReference, yReference = (0, 0)
            graphics.draw_point(tip[0] + xReference, tip[1] + yReference, (255, 0, 0))
        graphics.render(vectorList)

        # Maintain only the last 1000 points
        if len(tipList) > 1000:
            tipList.pop(0)

if __name__ == "__main__":
    main()