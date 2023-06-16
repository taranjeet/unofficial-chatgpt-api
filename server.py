#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import os
import time
import flask
from flask import request
from playwright.sync_api import sync_playwright

app = flask.Flask(__name__)
playwright = sync_playwright().start()
browser = playwright.chromium.launch_persistent_context(user_data_dir="/tmp/playwright", headless=False)
page = browser.new_page()


def get_input_box():
    """Get the child textarea of `PromptTextarea__TextareaWrapper`"""
    return page.query_selector("textarea")


def is_logged_in():
    # See if we have a textarea with data-id="root"
    return get_input_box() is not None


def is_loading_response() -> bool:
    """See if the send button is disabled, if it is, we're still loading"""
    return not page.query_selector("textarea ~ button").is_enabled()


def send_message(message):
    # Send the message
    box = get_input_box()
    box.click()
    box.fill(message)
    box.press("Enter")


def get_last_message():
    """Get the latest message"""
    while is_loading_response():
        time.sleep(0.25)
    page_elements = page.query_selector_all("div[class*='request-:']")
    last_element = page_elements[-1]
    return last_element.inner_text()


def regenerate_response():
    """Clicks on the Try again button.
    Returns None if there is no button"""
    try_again_button = page.query_selector("button:has-text('Try again')")
    if try_again_button is not None:
        try_again_button.click()
        time.sleep(0.5)
    return try_again_button


def get_reset_button():
    """Returns the reset thread button (it is an a tag not a button)"""
    return page.query_selector("a:has-text('Reset chat')")


@app.route("/chat", methods=["POST"])
def chat():
    message = request.form.get("message")
    send_message(message)
    response = get_last_message()
    return response


@app.route("/regenerate", methods=["POST"])
def regenerate():
    if regenerate_response() is None:
        return "No response to regenerate"
    response = get_last_message()
    return response


@app.route("/reset", methods=["POST"])
def reset():
    get_reset_button().click()
    return "Chat thread reset"


@app.route("/restart", methods=["POST"])
def restart():
    global page, browser, playwright
    page.close()
    browser.close()
    playwright.stop()
    time.sleep(0.25)
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch_persistent_context(user_data_dir="/tmp/playwright", headless=False)
    page = browser.new_page()
    page.goto("https://chat.openai.com/")
    return "API restart!"


def start_browser():
    page.goto("https://chat.openai.com/")
    if not is_logged_in():
        print("Please log in to OpenAI Chat")
        print("Press enter when you're done")
        input()
    else:
        print("Logged in")

    app.run(port=5001, threaded=False, host="0.0.0.0")


if __name__ == "__main__":
    start_browser()
