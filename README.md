# autom8

This project is work-in-progress, and as a result the functionality presented below is not guaranteed to work flawlessly. `autom8` currently implements the following commands:

- `nmap` -> Parse Nmap output with `nmaptocsv` and group the results into CSV.


#### Installation

Clone `autom8` locally and install the required packages (argparse, nmaptocsv).

```console
$ git clone https://github.com/iamaldi/autom8.git
$ cd autom8/
$ pip install -r requirements
```

#### Usage

List available commands.

```console
$ python3 autom8.py -h
usage: python3 autom8.py [-h] {nmap} ...

options:
  -h, --help  show this help message and exit

Available commands:
  {nmap}      List required arguments with 'command help'
    nmap      Parse Nmap output with nmaptocsv and group the results into CSV.
```

List details of the `nmap` command.


```console
$ python3 autom8.py nmap -h
usage: python3 autom8.py nmap [-h] (-n NORMAL | -x XML) [-d {;,,}] -o OUTPUT [-f FORMAT]

options:
  -h, --help            show this help message and exit
  -n NORMAL, --normal NORMAL
                        Path to file with Normal (-oN) or Grepable (-oG) Nmap output.
  -x XML, --xml XML     Path to file with XML (-oX) Nmap output.
  -d {;,,}, --delimiter {;,,}
                        Delimiter to use in the CSV output. (default: ;)
  -o OUTPUT, --output OUTPUT
                        Destination path to save the CSV output. (required)
  -f FORMAT, --format FORMAT
                        CSV output format {fqdn, rdns, hop_number, ip, mac_address, mac_vendor, port, protocol, os, script, service, version} (default: ip-fqdn-port-protocol-service-version)
```

* `-f/--format` argument can be set however currently there is no implementation to reflect it in the final output

#### Example

```console
$ python3 autom8.py nmap -n ../localscan.nmap -o /tmp/localscan_results.csv

[autom8:nmap] Parsing '/home/user/localscan.nmap'
[autom8:nmap] Reading temporary CSV from '/home/user/autom8/tmp_nmaptocsv_results.csv'
[autom8:nmap] Deleting temporary CSV file '/home/user/autom8/tmp_nmaptocsv_results.csv'
[autom8:nmap] Grouping Nmap results by IP address
[autom8:nmap] Results written to '/tmp/localscan_results.csv'
[autom8:nmap] In MS Word: You can replace the '/newline_placehoder' with line break using '^l' in 'Find & Replace'
[autom8:nmap] In MS Excel: You can replace the '/newline_placehoder' with line break using CTRL + J in 'Find & Replace'
```

```console
$ cat /tmp/localscan_results.csv

FQDN;IP;PORT/PROTOCOL/VERSION;OS
gateway;10.15.20.1;53/tcp/domain/newline_placeholder80/tcp/http/newline_placeholder443/tcp/https/newline_placeholder20001/tcp/microsan;
```

#### Credits

- `autom8`'s 'nmap' command relies on [nmaptocsv](https://github.com/maaaaz/nmaptocsv) for parsing the Nmap output 
