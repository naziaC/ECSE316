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
    # Naive DFT for 1D array
    # Formula: Xk = sum (x_n * e^(-i2pikn/N) for k= 0 to N-1
    N = len(array)
    k = np.arange(N)

    # Copy original array
    copy = array.copy()

    # For each value in the array
    for n in range(N):
        array[n] = np.sum(copy * np.exp(-2j * np.pi * n * k / N))
    
    return array

def dft_2d(array):
    # Naive DFT for 2D array
    # N Rows and M Columns
    N = len(array)
    M = len(array[0])
    
    # for each row n
    for n in range(N):
        array[n] = dft_1d(array[n])
        
    # for each column m
    for m in range(M):
        array[:,m] = dft_1d(array[:,m])
    
    return array

def fft_1d(array):
    # FFT for 1D array
    N = len(array)
    k = np.arange(N)
    constant = np.exp(-2j * np.pi * k / N)

    # Base case
    if N <= 1:
        return array
    
    # Step case: 
    # Divide: split even and odd indices
    even = fft_1d(array[0::2])
    odd = fft_1d(array[1::2])

    # Conquer: merge results
    return np.concatenate([even + constant[:int(N/2)] * odd, even - constant[int(N/2):] * odd])

def fft_2d(array):
    # FFT for 2D array
    # N Rows and M Columns
    N = len(array)
    M = len(array[0])
    
    # for each row n
    for n in range(N):
        array[n] = fft_1d(array[n])
        
    # for each column m
    for m in range(M):
        array[:,m] = fft_1d(array[:,m])
    
    return array

def inv_fft_1d(array):
    # Divide & Conquer Colley-Tukey FFT Algorithm for inverse FFT
    N = len(array)
    k = np.arange(N)
    constant = np.exp(2j * np.pi * k / N)

    # Base case
    if N <= 1:
        return array
    
    # Step case: 
    # Divide: split even and odd indices
    even = inv_fft_1d(array[0::2])
    odd = inv_fft_1d(array[1::2])

    # Conquer: merge results
    return np.concatenate([even + constant[:int(N/2)] * odd, even - constant[int(N/2):] * odd]) / N

def inv_fft_2d(array):
    # FFT for 2D array
    # Rows and Columns
    N = array.shape[0]
    M = array.shape[1]
    
    # for each row n
    for n in range(N):
        array[n] = inv_fft_2d(array[n])
        
    # for each column m
    for m in range(M):
        array[:,m] = inv_fft_2d(array[:,m])
    
    return array

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