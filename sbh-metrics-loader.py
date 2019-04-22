#!/usr/bin/env python3

import argparse
import configparser
import csv
import hashlib
import json
import datetime
import logging
import os
import sys
import time

import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.util.retry import Retry

S_LOGSTASH = 'logstash_writer'
O_URL = 'url'
O_KEY = 'key'
O_SECRET = 'secret'

DATAFRAME_VERSION = '1.0.0'
SALT = '[/bZpm,U3+-U'


def generate_token():
    t = int(time.time()/60)*60
    hasher = hashlib.sha1()
    hasher.update(str(t).encode('utf-8') + SALT.encode('utf-8'))
    return hasher.hexdigest()[0:8]


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=argparse.FileType('r'),
                        metavar="CONFIG_FILE")
    parser.add_argument("csvfile", type=argparse.FileType('r'),
                        metavar="CSV_FILE")
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-t', '--token', action='store_true',
                        help='Add a time-based token to each record')
    parser.add_argument("-C", "--classname",
                        metavar="ClassName", help="Optional class name")
    args = parser.parse_args(args)
    return args


def init_logging(debug=False):
    msgFormat = '%(asctime)s %(levelname)s %(message)s'
    dateFormat = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msgFormat, datefmt=dateFormat, level=level)


def send_record(msg, url, key, secret):
    try:
        r = requests.Session()
        # In case the Logstash HTTP endpoint gets overwhelmed
        retries = Retry(total=5, backoff_factor=1,
                        status_forcelist=[502, 503, 504])
        r.mount('https://', HTTPAdapter(max_retries=retries))
        r.post(url, json=msg, auth=HTTPBasicAuth(
            key, secret))
    except Exception:
        logging.exception(
            'Failed to POST payload to Logstash')
        raise


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)
    config = configparser.ConfigParser()
    config.read_file(args.config)

    if not config.has_section(S_LOGSTASH):
        print('No "{}" section found in {} configuration'.format(S_LOGSTASH))
        sys.exit(1)

    logstash_url = config.get(S_LOGSTASH, O_URL,
                              fallback=None)
    logstash_key = config.get(S_LOGSTASH, O_KEY, fallback=None)
    logstash_secret = config.get(S_LOGSTASH, O_SECRET, fallback=None)

    atoken = generate_token()
    if args.token:
        print('Token: ' + atoken)

    with args.csvfile as f:

        if args.classname:
            pretty_class = args.classname
        else:
            pretty_class = os.path.splitext(
                os.path.basename(f.name))[0]
        logging.info(f'Loading {pretty_class}')

        reader = csv.DictReader(f)
        headers = [h.lower().replace(' ', '-') for h in reader.fieldnames]
        try:
            int(headers[0])
            headers = ['timestamp', 'name', 'value']
            logging.info('Using pre-defined fieldnames')
        except ValueError:
            logging.info('Using fieldnames from CSV file')
        reader.fieldnames = headers

        for row in reader:
            row['class'] = pretty_class
            row['version'] = DATAFRAME_VERSION
            if 'name' in row:
                row['name'] = row['name'].replace(' ', '-')
            row['timestamp'] = datetime.datetime.utcfromtimestamp(
                int(row['timestamp'])).isoformat() + 'Z'
            # Optionally, add a discriminator token to records when stored
            if args.token:
                row['token'] = atoken

            send_record(row, logstash_url, logstash_key, logstash_secret)


if __name__ == '__main__':
    main()
