import urllib.parse
import requests
import sys
from builtins import input

def process_query(query):
    if query == "quit":
        print("Exiting.")
        sys.exit()

    # Define the base URL
    base_url = "http://localhost:5001/chat"

    # URI encode the string argument
    encoded_arg = urllib.parse.quote(query)

    # Append the encoded argument to the base URL
    url = base_url + "?q=" + encoded_arg

    # Make a GET request to the URL
    response = requests.get(url)

    # Print the response
    print(response.text)

def loop():
    # Set up the REPL loop
    while True:
        # Prompt the user for input
        query = input("⎊: ")
        print("--")

        # Evaluate the user's input
        process_query(query)
        print("--")

if __name__ == "__main__":
    loop()
