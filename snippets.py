#
# Snippets App: A simple command line application to store snippets of text
# in a database
#
# February 2015
# Version 1.0
#

# import the logging module to store the output of the App in a log file
import logging
# import argparse module so that can accept aruments from the Command Line
import argparse
# import sys module so can access the argv variable
import sys
# import psycopg2 to use PostgreSQL with Python
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
# Add logging lines for connecting snippets app to database from Python
logging.debug("Connection to PostgreSQL.")
# Establish the connection to Postgres with the psycopg2 package - settings
connection = psycopg2.connect("dbname='snippets' user='m' host='localhost'")
logging.debug("Database connection established.")


# Define four functions to Create, Retrieve, Update & Destroy objects in the database.
# Four code stubs (unfinished skeleton code to just get basics working).

# Create objects in the database
def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet.
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    # ADD error handling to the put method:
    #     where the snippet already exists, simply update it, otherwise
    #     Psycopg2 throws an error that the snippet already exists.
    #     NB: this is called a MERGE
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("INSERT INTO snippets VALUES (%s, %s)", (name, snippet))
    except psycopg2.IntegrityError as e:
        with connection, connection.cursor() as cursor:
            connection.rollback()
            cursor.execute("UPDATE snippets SET message=%s WHERE keyword=%s", (snippet, name))
            connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet

# Retrieve objects in the database
def get(name):
    """"
    Retrieve the snippet with the given name.

    If there is no such snippet, displays error message. #TODO: Confirm this with mentor

    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    # Using the 'with' block the transaction is guaranteed to be committed (if everything works)
    # or rolled back if there's an exception thrown
    # [cursor object is known as a context manager] when context managers are used in a 'with' block
    # they automatically perform cleanup actions when exited
    with connection, connection.cursor() as cursor:
        cursor.execute("SELECT message FROM snippets WHERE keyword=%s;", (name,))
        row = cursor.fetchone()
    logging.debug("Snippet retrieved successfully.")
    # Need to add commit() call, to do with locking access to database while reading
    connection.commit()
    if not row:
        # No snippet was found with that name
        return "ERROR: No snippet with that name exists. Please try again."
    return row[0]
    
# Update objects in the database    
def update(name):
    """
    Retrieve a snippet and update it's associated name or snippet.

    Returns the name and the snippet.
    """
    logging.error("FIXME: Unimplemented - update({!r})".format(name))
    return name + " updated."

# Delete objects in the database
def delete(name):
    """"
    Delete the snippet with the given name.

    If there is no such snippet, displays error message. #TODO: Confirm this with mentor

    Returns message confirming snippet deleted.
    """
    logging.error("FIXME: Unimplemented - delete({!r})".format(name))
    return name + " deleted."


# Build the Command Line Interface. The ability to accept arguments on the CL
# (Note: two alternatives using options ('-x' or '--y') or postion (e.g. git)

def main():
    """ Main function. Accepts arguments on command line """
    logging.info("Constructing parser")

    # STEP 1: CREATE THE ARGUMENT PARSER
    # Create instance of 'ArgumentParser' object from argsparse module (must add import argparse)
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    # STEP 2: CREATE MULTIPLE SUBPARSERS FOR EACH COMMAND
    # Here using the 'add_subparsers' method of the parser to add multiple subparsers
    # Have different subparsers for the different commands (similar to git)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 1. Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet.")
    put_parser.add_argument("snippet", help="The snippet of text (a string enclosed in '').")

    # 2. Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")

    # STEP 3: JOIN THE MAIN AND SUB-PARSERS TOGETHER
    # 'parse_args' function takes list of arguments and splits into named variabes,
    # access the arguments via the 'arguments' variable

    arguments = parser.parse_args(sys.argv[1:])
        # Then convert parsed arguments from Namespace to dictionary
        # (using built-in 'vars' function) as dictionary is
        # easier to work with
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        # double star operator is unpacking, converts key-value pairs in dictionary
        # into keyword arguments to the function
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))

# Enable snippets.py to be called from the Command Line
if __name__ == "__main__":
    main()