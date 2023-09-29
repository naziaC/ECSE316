"""
@author: Yu An Lu, Nazia Chowdhury
ECSE 316 Assignment 1
"""

# Import libraries
import argparse
import socket
import binascii
import random
import time

header = None
domain_name = None
question = None
query = None
qtype = None
answer = None
t_start = None
t_end = None

def dnsClient (args):
    # Create UDP socket
    global answer, query, qtype, t_start, t_end
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.settimeout(args.timeout)
    t_start = time.time()
    n_retries = 0
    
    print('DnsClient sending request for: ' + args.name + '\n')
    print('Server: ' + args.server[1:] + '\n')
    if (args.mx):
        qtype_string = 'MX'
    elif (args.ns):
        qtype_string = 'NS'
    else:
        qtype_string = 'A'
    print('Request type: ' + qtype_string + '\n')
    
    # Send query to server for max number of retries
    for i in range(args.max_retries):
        print('Sending query to server...')
        try:
            # Send query to server
            createQuery(args)
            udpSocket.sendto(bytes.fromhex(query), (args.server[1:], args.port))
            # Receive response from server
            answer = udpSocket.recvfrom(1024)
            t_end = time.time()
            break
        except socket.timeout:
            print('ERROR \t [Timeout event -  Resending query to server...]')
            n_retries = n_retries + 1
            continue

    if answer == None or len(answer) == 0:
        print('ERROR \t [Maximum number of retries reached - Exiting program]')
        return
    else:
        print("Answer: " + str(answer) + '\n')
        answer_hex = binascii.hexlify(answer[0]).decode('utf-8')
        print(answer_hex)
        
        print('Response received after [' + str(t_end - t_start) + '] seconds' + '([' + str(n_retries) + '] retries)')
        parseResponse(answer_hex)
    
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
    global header, question, query
    createHeader()
    createQuestion(args)

    query = header + question
    print('DNS Request Message: ' + query)

def createHeader():
    global header

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

def createQuestion(args):
    global domain_name, qtype, query, question
    # QNAME = domain name [TODO: check if this is correct]
    args_arr = args.name.split('.')
    qname = ''
    for i in range(len(args_arr)):
        # convert to 8-bit unsigned integer hex representation
        qname += str(hex(int(len(args_arr[i]))).replace('0x', '').zfill(2))
        for j in range(len(args_arr[i])):
            qname += str((hex(int(binascii.hexlify(args_arr[i][j].encode('utf-8')), 16)).replace('0x', '')).zfill(2))
    domain_name = qname
    qname += '00'

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

def parseResponse (answer_hex):
    global header, question, query, qtype, t_start, t_end
    print("***Answer Section ([num-answers] records)*** \n")
    
    # get id from query header
    query_id = header[0:4]
    
    # get id from answer header
    answer_id = answer_hex[0:4]
    
    # check if id from query header matches id from answer header
    if (query_id != answer_id):
        print('ERROR \t [ID in response does not match ID in query]')
        return
    
    answer_header = answer_hex[0:24]
    answer_question = answer_hex[24:len(question) + 24]
    
    print('Answer Header: ' + answer_header)
    print('Query Header: ' + header)
    print('Answer Question: ' + answer_question)
    print('Query Question: ' + question)
    
    rcode = answer_header[7:8]
    qdcount = answer_header[8:12]
    ancount = answer_header[12:16]
    nscount = answer_header[16:20]
    arcount = answer_header[20:24]
    
    print ('RCODE: ' + rcode)
    print ('QDCOUNT: ' + qdcount)
    print ('ANCOUNT: ' + ancount)
    print ('NSCOUNT: ' + nscount)
    print ('ARCOUNT: ' + arcount)    
    # # Check if RCODE is 0
    # if rcode != '0000':
    #     print('ERROR \t [RCODE is not 0]')
    #     return
    # # Check if ANCOUNT is 0
    # elif ancount == '0000':
    #     print('ERROR \t [ANCOUNT is 0]')
    #     return
    # # Check if NSCOUNT is 0
    # elif nscount != '0000':
    #     print('ERROR \t [NSCOUNT is not 0]')
    #     return
    # # Check if ARCOUNT is 0
    # elif arcount != '0000':
    #     print('ERROR \t [ARCOUNT is not 0]')
    #     return
    # else:
    #     print('Response received after [' + str(t_end - t_start) + '] seconds')

# Program entry point
if __name__ == "__main__":
    dnsClient(parseInput())