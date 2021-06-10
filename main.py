import os
import requests
import asyncio
from pyppeteer import launch
from dotenv import load_dotenv
import json
import logging

logging.basicConfig(filename ='secrets_retriever_app.log',
                        level = logging.ERROR)

COOKIE_URL = os.getenv("COOKIE_URL", None)
if not COOKIE_URL:
    raise Exception(
        "You need to set your API key to your LINKEDIN_USERNAME .env variable"
    )

PRESENCE_OF_LOGIN = os.getenv("PRESENCE_OF_LOGIN", None)
if not PRESENCE_OF_LOGIN:
    raise Exception(
        "You need to set your API key to your LINKEDIN_USERNAME .env variable"
    )
elif PRESENCE_OF_LOGIN == "Y":
    USER_NAME = os.getenv("USER_NAME", None)
    if not USER_NAME:
        raise Exception(
            "You need to set your API key to your LINKEDIN_USERNAME .env variable"
        )

    PASS_WORD = os.getenv("PASS_WORD", None)
    if not PASS_WORD:
        raise Exception(
            "You need to set your API key to your LINKEDIN_PASSWORD .env variable"
        )
elif PRESENCE_OF_LOGIN == "N":
    pass
elif PRESENCE_OF_LOGIN != "N" and PRESENCE_OF_LOGIN != "N":
    raise Exception(
            "Something is not right"
        )

def open_text_file(content_text):
    with open('cookie_content.txt', 'w+') as cookie_file:
            cookie_file.write(content_text)

def append_text_file(append_content):
    with open('cookie_content.txt', 'a') as f:
        f.writelines(append_content)


async def main():
    browser = await launch({'headless': True, 'devtools': False}) 
    page = await browser.newPage()
    await page.goto(COOKIE_URL)
    # await page.waitForNavigation()
    if PRESENCE_OF_LOGIN == "Y":
        await page.type('#username', USER_NAME) # if the id of the username field is username proceed if not inspect browser and update
        await page.type('#password', PASS_WORD) # if the id of the password field is password proceed if not inspect browser and update
        await asyncio.wait([
            page.keyboard.press('Enter'),
            page.waitForNavigation(),
        ])
    await page.screenshot({'path': 'cookiepage.png'}) #check the screenshot to confirm you were logged in and not shown a security page
    cookies_all = await page.cookies()
    if cookies_all:
        try:
            number_of_cookies_present = len(cookies_all)
            open_text_file(f"These are the {number_of_cookies_present} cookies for {COOKIE_URL} \n")
            cookie_counter = 1
            for cookie_item in cookies_all:
                print(f"This is Cookie Number {cookie_counter}")
                append_content = json.dumps(cookie_item, indent=4)
                print(append_content)
                append_text_file(append_content)
                print("========================================")
                cookie_counter += 1
                if cookie_counter > number_of_cookies_present:
                    break
        except Exception as exc:
            print("There was an error")

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
