#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# coding=utf-8
import datetime
import json
import logging
import signal
import sys

import requests
import yaml
from lxml import html

CONFIG_FILE = "matterbot-kuchnia.yml"
DATA_DIR = 'data'
FB_API_VERSION = '2.7'

log = logging.getLogger(__name__)


def main():
    setup_logging()
    log.info("Matterbot Kuchnia Domowa started")
    install_interrupt_handler()
    config = load_config()
    check_post(config)


def load_config():
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    log.debug("Config loaded")
    return config


def check_post(config):
    mm_config = config['mattermost']
    integration = config['kuchnia']
    url = "http://www.barexpres.pl"
    log.info("Checking: %s" % url)
    last_post_text = get_today_menu(url)
    if last_post_text:
        log.info("Post: " + last_post_text)
        username = integration.get('mm_username')
        icon_url = integration.get('mm_icon_url')
        basic_auth = mm_config.get('basic_auth')
        data = json.dumps({'username': username, 'text': last_post_text, 'icon_url': icon_url})
        webhook_url = mm_config['webhook_url']
        requests.post(webhook_url, data=data, auth=to_tuple(basic_auth))
    else:
        log.info("No menu for today")

def get_today_menu(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    weekday = datetime.datetime.today().weekday()
    if weekday < 5:
        lunch_sets_titles = tree.xpath('//td[@class="zestaw"]/text()')
        lunch_sets_contents = tree.xpath('//td[@class="tabela_rozmiar"]//text()[normalize-space()]')
        lunch_sets_prices = tree.xpath(
            '//td[@class="tabela_rozmiar"]/following-sibling::td//text()[normalize-space()][contains(.,"z")]')
        first_set = weekday * 2
        second_set = weekday * 2 + 1
        last_post_text = lunch_sets_titles[first_set] + ": " + lunch_sets_contents[first_set] + " - " + \
                         lunch_sets_prices[first_set] + "\n" + lunch_sets_titles[second_set] + ": " + \
                         lunch_sets_contents[second_set] + " - " + lunch_sets_prices[second_set]
    else:
        last_post_text = None
    return last_post_text


def to_tuple(basic_auth):
    return tuple(basic_auth.values()) if basic_auth is not None else None


def install_interrupt_handler():
    signal.signal(signal.SIGINT, signal_handler)
    log.info('Press Ctrl+C or send SIGINT to exit')


def signal_handler(sig, frame):
    log.info('SIGINT received! Bye!')
    sys.exit(0)


def setup_logging():
    logging.basicConfig(format='%(asctime)s [%(module)s] %(message)s')
    log.setLevel(logging.INFO)


main()
