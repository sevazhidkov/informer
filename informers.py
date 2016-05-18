import os
import time
import dateutil.parser
import dateutil.tz
import json
import requests
import vk_api
import todoist


def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


vk_session = vk_api.VkApi(os.environ['VK_LOGIN'], os.environ['VK_PASSWORD'],
                          captcha_handler=captcha_handler)
vk_session.authorization()
vk = vk_session.get_api()

weather_base = 'http://api.openweathermap.org/data/2.5/weather?id={}&appid={}&units=metric'
weather_url = weather_base.format(
    os.environ.get('WEATHER_CITY', 471430),
    os.environ.get('WEATHER_API_KEY')
)

todoist_api = todoist.TodoistAPI()
todoist_api.login(os.environ['TODOIST_LOGIN'], os.environ['TODOIST_PASSWORD'])

loklak_base = 'http://loklak.org/api/search.json?timezoneOffset=-240&q=%40{}+since%3A'
loklak_url = loklak_base.format(os.environ.get('TWITTER_NAME', 'sevazhidkov'))


def time_informer(device):
    device.print_rows('Today:', time.strftime('%c'))


def vk_informer(device):
    response = vk.messages.getDialogs(unread=1)
    device.print_rows('New VK messages:', str(response['count']))


def weather_informer(device):
    response = requests.get(weather_url)
    weather = json.loads(response.text)
    device.print_rows(
        'Temperature: ' + str(weather['main']['temp']),
        weather['weather'][0]['description'].capitalize()
    )


def todoist_informer(device):
    todoist_api.items.sync()
    items = todoist_api.items.all()
    tasks_num = 0
    for item in items:
        if item.data['due_date_utc'] is None:
            continue
        utc_date = dateutil.parser.parse(item.data['due_date_utc'])
        if utc_date.astimezone(dateutil.tz.tzlocal()).day == time.localtime().tm_yday:
            tasks_num += 1
    device.print_rows('Today tasks:', str(tasks_num))


def twitter_informer(device):
    localtime = time.localtime()
    date = '{}-{}-{}'.format(localtime.tm_year, localtime.tm_mon, localtime.tm_yday)
    mentions_num = json.loads(requests.get(loklak_url + date).text)['search_metadata']['count']
    device.print_rows('Twitter mentions:', str(mentions_num))
