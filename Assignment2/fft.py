"""
@author: Nazia Chowdhury, Yu An Lu
ECSE 316 Assignment 2
"""

# Import libraries
import matplotlib.colors as colors
import matplotlib.image as image
import matplotlib.pyplot as pyplot
import numpy as np
import argparse
import cv2

##################################################
#          Fourier Transform Functions           #
##################################################

def dft_1d(array):
    # DFT: Xk = sum (x_n * e^(-i2pikn/N) for k= 0 to N-1
    N = len(array)
    k = np.arange(N)

    # Copy original array
    copy = array.copy()

    # For each value in the array
    for n in range(N):
        array[n] = np.sum(copy * np.exp(-2j * np.pi * n * k / N))
    
    return array

def dft_2d(array):
    # DFT for 2D array
    # Rows and Columns
    N = array.shape[0]
    M = array.shape[1]
    
    # for each row n
    for n in range(N):
        array[n] = dft_1d(array[n])
        
    # for each column m
    for m in range(M):
        array[:,m] = dft_1d(array[:,m])
    
    return array

def fft_1d(array):
    # Divide & Conquer Colley-Tukey FFT Algorithm
    N = len(array)
    k = np.arange(N)

    # Base case
    if N <= 1:
        return array
    
    # Step case: 
    # Divide: split even and odd indices
    even = fft_1d(array[0::2])
    odd = fft_1d(array[1::2])

    constant = np.exp(-2j * np.pi * k / N)

    # Conquer: merge results
    return np.concatenate([even + constant[:int(N/2)] * odd, even - constant[int(N/2):] * odd])

def fft_2d(array):
    # FFT for 2D array
    # Rows and Columns
    N = array.shape[0]
    M = array.shape[1]
    
    # for each row n
    for n in range(N):
        array[n] = fft_1d(array[n])
        
    # for each column m
    for m in range(M):
        array[:,m] = fft_1d(array[:,m])
    
    return array

def inv_fft_1d(array):
    # Create a new array with the same dimensions as the original image
    fourierArray = np.zeros(array.shape, dtype=complex)
    
    # Iterate through each pixel of the image
    for x in range(array.shape[0]):
        # Iterate through each pixel of the image
        for u in range(array.shape[0]):
            # Calculate the Fourier Transform
            fourierArray[x] += array[u] * np.exp(2j * np.pi * (u * x / array.shape[0]))
    
    return fourierArray

def inv_fft_2d(array):
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
    # resize the image to have length or diwth that is a power of 2
    length = len(args.image[0])
    width = len(args.image)
    
    # resize length and width to a power of 2
    width = pow(2, (width - 1).bit_length())
    length = pow(2, (length - 1).bit_length())

    # get image array
    img = image.imread(args.image)

    # resize image & transform into array
    arr = np.asarray(cv2.resize(img, (length, width)), dtype=complex)
    
    if (args.mode == 1):
        fastmode(arr)
    elif (args.mode == 2):
        denoise(arr)
    elif (args.mode == 3):
        compress(arr)
    elif (args.mode == 4):
        runtime(arr)
    else:
        fastmode(arr)
     
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