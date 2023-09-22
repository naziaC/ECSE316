"""
@author: Yu An Lu, Nazia Chowdhury
ECSE 316 Assignment 1
"""

# Import libraries
import argparse
import socket

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
    # todo - fix parser
    parser = argparse.ArgumentParser(description="DNS Client Argument Parser")
    
    parser.add_argument('-t', '--timeout', type=int, default=5, help="""
        Timeout value: How long to wait, in seconds, before retransmitting an unanswered query. Default value: 5
        """) 
    parser.add_argument('-r', '--max-retries', type=int, default=3, help="""
        Maximum number of retries: Maximum number of times to retransmit an unanswered query before giving up. Default value: 3
        """)
    parser.add_argument('-p', '--port', type=int, default=53, help="""
        Port number: UDP port number ofthe DNS server. Default value: 53
        """)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-mx', '--mx', action='store_true', help="""
        MX flag: indicate whether to send a MX (mail server) or NS (name server) query.
        At most one ofthese can be given, and if neither is given then the client should send a type A (IP address) query.
        """)
    group.add_argument('-ns', '--ns', action='store_true', help="""
        NS flag: indicate whether to send a MX (mail server) or NS (name server) query.
        At most one ofthese can be given, and if neither is given then the client should send a type A (IP address) query.
        """)
    parser.add_argument('server', type=str, help="Server: IPv4 address of the DNS server, in a.b.c.d.format")
    parser.add_argument('name', type=str, help="Domain name to query for")
    
    arguments = parser.parse_args()
    
    timeout = arguments.timeout
    max_retries = arguments.max_retries
    port = arguments.port
    server = arguments.server
    name = arguments.name
    if arguments.mx:
        serverType = 'MX'
        # Check for -ns flag
    elif arguments.ns:
        serverType = 'NS'
    server = arguments.server
    name = arguments.name
    

# Program entry point
if __name__ == "__main__":
    parseInput()
    dnsClient()