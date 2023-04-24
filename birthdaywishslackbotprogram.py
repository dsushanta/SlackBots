import random
import ssl
import certifi
# from slack import WebClient
from slack_sdk import WebClient
from datetime import date, datetime


def getCurrentDay():
    today = date.today()
    return today.day


def getCurrentMonth():
    today = date.today()
    return today.month


def getDisplayNamesOfBirthdayPersons():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    slack_client = WebClient(BOT_TOKEN, ssl=ssl_context)
    slack_client_without_bot_token = WebClient(AUTH_TOKEN, ssl=ssl_context)
    # slack_client = WebClient(BOT_TOKEN)
    # slack_client_without_bot_token = WebClient(AUTH_TOKEN)
    slack_client.rtm_connect()
    user_list_str = slack_client.users_list()
    users = user_list_str.get('members')
    for user in users:
        try:
            status = user.get('deleted')
            if status:
                continue
            is_bot = user.get('is_bot')
            if is_bot:
                continue
            user_id = user.get('id')
            name = user.get('name')
            first_name = user.get('profile').get('first_name')
            user_info = slack_client_without_bot_token.users_profile_get(user=user_id)
            bday_string = user_info.get('profile').get('fields').get('XfNVGXDAS1').get('value')
            date_object = datetime.strptime(bday_string, BIRTHDAY_FORMAT).date()
            day = date_object.day
            month = date_object.month

            if month == getCurrentMonth() and day == getCurrentDay():
                birthday_persons['<@'+user_id+'>'] = first_name
        except AttributeError:
            print('User %s has not set birth date' % name)
            continue
        except ValueError:
            print('Invalid date format : %s , moving on ' % bday_string)
            continue


def postBirthdayWishes():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    slack_client = WebClient(BOT_TOKEN, ssl=ssl_context)
    # slack_client = WebClient(BOT_TOKEN)
    slack_client.rtm_connect()
    for id, first_name in birthday_persons.items():
        random_number = random.randint(0, len(MODIFIED_BIRTHDAY_WISHES)-1)
        birthday_wish = MODIFIED_BIRTHDAY_WISHES[random_number]
        random_number = random.randint(0, len(BIRTHDAY_IMAGE_URLS) - 1)
        image_url = BIRTHDAY_IMAGE_URLS[random_number]
        message = template.replace("REPLACE_WITH_WISH", birthday_wish)
        message = message.replace("REPLACE_WITH_IMAGE_URL", image_url)
        # message = message % (first_name, id)
        slack_client.chat_postMessage(
            channel=CHANNEL_NAME,
            blocks=message)

    # random_number = random.randint(0, len(MODIFIED_BIRTHDAY_WISHES)-1)
    # birthday_wish = MODIFIED_BIRTHDAY_WISHES[random_number]
    # random_number = random.randint(0, len(BIRTHDAY_IMAGE_URLS) - 1)
    # image_url = BIRTHDAY_IMAGE_URLS[random_number]
    # message = template.replace("REPLACE_WITH_WISH", birthday_wish)
    # message = message.replace("REPLACE_WITH_IMAGE_URL", image_url)
    # # message = message % (first_name, id)
    # idd = 'UK085LHE0'
    # namee = 'Sushant'
    # message = message % (namee, idd)
    # slack_client.chat_postMessage(
    #     channel=CHANNEL_NAME,
    #     blocks=message)


BIRTHDAY_FORMAT = '%Y-%m-%d'

# settings for TestVagrant
AUTH_TOKEN = 'xoxp-10189127591-646277697476-5144997657735-583d3f10cae0c7b829db7291f2775a38'
BOT_TOKEN = 'xoxb-10189127591-790313797619-T9Svt2q7pNSlpWvGFez5Wl5g'

# AUTH_TOKEN = 'xoxp-10189127591-646277697476-854700790421-1fa318a8c54d80b97c00250db5881b87'
# BOT_TOKEN = 'xoxb-10189127591-790313797619-ay83iRVEgYG5zkNKxLlN3Ix7'


# CHANNEL_NAME = 'general'
CHANNEL_NAME = 'testing-bday-slackbot'

