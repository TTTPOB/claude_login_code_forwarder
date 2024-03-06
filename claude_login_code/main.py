import email
import imaplib2
import logging
import re

l = logging.getLogger(__name__)
l.setLevel(logging.INFO)
l.addHandler(logging.StreamHandler())


def mark_email_as_read(imap_client, num):
    imap_client.store(num, "+FLAGS", "\\Seen")


def process_email(from_email, subject, body):
    msg =  f"\nFrom: {from_email}\nSubject: {subject}"
    # wrap number in subject with '`'
    msg = re.sub(r'(\d+)', r'`\1`', msg)
    return msg


def get_email_details(email_message):
    # Extract email details
    subject = email_message["Subject"]
    from_email = email_message["From"]
    body = ""

    # Get the email body
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = email_message.get_payload(decode=True).decode()

    return subject, from_email, body


def filter_email(email):
    from_email = email["From"]
    if from_email.endswith(".anthropic.com>"):
        return True
    return False


def email_login(config):
    imap_client = imaplib2.IMAP4_SSL(config["email"]["host"])
    imap_client.login(config["email"]["user"], config["email"]["password"])
    imap_client.select("inbox")
    return imap_client


def email_generator(imap_client: imaplib2.IMAP4_SSL):
    while True:
        # Start IDLE mode
        imap_client.idle()

        # Wait for new emails
        _, data = imap_client.search(None, "UNSEEN")  # Change the condition as needed

        for num in data[0].split():
            _, fetched = imap_client.fetch(num, "(RFC822)")
            for item in fetched:
                if isinstance(item, tuple) and len(item) == 2 and "RFC822" in item[0].decode():
                    raw_email = item[1]
                    break
            email_message = email.message_from_bytes(raw_email)
            l.info(f"New email arrived: {email_message}")
            if filter_email(email_message):
                yield email_message, num


async def listen_email_and_forward(config, client, imap_client):
    await client.start(bot_token=config["telegram"]["bot_token"])
    async with client:
        for email_message, num in email_generator(imap_client):
            subject, from_email, body = get_email_details(email_message)
            # Process the email content
            message = process_email(from_email, subject, body)

            if message:
                # Forward the email to Telegram
                await client.send_message(config["telegram"]["channel_id"], message, parse_mode="markdown")
                l.info("Email forwarded to Telegram")

            # Mark the email as read
            mark_email_as_read(imap_client, num)
