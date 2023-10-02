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
    
    print('DnsClient sending request for: ' + args.name)
    print('Server: ' + args.server[1:])
    if (args.mx):
        qtype_string = 'MX'
    elif (args.ns):
        qtype_string = 'NS'
    else:
        qtype_string = 'A'
    print('Request type: ' + qtype_string)
    
    # Send query to server for max number of retries
    for i in range(args.max_retries):
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
        response = binascii.hexlify(response[0]).decode('utf-8')
        
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
    
    # print('Answer Header: ' + response_header)
    # print('Query Header: ' + header)
    # print('Answer Question: ' + response_question)
    # # TODO error checking to see if answer question and query question are the same
    # print('Query Question: ' + question)
    # print('Answer Record: ' + response_answer)
    
    # convert qr & aa from hex to binary
    qr = str(bin(int(response_header[4:5], 16)).replace('0b', '').zfill(4))[0:1]
    aa = int(str(bin(int(response_header[5:6], 16)).replace('0b', '').zfill(4))[1:2], 2)
    rcode = response_header[7:8]
    qdcount = response_header[8:12]
    ancount = response_header[12:16]
    nscount = response_header[16:20]
    arcount = response_header[20:24]
    
    # print ('QR: ' + qr)
    # print ('AA: ' + str(aa))
    # print ('RCODE: ' + rcode)
    # print ('QDCOUNT: ' + qdcount)
    # print ('ANCOUNT: ' + ancount)
    # print ('NSCOUNT: ' + nscount)
    # print ('ARCOUNT: ' + arcount)
      
    # Check if RCODE is 0
    if rcode == '1':
        print('ERROR \t [Format error: the name server was unable to interpret the query]')
        exit()
    elif rcode == '2':
        print('ERROR \t [Server failure: the name server was unable to process this query due to a problem with the name server]')
        exit()
    elif rcode == '3':
        print('NOTFOUND \t [Name error: meaningful only for responses from an authoritative name server, this code signifies that the domain name referenced in the query does not exist]')
        exit()
    elif rcode == '4':
        print('ERROR \t [Not implemented: the name server does not support the requested kind of query]')
        exit()
    elif rcode == '5':
        print('ERROR \t [Refused: the name server refuses to perform the requested operation for policy reasons]')
        exit()
    elif rcode != '0':
        print('Unknown Error')
        exit()
    
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
        print('TODO')

    if (int(ancount, 16) > 0): 
        print("***Answer Section ((" + str(int(ancount, 16)) + " records)***")
        parseAnswer(int(ancount, 16), response_answer_index, aa)
    else:
        print("NOTFOUND")
    
    if (int(arcount, 16) > 0): 
        print("***Additional Section (" + str(int(arcount, 16)) + "records)***")
        parseAnswer(int(arcount, 16), response_answer_index, aa)
        
def parseAnswer(count, index, aa):
    # Each record format: NAME, TYPE, CLASS, TTL, RDLENGTH, RDATA
    auth_status = 'auth' if aa else 'nonauth'
        
    for record in range(count):
        # Parse domain name from response
        name, end = parse_domain_name(index)

        # Get QTYPE from response
        response_type = response[end: end + 4]
        # Get QCLASS from response
        response_class = response[end + 4: end + 8]
        # Get TTL from response
        ttl = response[end + 8: end + 16]
        # Get RDLENGTH from response
        rdlength = response[end + 16: end + 20]
        # Get RDATA from response
        rdata_index = end + 20
        rdata = response[rdata_index: rdata_index + int(rdlength, 16) * 2]
            
        # if A type => convert to IP address (4 octects)
        if (response_type == '0001'):
            rdata = str(int(rdata[0:2], 16)) + '.' + str(int(rdata[2:4], 16)) + '.' + str(int(rdata[4:6], 16)) + '.' + str(int(rdata[6:8], 16))
            print('IP \t [' + rdata + '] \t [' + ttl + '] \t' + auth_status)
        # if NS type => convert to qname
        elif (response_type == '0002'):
            rdata, end = parse_domain_name(rdata_index)
            print('NS \t [' + rdata + '] \t [' + ttl + '] \t' + auth_status)
        # if CNAME type => name of alias
        elif (response_type == '0005'):
            rdata, end = parse_domain_name(rdata_index)
            print('CNAME \t [' + rdata + '] \t [' + ttl + '] \t' + auth_status)
        # if MX type => preference + exchange
        elif (response_type == '000f'):
            rdata, end = parse_domain_name(rdata_index + 4)
            print('MX \t [' + rdata + '] \t [' + ttl + '] \t' + auth_status)
        else:
            rdata = 'Unknown'

        # increment index to next record
        index = rdata_index + int(rdlength, 16) * 2
                
   
# Function to decode domain name from response and handle packet compression
def parse_domain_name(offset): 
    global response
    start = offset
    name = ''
    
    while response[start:start + 2] != '00':
        # convert response to binary
        pointer = str(bin(int(response[start:start + 4], 16)).replace('0b', '').zfill(16))
        # take first two bits
        pointer_header = pointer[0:2]
        # check if pointer
        if pointer_header == '11':
            # Get offset from pointer in octets
            offset = int(pointer[2:], 2)
            name += parse_domain_name(offset * 2)[0]
            start += 4
            break
        else:
            for i in range(int(response[start:start + 2], 16)):
                name += binascii.unhexlify(response[start + (i + 1) * 2:start + (i + 2) * 2]).decode('utf-8')
            name += '.'
            start += (int(response[start:start + 2], 16) + 1) * 2
        
    if name.endswith('.'):
        name = name[:-1]
            
    return name, start

# Program entry point
if __name__ == "__main__":
    dnsClient(parseInput())