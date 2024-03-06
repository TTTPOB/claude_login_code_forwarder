# Anthropic Email Forwarder

claude.ai won't let me login using email and password, so I have to use login code. I hate check email, so...

This program monitors an email inbox for messages from Anthropic and forwards the mail subject to telegram channel.

## Usage

Create a `config.toml` file with the following structure:

```toml
[email]
host = "imap.example.com"
user = "your_email@example.com"
password = "notsecure"

[telegram]
api_id = "123456"
api_hash = "xxyyaabb"
bot_token = "123456:xxxxxx"
channel_id = -123456789
```

Run the program using the following command:

```
python -m claude_login_code -c /path/to/config.toml
```

The program will continuously monitor your email inbox and forward Anthropic messages to the specified Telegram channel.

A `Dockerfile` is included, in case you want to run it in container.

## Configuration

The `config.toml` file contains the necessary configuration options:

- `[email]` section:
  - `host`: IMAP host address of your email provider
  - `user`: Your email address
  - `password`: Your email account password, likley to be an app password

- `[telegram]` section:
  - `api_id`: Your Telegram API ID
  - `api_hash`: Your Telegram API hash
  - `bot_token`: Token of the Telegram bot for forwarding messages
  - `channel_id`: ID of the Telegram channel to forward messages to

## License

This project is licensed under the [MIT License](LICENSE).
