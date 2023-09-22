"""
@author: Yu An Lu, Nazia Chowdhury
ECSE 316 Assignment 1
"""

import sys

# Default values
timeout = 5
max_retries = 3
port = 53
serverType = 'A'
server = None
name = None

def dnsClient ():
    # Create UDP socket
    print("ToDo")

def parseInput ():
    # Parse user input
    # for loop to iterate through the arguments
    for i in range(len(sys.argv)):
        # Check for -t flag
        if sys.argv[i] == '-t':
            timeout = sys.argv[i+1]
        # Check for -r flag
        elif sys.argv[i] == '-r':
            max_retries = sys.argv[i+1]
        # Check for -p flag
        elif sys.argv[i] == '-p':
            port = sys.argv[i+1]
        # Check for -mx flag
        elif sys.argv[i] == '-mx':
            serverType = 'MX'
        # Check for -ns flag
        elif sys.argv[i] == '-ns':
            serverType = 'NS'
        # Check for @ flag
        elif '@' in sys.argv[i]:
            server = sys.argv[i]
        # Check for domain name
        else:
            name = sys.argv[i]

# Program entry point
if __name__ == "__main__":
    parseInput()
    dnsClient()