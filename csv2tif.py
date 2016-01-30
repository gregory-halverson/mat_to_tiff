import sys

from csv_to_tiff import csv_to_global_tiff

if len(sys.argv) > 1:
    csv_directory = sys.argv[1]
else:
    csv_directory = None
    exit()

if len(sys.argv) > 2:
    variable_name = sys.argv[2]
else:
    variable_name = None
    exit()

if len(sys.argv) > 3:
    output_directory = sys.argv[3]
else:
    output_directory = None
    exit()

csv_to_global_tiff(csv_directory, variable_name, output_directory)