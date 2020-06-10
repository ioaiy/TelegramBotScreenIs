# Alternative to these resources
# https://www.browserstack.com/
# http://browsershots.org/
# https://www.codeinwp.com/blog/best-website-screenshot-tools/

# TO-DO LIST
# Add new browsers from the selenium webdrider list
# Add headless mode for Firefox
#
import os
import validators
import telebot
from selenium import webdriver

# SELENIUM - configure the browser to work correctly in headless mode
# Preferences for Google Chrome
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('--headless')
OPTIONS.add_argument('--disable-gpu')
OPTIONS.add_argument('--disable-dev-shm-usage')
OPTIONS.add_argument('--no-sandbox')
OPTIONS.add_argument("--disable-notifications")

# TELEGRAM - create a bot
TOKEN = 'Your token'
BOT = telebot.TeleBot(TOKEN, threaded = False)

# MESSAGE FROM USER
def find_at(msg):
    for text in msg:
        if 'https' in text:
            return text


def TeleBot_message(message, msg):
    BOT.send_message(chat_id=message.chat.id, text=msg)


def Next_Step(message, step):
    BOT.register_next_step_handler(message, step)


# Implementation of required /start and /help commands
@BOT.message_handler(commands=['start'])
def hello_user(message):
    info = "Write the command /help \nTo find out how you can get your png image."
    BOT.send_message(message.chat.id, 'Hello, ' + message.from_user.username + "! \n\n" + info)


@BOT.message_handler(commands=['help'])
def show_help(message):
    BOT.send_message(message.chat.id, 'To get screenshots of the webpage, send me your link. '
                                      'Copy it from your browser\'s address bar.\n\nExample:\nhttps://go-gl.com/jjf')
    TeleBot_message(message, 'Select one of the browsers /google /firefox')


@BOT.message_handler(content_types=['text'])
def get_start(message):
    if message.text == '/google':
        # Chrome(message)
        TeleBot_message(message, 'Enter the link for Google Chrome')
        Next_Step(message, Chrome)
    elif message.text == '/firefox':
        # Firefox(message)
        TeleBot_message(message, 'Enter the link for Mozilla Firefox')
        Next_Step(message, Firefox)
    else:
        TeleBot_message(message, 'Select one of the browsers /google /firefox')
        Next_Step(message, get_start)

def Chrome(message):
    if message.text == '/firefox':
        # Firefox(message)
        TeleBot_message(message, 'Paste your link for Firefox')
        Next_Step(message, Firefox)
    else:
        texts = message.text.split()
        at_text = find_at(texts)
        url = f'{at_text}'
        uid = message.chat.id
        if not validators.url(url):
            TeleBot_message(message, 'URL is invalid for Google Chrome! Try again')
            Next_Step(message, Chrome)
        else:
            BOT.send_message(uid, 'Please, wait...')
            photo_path = str(uid) + '.png'
            driver = webdriver.Chrome(
                executable_path="D:/WebDrivers/chromedriver_win32/chromedriver.exe",
                options=OPTIONS)
            driver.set_window_size(1280, 720)
            driver.get(url)
            driver.save_screenshot(photo_path)
            BOT.send_photo(uid, photo = open(photo_path, 'rb'))
            driver.quit()
            os.remove(photo_path)
        TeleBot_message(message, 'Paste the link or change your Google Chrome browser to another')
        Next_Step(message, Chrome)

def Firefox(message):
    if message.text == '/google':
        # Chrome(message)
        TeleBot_message(message, 'Paste your link for Chrome')
        Next_Step(message, Chrome)
    else:
        texts = message.text.split()
        at_text = find_at(texts)
        url = f'{at_text}'
        uid = message.chat.id
        if not validators.url(url):
            BOT.send_message(uid, 'URL is invalid for Mozilla Firefox! Try again')
            Next_Step(message, Firefox)
        else:
            BOT.send_message(uid, 'Please, wait...')
            photo_path = str(uid) + '.png'
            profile = webdriver.FirefoxProfile('C:/Users/dsyug/AppData/Local/Mozilla/Firefox/Profiles/hruw1vcp.default')
            driver = webdriver.Firefox(firefox_profile=profile,
                                       executable_path="D:/WebDrivers/geckodriver-v0.24.0-win64/geckodriver.exe")
            driver.set_window_size(1280, 720)
            driver.get(url)
            driver.save_screenshot(photo_path)
            BOT.send_photo(uid, photo=open(photo_path, 'rb'))
            driver.quit()
            os.remove(photo_path)
        TeleBot_message(message, 'Paste the link or change your Mozilla Firefox browser to another')
        Next_Step(message, Firefox)


# # Getting a screenshot of the website using selenium and headless chrome
# @BOT.message_handler(func=lambda msg: msg.text is not None and 'ht' in msg.text)
# def at_answer(message):
#     texts = message.text.split()
#     at_text = find_at(texts)
#     url = f'{at_text}'
#     uid = message.chat.id
#     if not validators.url(url):
#         BOT.send_message(uid, 'URL is invalid!')
#     else:
#         BOT.send_message(uid, 'Please, wait...')
#         photo_path = str(uid) + '.png'
#         driver = webdriver.Chrome(executable_path="D:/WebDrivers/chromedriver_win32/chromedriver.exe", options=OPTIONS)
#         driver.set_window_size(1280, 720)
#         driver.get(url)
#         driver.save_screenshot(photo_path)
#         BOT.send_photo(uid, photo = open(photo_path, 'rb'))
#         driver.quit()
#         os.remove(photo_path)


 # Run the bot
if __name__ == '__main__':
    BOT.infinity_polling()