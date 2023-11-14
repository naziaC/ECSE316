"""
@author: Nazia Chowdhury, Yu An Lu
ECSE 316 Assignment 1
"""

# Import libraries
import matplotlib.colors as colors
import matplotlib.image as image
import matplotlib.pyplot as pyplot
import numpy as np
import argparse

##################################################
#          Fourier Transform Functions           #
##################################################

def naive1DFourierTransform(array):
    # For 1d Array
    if (len(array.shape) == 1):
        # Create a new array with the same dimensions as the original image
        fourierArray = np.zeros(array.shape, dtype=complex)
        
        # Iterate through each pixel of the image
        for u in range(array.shape[0]):
            # Iterate through each pixel of the image
            for x in range(array.shape[0]):
                # Calculate the Fourier Transform
                fourierArray[u] += array[x] * np.exp(-2j * np.pi * (u * x / array.shape[0]))
        
        return fourierArray
    
def inverseNaive1DFourierTransform(array):
    # Create a new array with the same dimensions as the original image
    fourierArray = np.zeros(array.shape, dtype=complex)
    
    # Iterate through each pixel of the image
    for x in range(array.shape[0]):
        # Iterate through each pixel of the image
        for u in range(array.shape[0]):
            # Calculate the Fourier Transform
            fourierArray[x] += array[u] * np.exp(2j * np.pi * (u * x / array.shape[0]))
    
    return fourierArray

def naive2DFourierTransform(array):
    # Create a new array with the same dimensions as the original image
    fourierArray = np.zeros(array.shape, dtype=complex)
    
    # Iterate through each pixel of the image
    for u in range(array.shape[0]):
        for v in range(array.shape[1]):
            # Iterate through each pixel of the image
            for x in range(array.shape[0]):
                for y in range(array.shape[1]):
                    # Calculate the Fourier Transform
                    fourierArray[u][v] += array[x][y] * np.exp(-2j * np.pi * ((u * x / array.shape[0]) + (v * y / array.shape[1])))
    
    return fourierArray

def inverseNaive2DFourierTransform(array):
    # Create a new array with the same dimensions as the original image
    fourierArray = np.zeros(array.shape, dtype=complex)
    
    # Iterate through each pixel of the image
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            # Iterate through each pixel of the image
            for u in range(array.shape[0]):
                for v in range(array.shape[1]):
                    # Calculate the Fourier Transform
                    fourierArray[x][y] += array[u][v] * np.exp(2j * np.pi * ((u * x / array.shape[0]) + (v * y / array.shape[1])))
    
    return fourierArray

def fast1DFourierTransform(array):
    # For 1d Array
    if (len(array.shape) == 1):
        # Create a new array with the same dimensions as the original image
        fourierArray = np.zeros(array.shape, dtype=complex)
        
        # Iterate through each pixel of the image
        for u in range(array.shape[0]):
            # Iterate through each pixel of the image
            for x in range(array.shape[0]):
                # Calculate the Fourier Transform
                fourierArray[u] += array[x] * np.exp(-2j * np.pi * (u * x / array.shape[0]))
        
        return fourierArray
    
def inverseFast1DFourierTransform(array):
    # Create a new array with the same dimensions as the original image
    fourierArray = np.zeros(array.shape, dtype=complex)
    
    # Iterate through each pixel of the image
    for x in range(array.shape[0]):
        # Iterate through each pixel of the image
        for u in range(array.shape[0]):
            # Calculate the Fourier Transform
            fourierArray[x] += array[u] * np.exp(2j * np.pi * (u * x / array.shape[0]))
    
    return fourierArray

def fast2DFourierTransform(array):
    # Create a new array with the same dimensions as the original image
    fourierArray = np.zeros(array.shape, dtype=complex)
    
    # Iterate through each pixel of the image
    for u in range(array.shape[0]):
        for v in range(array.shape[1]):
            # Iterate through each pixel of the image
            for x in range(array.shape[0]):
                for y in range(array.shape[1]):
                    # Calculate the Fourier Transform
                    fourierArray[u][v] += array[x][y] * np.exp(-2j * np.pi * ((u * x / array.shape[0]) + (v * y / array.shape[1])))
    
    return fourierArray

def inverseFast2DFourierTransform(array):
    # Create a new array with the same dimensions as the original image
    fourierArray = np.zeros(array.shape, dtype=complex)
    
    # Iterate through each pixel of the image
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            # Iterate through each pixel of the image
            for u in range(array.shape[0]):
                for v in range(array.shape[1]):
                    # Calculate the Fourier Transform
                    fourierArray[x][y] += array[u][v] * np.exp(2j * np.pi * ((u * x / array.shape[0]) + (v * y / array.shape[1])))
    
    return fourierArray

##################################################
#                  Processing                    #
##################################################

def main(args):
    arr = image.imread(args.image)
    
    if (args.mode == 1):
        fastmode(arr)
    elif (args.mode == 2):
        denoise(arr)
    elif (args.mode == 3):
        compress(arr)
    elif (args.mode == 4):
        runtime(arr)
    else:
        fastmode(args)
     
def parseInput():
    # Parse user input
    parser = argparse.ArgumentParser(description="FFT Argument Parser")
    
    parser.add_argument('-m', '--mode', type=int, default=1, help="""
        [1] (Default) for fast mode where the image is converted into its FFT form and displayed;
        [2] for denoising where the image is denoised by applying an FFT, truncating high;
        frequencies and then displayed; 
        [3] for compressing and plot the image;
        [4] for plotting the runtime graphs for the report
        """) 
    parser.add_argument('-i', '--image', type=str, default="moonlanding.png", help="""
        Filename of the image we wish to take the DFT of
        """)
    
    return parser.parse_args()

def fastmode(args):
    print("Fast mode")
    
    
    
def denoise(args):
    print("Denoise mode")
    
def compress(args):
    print("Compress mode")
    
def runtime(args):
    print("Runtime mode")


# Program entry point
if __name__ == "__main__":
    main(parseInput())