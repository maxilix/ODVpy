from common import extension
from dvf_parser import DvfParser
from dev.utils import list_files

# parser = argparse.ArgumentParser(description='Desperados WDoA DVF extractor')
# parser.add_argument('dvf_file', metavar='FILE', type=str, help='DVF file to parse')
# #parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')
#
#
# args = parser.parse_args()
# path_to_file = args.dvf_file


dvf_list = list_files("../../Desperados Wanted Dead or Alive/", recursive=True,
                      filename_filter=lambda filename: extension(filename) == "dvf")
# for f in dvf_list:
#     print(f.rsplit("/", 1)[1])

dvf = DvfParser(dvf_list[20])

dvf.sprites[33].build()
dvf.sprites[33].bmp.show()
