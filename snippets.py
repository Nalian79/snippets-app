import argparse
import csv
import logging
import sys

# Set the log output file, and the log level.
logging.basicConfig(filename="output.log", level=logging.DEBUG)

def put(name, snippet, filename):
    """ Store a snippet with an associated name in the CSV file """
    logging.info("Writing {!r}:{!r} to {!r}".format(name, snippet, filename))
    logging.debug("Opening file")
    with open(filename, "a") as f:
        writer = csv.writer(f)
        logging.debug("Writing snippet to file")
        writer.writerow([name, snippet])
    logging.debug("Write successful")
    return name, snippet

def make_parser():
    """ Construct the command line parser """
    logging.info("Constructing parser")
    description = "Store and retrieve snippets of text"
    parser = argparse.ArgumentParser(description=description)

    subparsers = parser.add_subparsers(help="Available commands")

    #Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    put_parser.add_argument("filename", default="snippets.csv", nargs="?",
                            help="The snippet filename")

    return parser

def main():
    """ Main function """
    logging.info("Starting snippets")
    parser = make_parser()
    logging.debug("All arguments are: {!r}".format(sys.argv[0:]))
    arguments = parser.parse_args(sys.argv[1:])
    logging.debug("Arguments are: {!r}".format(arguments))
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    logging.debug("Arguments are now: {!r}".format(arguments))
    command = arguments.pop("command")

    if command == "put":
        name, snippet, filename = put(**arguments)
        print "Stored {!r} as {!r} in {!r}".format(snippet, name, filename)

if __name__ == "__main__":
    main()
