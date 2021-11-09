from email import message_from_bytes
from email.header import decode_header
from imaplib import IMAP4_SSL


async def get_inbox(username: str, password: str, host='imap.gmail.com', path='') -> list:
    mail = IMAP4_SSL(host)
    try:
        mail.login(username, password)
    except BaseException:
        return []
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    my_message = []
    # go over unread messages
    for num in search_data[0].split():
        email_data = {}
        # take message and get info about it
        email_message = message_from_bytes(mail.fetch(num, '(RFC822)')[1][0][1])
        try:
            for i, part in enumerate(email_message.walk()):
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()

                filename = part.get_filename()
                if filename:
                    filename_decode, encoding = decode_header(filename)[0]

                    if email_data.get('files') is None:
                        email_data['files'] = []
                    email_data['files'] += [path + f'{i}_' + filename_decode.decode()]

                    with open(path + f'{i}_' + filename_decode.decode(), 'wb') as new_file:
                        new_file.write(part.get_payload(decode=True))

            my_message.append(email_data)
        except UnicodeDecodeError:
            continue
    return [await reformat_mail(message) for message in my_message]


async def reformat_mail(message: dict) -> dict:
    symbols = ['\n', '\r', '\t', '\xa0', '\u200e']
    parse_message = {}
    for key, value in message.items():
        for symbol in symbols:
            while symbol * 2 in key:
                key = key.replace(symbol * 2, symbol)
            while symbol * 2 in value:
                value = key.replace(symbol * 2, symbol)
        parse_message[key] = value
    return parse_message
