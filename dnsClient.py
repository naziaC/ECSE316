"""
@author: Yu An Lu, Nazia Chowdhury
ECSE 316 Assignment 1
"""

# python3 dnsClient.py @132.206.85.18 www.mcgill.ca
# python3 dnsClient.py -t 10 -r 2 -mx @8.8.8.8 mcgill.ca

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
response = None
t_start = None
t_end = None
response_answer_index = None

def dnsClient (args):
    # Create UDP socket
    global response, query, qtype, t_start, t_end
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
            response = udpSocket.recvfrom(1024)
            t_end = time.time()
            break
        except socket.timeout:
            print('ERROR \t [Timeout event -  Resending query to server...]')
            n_retries = n_retries + 1
            continue

    if response == None or len(response) == 0:
        print('ERROR \t [Maximum number of retries reached - Exiting program]')
        return
    else:
        print("Answer: " + str(response) + '\n')
        response = binascii.hexlify(response[0]).decode('utf-8')
        print(response)
        
        print('Response received after [' + str(t_end - t_start) + '] seconds' + '([' + str(n_retries) + '] retries)')
        parseResponse()
    
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

def parseResponse ():
    global header, question, query, qtype, t_start, t_end, response, response_answer_index
    print("***Answer Section ([num-answers] records)*** \n")
    
    # check if id from query header matches id from answer header
    query_id = header[0:4]
    response_id = response[0:4]

    if (query_id != response_id):
        print('ERROR \t [ID in response does not match ID in query]')
        return
    
    response_header = response[0:24]
    response_question = response[24:len(question) + 24]
    response_answer_index = len(question) + 24
    response_answer = response[response_answer_index:]
    
    print('Answer Header: ' + response_header)
    print('Query Header: ' + header)
    print('Answer Question: ' + response_question)
    # TODO error checking to see if answer question and query question are the same
    print('Query Question: ' + question)
    print('Answer Record: ' + response_answer)
    
    rcode = response_header[7:8]
    qdcount = response_header[8:12]
    ancount = response_header[12:16]
    nscount = response_header[16:20]
    arcount = response_header[20:24]
    
    print ('RCODE: ' + rcode)
    print ('QDCOUNT: ' + qdcount)
    print ('ANCOUNT: ' + ancount)
    print ('NSCOUNT: ' + nscount)
    print ('ARCOUNT: ' + arcount)  
      
    # Check if RCODE is 0
    if rcode == '1':
        print('ERROR \t [Format error: the name server was unable to interpret the query]')
    elif rcode == '2':
        print('ERROR \t [Server failure: the name server was unable to process this query due to a problem with the name server]')
    elif rcode == '3':
        print('NOTFOUND \t [Name error: meaningful only for responses from an authoritative name server, this code signifies that the domain name referenced in the query does not exist]')
    elif rcode == '4':
        print('ERROR \t [Not implemented: the name server does not support the requested kind of query]')
    elif rcode == '5':
        print('ERROR \t [Refused: the name server refuses to perform the requested operation for policy reasons]')
    elif rcode != '0':
        print('Unknown Error')
    
    # Check if ANCOUNT is 0
    elif ancount == '0000':
        print('ERROR \t [ANCOUNT is 0]')
        return
    # Check if NSCOUNT is 0
    elif nscount != '0000':
        print('ERROR \t [NSCOUNT is not 0]')
        return
    # Check if ARCOUNT is 0
    elif arcount != '0000':
        print('ERROR \t [ARCOUNT is not 0]')
        return
    else:
        print('Response received after [' + str(t_end - t_start) + '] seconds')

    parseAnswer(response_answer, int(ancount, 16))

def parseAnswer(response_answer, ancount):
        # Each record format: NAME, TYPE, CLASS, TTL, RDLENGTH, RDATA
        # Convert hex to binary
        # response_answer = str(bin(int(response_answer, 16)).replace('0b', '').zfill(len(response_answer) * 4))

        for record in range(ancount):
            # Parse domain name from response
            name, end = parse_domain_name(response_answer_index)
            
            # # See if name is compressed
            # if response_answer[0:2] == '11':
            #     # Get offset from pointer in octets
            #     offset = int(response_answer[2:16], 2)
            #     # Get domain name from offset
            #     name = parse_domain_name(response_answer, offset)[0]
            #     # Set end of domain name to end of pointer
            #     end = 16

            # # If name is not compressed
            # else:
            #     # Get domain name from response
            #     # name, end = parse_domain_name(response_answer, 0, len(response_answer))
            #     # TODO: check if this is correct
            #     print("TODO")

            # Get QTYPE from response
            response_type = response[end: end + 16]
            # Get QCLASS from response
            response_class = response[end + 16: end + 32]
            # Get TTL from response
            ttl = response[end + 32: end + 64]
            # Get RDLENGTH from response
            rdlength = response[end + 64: end + 80]
            # Get RDATA from response
            rdata = response[end + 80: end + 80 + int(rdlength, 2) * 8]

            # Print out record
            print('Domain Name: ' + name)
            print('QTYPE: ' + str(response_type))
            print('QCLASS: ' + str(response_class))
            print('TTL: ' + str(int(ttl, 2)))
            print('RDLENGTH: ' + str(int(rdlength, 2)))
            print('RDATA: ' + str(int(rdata, 2)))
            print('\n')
            print('Record ' + record + ' done!!')
   
# Function to decode domain name from response and handle packet compression
def parse_domain_name(offset): 
    # resonse in hex
    # offset in octets
    global response
    start = offset
    name = ''

    print('Response: ' + response)
    print('Start ' + response[start:start + 2])
    
    while response[start:start + 2] != '00':
        # Check if pointer
        print('Check pointer ' + response[start:start + 1])
        # convert hex to binary than take first two bits
        # if first two bits are 11, then it is a pointer
        
        # convert response to binary
        pointer = str(bin(int(response[start:start + 4], 16)).replace('0b', '').zfill(len(response) * 4))
        # take first two bits
        pointer_header = pointer[0:2]
        # check if pointer
        if pointer_header == '11':
            # Get offset from pointer in octets
            offset = int(pointer[2:], 2)
            # Get domain name from offset
            name += parse_domain_name(offset * 2)[0]
            # # Set end of domain name to end of pointer
            start = start + 4
            break
        
        print (response[start:start + 2])
        # if not pointer, convert hex to ascii
        for i in range(int(response[start:start + 2], 16)):
            name += binascii.unhexlify(response[start + (i + 1):start + 2 + (i + 1)]).decode('utf-8')
        name += '.'
        start += int(response[start:start + 2], 16) + 2

    end = start + 2

    return name, end


# Program entry point
if __name__ == "__main__":
    dnsClient(parseInput())