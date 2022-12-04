"""Make some requests to OpenAI's chatbot"""

import time
import os 
import flask

from flask import g

from playwright.sync_api import sync_playwright

APP = flask.Flask(__name__)
PLAY = sync_playwright().start()
BROWSER = PLAY.chromium.launch_persistent_context(
    user_data_dir="/tmp/playwright",
    headless=False,
)
PAGE = BROWSER.new_page()

def get_input_box():
    """Get the child textarea of `PromptTextarea__TextareaWrapper`"""
    print ("Getting input box")
    QUERY = PAGE.query_selector("div[class*='PromptTextarea__TextareaWrapper']")
    if QUERY is None:
        return None
    return QUERY.query_selector("textarea")

def is_logged_in():
    # See if we have a textarea with data-id="root"
    return get_input_box() is not None

def send_message(message):
    print("➡️ 🤖 Sending message to OpenAI")
    print("message : "+ message)
    # Send the message
    box = get_input_box()
    box.click()
    box.fill(message)
    box.press("Enter")

def get_last_message():
    """Get the latest message"""
    page_elements = PAGE.query_selector_all("div[class*='ConversationItem__Message']")
    last_element = page_elements[-1]
    return last_element.inner_text()

@APP.route("/chat", methods=["GET"])
def chat():
    message = flask.request.args.get("q")
    print("Sending message: ", message)
    send_message(message)
    print("⏳ Waiting for response...")
    # Get last message every 1 seconds until last_message don't change
    last_message = get_last_message()
    while True:
        time.sleep(1)
        print(" ... waiting ...")
        new_message = get_last_message()
        if new_message == last_message and new_message != "":
            break
        last_message = new_message
    print("🤖 Got response: ", last_message)
    print("⏳ ✅ End waiting for response...")
    response = get_last_message()
    print("🤖 Response: ", response)
    return response

def start_browser():
    PAGE.goto("https://chat.openai.com/")
    print("Waiting for login...")
    if not is_logged_in():
        print("Please log in to OpenAI Chat")
        print("Press enter when you're done")
        input()
        APP.run(port=5001, threaded=False)
    else:
        print("Logged in")
        APP.run(port=5001, threaded=False)
        
if __name__ == "__main__":

    # Print starting server
    print("🚀 Starting server... on port 5001")
    print(" 👉 It can be accessed at http://localhost:5001")


    start_browser()
