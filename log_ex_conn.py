#!/usr/bin/python3

import csv
import sys
from loge import loge
import ipaddress
import socket
import argparse

def sanitize_col(str):
    if(('(' in str) and (')' in str)):
        #print("we have a host_name")
        parts = str.split(" ")
        host = parts[1].lstrip("(").rstrip(")")

        #removed hostname ... lets make sure it's a valid IP
        try:
            if(ipaddress.ip_address(host)):
                #removed hostname and this is an IP address
                return(host)
            else:
                #removed hostname but failed IP check
                return("127.0.0.2")
        except:
            #something failed
            return("127.0.0.2")
    else:
        #no hostname ... lets make sure it's a valid IP
        try:
            if(ipaddress.ip_address(str)):
                #no hostname and this is an IP address
                return(str)
            else:
                #no hostname but failed IP check
                return("127.0.0.2")
        except:
            #something failed
            return("127.0.0.2")
#end of sanitize_col

def extract_logs(ifile):
    debug = 0

    print("in function extract_logs")

    log_list = list()
    with open(ifile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            source = sanitize_col(row[0])
            dest   = sanitize_col(row[1])
            port   = row[2]
            
            if(debug == 1):
                print(source, end=" ")
                print(dest, end=" ")
                print(port, end="\n")

            entry = loge(source, dest, port)

            foundme = 0
            i = 0
            #search list to keep it uniq
            for en in log_list:
                if(debug == 1):
                    print(i)
                    i = i + 1
                    en.print_log_entry()
                if(en.compare(source, dest, port)):
                    en.increment()
                    foundme = 1
            # not found.  add it (also works for first entry since list is empty)
            if(foundme == 0):
                log_list.append(entry)
            
    ## dump
    if(debug == 1):
        print("-------------------------------------------")
        for en in log_list:
            en.print_log_entry()
    
    return(log_list)
#end of extract_logs

def connection_test(loge):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (loge.get_dest(), int(loge.get_port()))

    result = a_socket.connect_ex(location)

    if(result == 0):
        return True
    else:
        return False
#end of connection_test

def main():
    print("Log Extract")

    debug = 1

    parser = argparse.ArgumentParser(description='Log Exctract and Analysis')
    parser.add_argument("-f", required=True, help="Log File")
    parser.add_argument("-c", required=False, help="Do a connection to port (yes)")

    args = parser.parse_args()

    #inputfile = "telnet.csv"  #sys.argv[1]
    inputfile = args.f 

    #list of loge
    log_list = list()

    #need return to list
    log_list = extract_logs(inputfile)

    for en in log_list:
        en.print_log_entry()

        if(args.c == "yes"):
            if(connection_test(en)):
                print("Port Alive")
            else:
                print("Port Not_Found")

#end of main

if __name__ == "__main__":
    main()