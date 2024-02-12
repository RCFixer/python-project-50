import argparse

parser = argparse.ArgumentParser(description='Compares two configuration files and shows a difference.')
parser.add_argument('file', metavar='first_file')
parser.add_argument('file', metavar='second_file')

args = parser.parse_args()

