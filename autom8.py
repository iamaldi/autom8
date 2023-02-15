#!/usr/bin/python3

"""
Name: autom8
Description: Python scripts used for automation in security assessment pipelines.
Project: https://github.com/iamaldi/autom8
"""

import argparse
from modules import nmap

if __name__ == "__main__":

    # autom8.py argument definitions
    parser = argparse.ArgumentParser(prog='python3 autom8.py')
    subparsers = parser.add_subparsers(title='Available commands', dest='command', help='List required arguments with \'command help\'')

    # nmaptocsv sub-command arguments
    nmaptocsv_subparser = subparsers.add_parser('nmap', help='Parse Nmap output with nmaptocsv and group the results into CSV.')

    nmaptocsv_group = nmaptocsv_subparser.add_mutually_exclusive_group(required=True)
    nmaptocsv_group.add_argument('-n', '--normal', help='Path to file with Normal (-oN) or Grepable (-oG) Nmap output.')
    nmaptocsv_group.add_argument('-x', '--xml', help='Path to file with XML (-oX) Nmap output.')
    nmaptocsv_subparser.add_argument('-d', '--delimiter', choices=[';',','], default=';', help='Delimiter to use in the CSV output. (default: ;)')
    nmaptocsv_subparser.add_argument('-o', '--output', required=True, help='Destination path to save the CSV output. (required)')
    nmaptocsv_subparser.add_argument('-f', '--format', help = 'CSV output format {fqdn, rdns, hop_number, ip, mac_address, mac_vendor, port, protocol, os, script, service, version} (default: ip-fqdn-port-protocol-service-version)', default='ip-fqdn-port-protocol-service-version-os')
    nmaptocsv_subparser.add_argument('-s', '--script', help=argparse.SUPPRESS, action = 'store_const', const = 'ip-fqdn-port-protocol-service-version-script')
    nmaptocsv_subparser.add_argument('-nn', '--no-newline', help=argparse.SUPPRESS, default=False)
    nmaptocsv_subparser.add_argument('-sh', '--skip-header', help=argparse.SUPPRESS, default=False)

    arguments = parser.parse_args()
    
    if arguments.command == 'nmap':
        nmap.parse_output(arguments)
    else:
        parser.print_help()
