import argparse
import csv
import logging
import os
import sys

# Set the log output file, and the log level.
logging.basicConfig(filename="output.log", level=logging.DEBUG)


def put(name, snippet, filename):
    """ Store a snippet with an associated name in the CSV file.
    Allows for multiple snippets by the same name to be present.
    """
    logging.info("Writing {!r}:{!r} to {!r}".format(name, snippet, filename))
    with open(filename, "a") as f:
        logging.debug("Opening file: {!r}".format(filename))
        writer = csv.writer(f)
        logging.debug("Writing snippet to file...")
        writer.writerow([name, snippet])
        logging.debug("Write successful")
    return name, snippet

def search(string, filename):
    """Retrieves all snippets from a file that contain the string. """
    logging.info("Retrieving {!r} from {!r}".format(string, filename))
    with open(filename, "rb") as f:
        logging.debug("Opening file: {!r}".format(filename))
        reader = csv.reader(f)
        logging.debug("Retrieving snippet: {!r}".format(string))
        my_snippets = []
        for row in reader:
            if string in row:
                my_snippets.append(row)
                logging.debug("Retrieval Successful")
    return my_snippets

def get(name, snippet, filename):
    """Search for a stored snippet by given string in the CSV file. """
    logging.info("Searching for name {!r} in {!r}".format(name, filename))
    with open(filename, "rb") as f:
        logging.debug("Searching file: {!r}".format(filename))
        reader  = csv.reader(f)
        snippet = ""
        for row in reader:
            if name in row[0]:
                snippet = row[1]
                break
    return name, snippet

def update(name, snippet, filename):
    """Find an existing snippet and update it. """
    logging.info("Looking for snippet {!r}".format(name))
    with open(filename, "a+") as f:
        logging.debug("Searching file: {!r}".format(filename))
        writer = csv.writer(f)
        reader = csv.reader(f)
        for row in reader:
            if name in row:
                writer.writerow([name, snippet])
                logging.debug("Updated row")
            else:
                logging.info("No row found")
                print "No available snippet to update."
    return name, snippet

def make_parser():
    """ Construct the command line parser """
    logging.info("Constructing parser")
    description = "Store and retrieve snippets of text"
    parser = argparse.ArgumentParser(description=description)

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    #Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    put_parser.add_argument("filename", default="snippets.csv", nargs="?",
                            help="The snippet filename")

    #Subparser for search command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search",
                                       help="Find all the snippets with string.")
    search_parser.add_argument("string", help="The string to search for")
    search_parser.add_argument("filename", default="snippets.csv", nargs="?",
                            help="The snippet filename")

    #Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get",
                                       help="Retrieve a snippet by name")
    get_parser.add_argument("name", help="Name of the snippet you want to get.")
    get_parser.add_argument("snippet", default="", nargs="?")
    get_parser.add_argument("filename", default="snippets.csv", nargs="?",
                            help="The snippet filename")

    logging.debug("Constructing update subparser")
    update_parser = subparsers.add_parser("update",
                                          help="Update an existing snippet")
    update_parser.add_argument("name", help="Name of snippet to update")
    update_parser.add_argument("snippet", help="Text of the snippet.")
    update_parser.add_argument("filename", default="snippets.csv", nargs="?",
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
    # Create the file if it doesn't exist
    logging.debug("Checking to see if file exists..")
    if os.path.exists(arguments['filename']):
        logging.debug("File {!r} exists.".format(arguments['filename']))
    else:
        logging.debug("File {!r} doesn't exist.".format(arguments['filename']))
        with open(arguments['filename'], "a+") as c:
            writer = csv.writer(c)
            header = ["name","snippet"]
            writer.writerow(header)

    if command == "put":
        exists = get(**arguments)
        if len(exists[1]) > 0:
            print "Sorry, {!r} already exists.".format(exists[0])
        else:
            name, snippet = put(**arguments)
            print "Stored {!r} as {!r}.".format(snippet, name)

    elif command == "search":
        search_list = search(**arguments)
        if search_list:
            for item in search_list:
                print "{!r}: {!r}".format(item[0], item[1])
        else:
            print "Sorry, no snippet stored by that name!"

    elif command == "get":
        get_list = get(**arguments)
        if len(get_list[1]) > 0:
            print "Name: {!r}, Snippet: {!r}".format(get_list[0], get_list[1])
        else:
            print "No snippet stored by name: {!r}".format(get_list[0])

    elif command == "update":
        name, snippet = update(**arguments)
        print "Updating {!r} with {!r}.".format(name, snippet)

if __name__ == "__main__":
    main()
