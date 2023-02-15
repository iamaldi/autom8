#!/usr/bin/python3

"""
Name: autom8 Nmap Module
Description: Parse and group Nmap results.
Project: https://github.com/iamaldi/autom8
"""

import os

from nmaptocsv.nmaptocsv import parse
from nmaptocsv.nmaptocsv import parse_xml
from nmaptocsv.nmaptocsv import generate_csv

NEWLINE_PLACEHOLDER = "/newline_placeholder"

def parse_output(arguments):
    try:
        # parse normal (-oN) Nmap output
        if arguments.normal:
            fd_nmap_output = open(arguments.normal, 'r', encoding="utf-8")
            print("[autom8:nmap] Parsing '{}'".format(os.path.os.path.realpath(fd_nmap_output.name)))
            nmaptocsv_results = parse(fd_nmap_output)
        
        # parse XML (-oX) Nmap output
        elif arguments.xml:
            fd_nmap_output = open(arguments.xml, 'r', encoding="utf-8")
            print("[autom8:nmap] Parsing '{}'".format(os.path.os.path.realpath(fd_nmap_output.name)))
            nmaptocsv_results = parse_xml(fd_nmap_output)
        
        # generate a temp CSV file with the parsed output
        fd_tmp = open(os.path.dirname(__file__) + '/../tmp_nmaptocsv_results.csv', 'w+', encoding="utf-8")
        generate_csv(fd_tmp, nmaptocsv_results, arguments)

        # group results
        group_results(fd_tmp, arguments.output, arguments.delimiter)
    
    except IOError as e:
        exit("[autom8:nmap]: ", str(e))

def group_results(fd_tmp, output, delimiter):
    try:
        print("[autom8:nmap] Reading temporary CSV from '{0}'".format(os.path.realpath(fd_tmp.name)))
        fd_tmp.seek(0)
        nmap_entries = fd_tmp.readlines()
        fd_tmp.close()
        print("[autom8:nmap] Deleting temporary CSV file '{0}'".format(os.path.realpath(fd_tmp.name)))
        os.unlink(os.path.realpath(fd_tmp.name))
    except IOError as e:
        exit("[autom8:nmap]: ", str(e))

    print("[autom8:nmap] Grouping Nmap results by IP address")

    entry_group = []
    nmap_results = []

    # traverse result entries; skip CSV header
    for entry in nmap_entries[1:]:
        # single entry:
        # "10.10.10.3";"corp.local";"22";"tcp";"ssh";"OpenSSH 5.3 (protocol 2.0)"

        # process entry groups into a single entry
        # entry groups are defined by an empty newline
        if entry == '\n':
            # example of an entry group:
            #
            # ['10.10.10.3;corp.local;22;tcp;ssh;OpenSSH 5.3 (protocol 2.0)',
            # '10.10.10.3;corp.local;111;tcp;rpcbind;2-4 (RPC #100000)',
            # '10.10.10.3;corp.local;1111;tcp;lmsocialserver?;']
            
            entry_result = {
                "fqdn" : "",
                "ip" : "",
                "ppsv" : "", # port, protocol, service, version
                "os" : ""
            }

            # extract and group the port, protocol, service and version data from each entry
            for entry_details in entry_group:
                if len(entry_group) > 1:
                    entry_result['ppsv'] += '/'.join(entry_details.split(delimiter)[2:]).rstrip("/") + NEWLINE_PLACEHOLDER
                else:
                    entry_result['ppsv'] += '/'.join(entry_details.split(delimiter)[2:]).rstrip("/")
            
            # only process hosts that have at least one open port
            if entry_result['ppsv'] != "":
                # add the IP address and FQDN to the entry result
                entry_result['ip'] = entry_group[0].split(delimiter)[0]
                entry_result['fqdn'] = entry_group[0].split(delimiter)[1]

                # remove trailing placeholder
                entry_result['ppsv'] = entry_result['ppsv'].removesuffix(NEWLINE_PLACEHOLDER)
                nmap_results.append(entry_result)
            entry_group = []
        else :
            # group multiple entries by host
            entry_group.append(entry.replace('"', '').removesuffix('\n'))

    try:
        results_file = open(output, "w", encoding="utf-8")
        results_file.write('FQDN;IP;PORT/PROTOCOL/VERSION;OS\n')

        for result in nmap_results:
            results_file.write(";".join(result.values()) + '\n')
        
        results_file.close()

        print("[autom8:nmap] Results written to '{0}'".format(os.path.realpath(results_file.name)))
        print("[autom8:nmap] In MS Word: You can replace the '/newline_placehoder' with line break using '^l' in 'Find & Replace'")
        print("[autom8:nmap] In MS Excel: You can replace the '/newline_placehoder' with line break using CTRL + J in 'Find & Replace'")
    
    except IOError as e:
        exit("[autom8:nmap]: ", str(e))
