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
import time

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
    k = np.arange(N//2)
    constant = np.exp(-2j * np.pi * k / N)
    
    # Base case
    if N <= 16:
        return dft_1d(array)
    
    # Step case: 
    # Divide: split even and odd indices
    even = fft_1d(array[0::2])
    odd = fft_1d(array[1::2])

    # Conquer: merge results
    return np.concatenate([even + constant * odd, even - constant * odd])

def fft_2d(array):
    # FFT for 2D array
    # N Rows and M Columns
    N = len(array)
    M = len(array[0])
    
    for n in range(N):
        array[n] = fft_1d(array[n])
        
    # for each column m
    for m in range(M):
        array[:,m] = fft_1d(array[:,m])
    
    return array

def inv_dft_1d(array):
    # Naive Inverse DFT for 1D array
    N = len(array)
    k = np.arange(N)

    # Copy original array
    copy = array.copy()

    # For each value in the array
    for n in range(N):
        array[n] = np.sum(copy * np.exp(2j * np.pi * n * k / N))
    
    return array / N

def inv_fft_1d(array):
    # Divide & Conquer Colley-Tukey FFT Algorithm for inverse FFT
    N = len(array)
    k = np.arange(N)
    constant = np.exp(2j * np.pi * k / N)

    # Base case
    if N <= 16:
        return inv_dft_1d(array)
    
    # Step case: 
    # Divide: split even and odd indices
    even = inv_fft_1d(array[0::2])
    odd = inv_fft_1d(array[1::2])

    # Conquer: merge results
    return np.concatenate([even + constant[:int(N / 2)] * odd, even + constant[int(N / 2):] * odd])

def inv_fft_2d(array):
    # FFT for 2D array
    # Rows and Columns
    N = len(array)
    M = len(array[0])
    
    # for each row n
    for n in range(N):
        array[n] = inv_fft_1d(array[n])
        
    # for each column m
    for m in range(M):
        array[:,m] = inv_fft_1d(array[:,m])
    
    return array

##################################################
#                  Processing                    #
##################################################

def main(args):
    # resize the image to have length or width that is a power of 2
    img = image.imread(args.image)
    
    length = len(img[0])
    width = len(img)
    
    # resize length and width to a power of 2
    width = 1 if width == 0 else pow(2, (width - 1).bit_length()) 
    length = 1 if length == 0 else pow(2, (length - 1).bit_length())

    # resize image & transform into array
    new_img = cv2.resize(img, (length, width))
    arr = np.asarray(new_img, dtype=complex)
    
    if (args.mode == 1):
        fastmode(arr, new_img)
    elif (args.mode == 2):
        denoise(arr, new_img)
    elif (args.mode == 3):
        compress(arr, new_img)
    elif (args.mode == 4):
        runtime()
    else:
        print("Invalid mode")
     
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

def fastmode(args, img):
    # Perform FFT
    fft_img = fft_2d(args)
    # fft_img = np.fft.fft2(args) # numpy's FFT function for comparison
    
    # Plot the results
    pyplot.figure("Mode 1")
    pyplot.subplot(1, 2, 1)
    pyplot.imshow(img, cmap="gray")
    pyplot.title("Original Image")
    pyplot.subplot(1, 2, 2)
    pyplot.imshow(np.abs(fft_img), norm=colors.LogNorm())
    pyplot.title("FFT Image")
    pyplot.colorbar()
    pyplot.show() 
    
    print("Fast mode")
    
def denoise(arr, img, version=4):
    print("Denoise mode")
    # Output one by two subplot with original image and denoised image
    # Denoise: Apply FFT, apply procedures, and then apply an inverse FFT
    # Low frequency: ~0, ~2pi
    # High frequency: ~pi
    # Print # & fraction of non-zeros in the FFT image
    count = len(arr)*len(arr[0])
    non_zeros = 0

    # Apply FFT on array
    fft_img = fft_2d(arr)

    if version == 1:
        # Truncate low frequencies
        # Set all values of the 0.001th percentile of the FFT image to 0
        lower_bound = np.percentile(fft_img, 0.001)
        upper_bound = np.percentile(fft_img, 99.999)
        fft_img = np.where((fft_img <= lower_bound) | (fft_img >= upper_bound), 0, fft_img)
        non_zeros = np.count_nonzero(fft_img)

    elif version == 2:
        # Truncate high frequencies
        # Set all values of the 95th percentile of the FFT image to 0
        lower_bound = np.percentile(fft_img, 5)
        upper_bound = np.percentile(fft_img, 95)
        fft_img = np.where((fft_img >= lower_bound) & (fft_img <= upper_bound), 0, fft_img)
        non_zeros = np.count_nonzero(fft_img)

    elif version == 3:  
        # Threshold low frequencies 
        # Set all values of the 0.001th percentile of the FFT image to 0.5 * np.pi
        threshold = 0.5 * np.pi
        lower_bound = np.percentile(fft_img, 0.001)
        upper_bound = np.percentile(fft_img, 99.999)
        fft_img = np.where((fft_img <= lower_bound) | (fft_img >= upper_bound), threshold, fft_img)
        non_zeros = np.count_nonzero(fft_img)
    
    elif version == 4:
        # Threshold high frequencies
        # Set all values of the 95th percentile of the FFT image to 0.5 * np.pi
        threshold = 0.5 * np.pi
        lower_bound = np.percentile(fft_img, 10)
        upper_bound = np.percentile(fft_img, 90)
        fft_img = np.where((fft_img >= lower_bound) & (fft_img <= upper_bound), threshold, fft_img)
        non_zeros = np.count_nonzero(fft_img)
    
    elif version == 5:
        # Threshold everything to 0.5 * np.pi
        # Set all values of the FFT image to 0.5 * np.pi
        threshold = 0.5 * np.pi
        fft_img = np.full_like(fft_img, threshold, dtype=complex)
        non_zeros = np.count_nonzero(fft_img)

    # Apply inverse FFT
    denoised_img = inv_fft_2d(fft_img).real

    # Print # & fraction of non-zeros to the command line
    print("##################################################")
    print("Number of non-zeros in FFT: " + str(non_zeros))
    print("Fraction of non-zeros in FFT: " + str(non_zeros / count))
    print("##################################################")

    # Plot the results
    pyplot.figure("Mode 2")
    pyplot.subplot(1, 2, 1)
    pyplot.imshow(img, cmap="gray")
    pyplot.title("Original Image")
    pyplot.subplot(1, 2, 2)
    pyplot.imshow(denoised_img, cmap="gray")
    pyplot.title("Denoised Image")

    pyplot.show()
    
def compress(args, img):
    ftt_img = fft_2d(args)
    compession = [0, 25, 50, 75, 95]
    images = []
    
    for i in range(5):
        complement = 100 - compession[i] # Get the remaining of the compression
        lower_bound = np.percentile(ftt_img, complement//2) # Get the lower bound
        upper_bound = np.percentile(ftt_img, 100 - complement//2) # Get the upper bound
        transformed = ftt_img * np.logical_or(ftt_img <= lower_bound, ftt_img >= upper_bound) # Apply the compression
        images.append(inv_fft_2d(transformed).real) # Inverse FFT and get the real part of the image
    
    # Plot the results
    pyplot.figure("Mode 3")
    pyplot.subplot(2,3,1), pyplot.imshow(img, cmap = 'gray'), pyplot.title("Original Image")
    
    for i in range(1, 6):
         pyplot.subplot(2,3,i+1), pyplot.imshow(images[i-1], cmap = 'gray')
         pyplot.title("Compression: " + str(compession[i-1]) + "%")
         count = len(images[i-1])*len(images[i-1][0])
         non_zeros = count * ((100 - compession[i-1]) / 100)
         print("Compression at " + str(compession[i-1]) + "% has non zeros as: " + str(non_zeros) + " out of " + str(count))

    pyplot.show()
    print("Compress mode")
    
def runtime():
    print("Runtime mode")
    # Create 2D arrays of random elements of various sizes (square and powers of 2)
    # Start from 2^5 and move up to 2^10 or up to the size that computer can handle
    sizes = [32, 64, 128, 256, 512, 1024]
    avgs_dft = []
    stds_dft = []
    avgs_fft = []
    stds_fft = []

    # Repeat the experiment 10 times for each size
    for i in range(len(sizes)):
        runtime_dft = 0
        runtime_fft = 0

        # Generate 2D square array of random elements of size sizes[i]
        array = np.random.rand(sizes[i], sizes[i])

        # Run DFT and FFT on each array 10 times
        for j in range(10):
            # Record runtime for each run
            start = time.time()
            dft_2d(array)
            end = time.time()
            runtime_dft += end - start

            start = time.time()
            fft_2d(array)
            end = time.time()
            runtime_fft += end - start
        
        # Obtain average runtime and standard deviation for each size
        avgs_dft.append(np.mean(runtime_dft))
        stds_dft.append(np.std(runtime_dft))
        avgs_fft.append(np.mean(runtime_fft))
        stds_fft.append(np.std(runtime_fft))    

    # Gather data for the plot by re-running the experiment 10 times for each size
    # Obtain average runtime and standard deviation for each size
    # Plot the average runtime (seconds) (y-axis) against the size of the array (x-axis)
    # Two lines: one for DFT and one for FFT
    # Include error bars for standard deviation that represent confidence interval of 95%

    # Plot DFT & FFT on same graph
    pyplot.title("DFT Runtime")
    pyplot.xlabel("Array Size")
    pyplot.ylabel("Runtime (s)")
    pyplot.errorbar(sizes, avgs_dft, yerr=2*stds_dft, fmt='o', color='blue', label="naive DFT")
    pyplot.errorbar(sizes, avgs_fft, yerr=2*stds_fft, fmt='o', color='red', label="FFT")
    pyplot.legend(["naive DFT", "FFT"])
    pyplot.show()

# Program entry point
if __name__ == "__main__":
    main(parseInput())