template = ("["
	"{"
		"\"type\": \"image\","
		"\"title\": {"
			"\"type\": \"plain_text\","
			"\"text\": \"Birthday Image\","
			"\"emoji\": true"
		"},"
		"\"image_url\": \"REPLACE_WITH_IMAGE_URL\","
		"\"alt_text\": \"Birthday Image\""
	"},"
    "{"
		"\"type\": \"section\","
		"\"text\": {"
			"\"type\": \"mrkdwn\","
			"\"text\": \"REPLACE_WITH_WISH\""
		"}"
	"}"
"]")

BIRTHDAY_IMAGE_URLS = [
    'https://i.ibb.co/3F4djjD/pic-1.png',
    'https://i.ibb.co/wyWK5cX/pic-2.png',
    'https://i.ibb.co/L0wLRBb/pic-3.png',
    'https://i.ibb.co/rvvXp6b/pic-4.png',
    'https://i.ibb.co/J3h5zDQ/pic-5.png',
    'https://i.ibb.co/M2QCttL/pic-6.png',
    'https://i.ibb.co/pRM3Q4b/pic-7.png',
    'https://i.ibb.co/XC5nJzD/pic-8.png',
    'https://i.ibb.co/Rzn1GcV/pic-9.png',
    'https://i.ibb.co/r65nww0/pic-10.png',
    'https://i.ibb.co/BfjjXj4/pic-11.png',
    'https://i.ibb.co/zsTnkJF/pic-12.png',
    'https://i.ibb.co/SQPZ7K4/pic-13.png',
    'https://i.ibb.co/pwdy0VG/pic-14.png',
    'https://i.ibb.co/PWjgG9T/pic-15.png',
    'https://i.ibb.co/6DcV2tL/pic-16.png',
    'https://i.ibb.co/bRN7Nyg/pic-17.png',
    'https://i.ibb.co/VTYGHT0/pic-18.png',
    'https://i.ibb.co/X5M8s7R/pic-19.png',
    'https://i.ibb.co/S0bzdy8/pic-20.png',
    'https://i.ibb.co/vL5vgY3/pic-21.png'
]

BIRTHDAY_WISHES = [
    'Here’s to another year of success, health, and happiness. Happy Bday!',
    'We wish you a love and laughter-filled birthday. Keep being awesome.',
    'Happy birthday! Wishing you another year full of love, joy, and all your favourite things.',
    'May this lovely day bring happiness and new opportunities in your life. Wishing you the happiest birthday ever!',
    'Sending you warm birthday wishes and lots of love. May this birthday bring you success and happiness.',
    'Happy Birthday! We wish you abundance, happiness, and health.',
    'Have a wonderful birthday. Another adventurous year full of prosperity and happiness awaits you! ',
    'Live your life to the fullest and enjoy every moment of your life. A very happy birthday to you.',
    'Happy Birthday! May you receive the greatest of joys and everlasting bliss.',
    'Happy birthday and many happy returns of the day! We hope this magical day brings you countless joy and laughter. Have a lovely day and a wonderful life ahead.',
    'May your day be filled with happiness and joy and may the years ahead bring you lots of success and prosperity. Happy Birthday!',
    'We hope that you achieve all the goals and successes that you desire for. Happy birthday!',
    'As you step into another year of your life, we wish you all the happiness and success. A very happy birthday to you.',
    'Happy Birthday! May all your wishes come true.',
    'May this day make all your dreams come true and keep your heart brimming with joy. Happy birthday!',
    'Happy Birthday! May your life be filled with abundant joy and blessings this year!',
    'Wishing you a lovely birthday and a great life ahead. Keep smiling!',
    'May your birthday be filled with lovely, sweet, and cherished memories. Happy Birthday!',
    'Wishing you the loveliest, most joyful birthday ever! Happy Birthday.',
    'Happy birthday! Wishing you a splendid year ahead. May peace and happiness always be with you.'
]
MODIFIED_BIRTHDAY_WISHES = [wish + " @channel Let us all wish %s a great birthday. :birthday: - %s " for wish in BIRTHDAY_WISHES]
birthday_persons = {}

BIRTHDAY_WISHES = []            # This is to clear data from an unused list
getDisplayNamesOfBirthdayPersons()
postBirthdayWishes()
