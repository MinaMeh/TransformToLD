import argparse

parser= argparse.ArgumentParser()
parser.add_argument('--operation', default="INFO",
                        choices=["CREATE", "UPDATE", "DELETE"],
                        help='specify an operation to do')
args= parser.parse_args()

