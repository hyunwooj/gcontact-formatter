import re
import atom
import gdata.contacts.data
import gdata.contacts.client
from phonenumbers import parse, format_number, PhoneNumberFormat


class PhoneNumberPattern(object):
    def __init__(self, regex, nation):
        self.regex = re.compile(regex)
        self.nation = nation

    def match(self, number):
        return self.regex.match(number)

    def format(self, number):
        return format_number(parse(number, self.nation), PhoneNumberFormat.INTERNATIONAL)

def get_contacts(gd_client):
    feed = gd_client.GetContacts()
    entries = feed.entry

    next_link = feed.GetNextLink()
    while next_link:
        feed = gd_client.GetContacts(uri=next_link.href)
        entries += feed.entry
        next_link = feed.GetNextLink()

    return entries

def update(gd_client, entries, patterns):
    for entry in entries:
        for number in entry.phone_number:
            for pattern in patterns:
                if pattern.match(number.text):
                    prev = number.text
                    number.text = pattern.format(number.text)
                    try:
                        gd_client.Update(entry)
                    except:
                        gd_client.Update(entry)
                    print prev, '=>', number.text
                    break
            else:
                print '[FAIL]:', entry.title.text, number.text

def run():
    email = 'youremail@gmail.com'
    password = 'password'

    gd_client = gdata.contacts.client.ContactsClient(source='phone number formatter')
    gd_client.ClientLogin(email, password, gd_client.source)

    entries = get_contacts(gd_client)

    patterns = [
        PhoneNumberPattern(r'^(\+82)?(-|\s)?0?(2|31|42|43|10|11|16|70)(-|\s)?[\d]{3,4}(-|\s)?[\d]{4}$', 'KR'),
        PhoneNumberPattern(r'^\/\/(010|011)[\d]{8}$', 'KR'),
        PhoneNumberPattern(r'^(1|\+1)?(-|\s)?\(?[^0][\d]{2}\)?(-|\s)?[\d]{3}(-|\s)?[\d]{4}$', 'US'),
    ]
    update(gd_client, entries, patterns)

if __name__ == "__main__":
    run()
