"""Make some requests to OpenAI's chatbot"""

import time
import os
import flask
import json
import re


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
    return PAGE.query_selector("textarea")

def is_logged_in():
    # See if we have a textarea with data-id="root"
    return get_input_box() is not None

def send_message(message):
    # Send the message
    box = get_input_box()
    box.click()
    box.fill(message)
    box.press("Enter")

def get_last_message():
    """Get the latest message"""
    page_elements = PAGE.query_selector_all("div[class*='ConversationItem__Message']")
    last_element = page_elements[-1]
    # Send back both the HTML & Plain Text
    message_contents = {
    	"text": last_element.inner_text(),
    	"html": last_element.inner_html()
	}
    return message_contents

@APP.route("/chat", methods=["GET"])
def chat():
    message = flask.request.args.get("q")
    print("Sending message: ", message)
    send_message(message)
    #wait 1 minute for ChatGPT to send back response
    try:
        element = PAGE.wait_for_selector('text="Try again"', timeout=60000)
    except TimeoutError:
        print("Element with text 'Try again' not found")
        
    response = get_last_message()
    print("Response: ", response)
    return response

def start_browser():
    PAGE.goto("https://chat.openai.com/")
    if not is_logged_in():
        print("Please log in to OpenAI Chat")
        print("Press enter when you're done")
        input()
    else:
        print("Logged in")
        APP.run(port=5001, threaded=False)

if __name__ == "__main__":
    start_browser()
