#!/usr/bin/enc python3

import argparse
import os

from c_dvf_parser import DvfParser





parser = argparse.ArgumentParser(description='Desperados WDoA DVF extractor')
parser.add_argument('dvf_file', metavar='FILE', type=str, help='DVF file to parse')
#parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')


args = parser.parse_args()
path_to_file = args.dvf_file

dvf = DvfParser(path_to_file)
dvf.save()





