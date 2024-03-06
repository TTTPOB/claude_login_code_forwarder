import argparse
import logging
import asyncio

import toml
from telethon import TelegramClient, events

from .main import *

l = logging.getLogger(__name__)
l.setLevel(logging.INFO)
l.addHandler(logging.StreamHandler())

parser = argparse.ArgumentParser(description="Email to Telegram Forwarder")
parser.add_argument(
    "-c", "--config-file", default="config.toml", help="Path to the configuration file"
)
args = parser.parse_args()

# Load the configuration from the TOML file
with open(args.config_file, "r") as f:
    config = toml.load(f)

# Create a Telegram client
client = TelegramClient(
    "bot", config["telegram"]["api_id"], config["telegram"]["api_hash"]
)
l.info("Telegram client started")

imap_client = email_login(config)
l.info("Email client started")


asyncio.run(listen_email_and_forward(config, client, imap_client))
