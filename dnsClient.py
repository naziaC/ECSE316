"""
@author: Yu An Lu, Nazia Chowdhury
ECSE 316 Assignment 1
"""

# Import libraries
import argparse
import socket
import binascii
import random

def dnsClient (args):
    # Create UDP socket
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Connect to the web server
    print('Connecting to server...\n' + createQuery(args))

    # [TODO: send query to server]
    # udpSocket.sendto(createQuery(args).encode('utf-8'), (args.server, args.port))

def parseInput ():
    # Parse user input
    parser = argparse.ArgumentParser(description="DNS Client Argument Parser")
    
    parser.add_argument('-t', '--timeout', type=int, default=5, help="""
        Timeout value: How long to wait, in seconds, before retransmitting an unanswered query. Default value: 5
        """) 
    parser.add_argument('-r', '--max_retries', type=int, default=3, help="""
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
    
    return parser.parse_args()
    
def createQuery(args):
    header = createHeader()
    question = createQuestion(args)
    return header + question

def createHeader():
    # Create randomized 16-bit number for ID
    id = str(bin(random.randint(0, 65535))).replace('0b', '').zfill(16)
    # QR = 0
    qr = '0'
    # OPCODE = 0
    opcode = '0000'
    # AA = 0 (not meaningful in query)
    aa = '0'
    # TC = 0 (not meaningful in query)
    tc = '0'
    # RD = 1
    rd = '1'
    # RA = 0 (not meaningful in query)
    ra = '0'
    # Z = 0
    z = '000'
    # RCODE = 0 (not meaningful in query)
    rc = '0000'
    # QDCOUNT = 1
    qdcount = '0000000000000001'
    # ANCOUNT = 0 (not meaningful in query)
    ancount = '0000000000000000'
    # NSCOUNT = 0 (not meaningful in query)
    nscount = '0000000000000000'
    # ARCOUNT = 0 (not meaningful in query)
    arcount = '0000000000000000'

    # concatenate all the header fields
    header = id + qr + opcode + aa + tc + rd + ra + z + rc + qdcount + ancount + nscount + arcount

    # transform header from binary to hex
    header = hex(int(header, 2)).replace('0x', '').zfill(4)

    print('header: ' + header)
    return header

def createQuestion(args):
    print('domain name: ' + args.name)
    # QNAME = domain name [TODO: check if this is correct]
    args_arr = args.name.split('.')
    qname = ''
    for i in range(len(args_arr)):
        # convert to 8-bit unsigned integer binary representation
        print('args_arr[' + str(i) + ']: ' + args_arr[i])
        qname += str(hex(int(len(args_arr[i]))).replace('0x', '').zfill(2))
        print('qname: ' + qname)
        for j in range(len(args_arr[i])):
            print('args_arr[' + str(i) + '][' + str(j) + ']: ' + args_arr[i][j])
            qname += str((hex(int(binascii.hexlify(args_arr[i][j].encode('utf-8')), 16)).replace('0x', '')).zfill(2))
    qname += '00'

    print('qname: ' + qname)

    # QTYPE = 1 (A)
    if (args.mx):
        qtype = '000f'
    elif (args.ns):
        qtype = '0002'
    else:
        qtype = '0001'
    # QCLASS = 1
    qclass = '0001'

    # concatenate all the question fields
    question = qname + qtype + qclass

    print('question: ' + question)
    return question

# Program entry point
if __name__ == "__main__":
    dnsClient(parseInput())