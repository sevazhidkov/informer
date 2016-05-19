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

weather_base = 'http://api.openweathermap.org/data/2.5/weather?id={}&APPID={}&units=metric'
weather_url = weather_base.format(
    os.environ.get('WEATHER_CITY', 471430),
    os.environ.get('WEATHER_API_KEY')
)

todoist_api = todoist.TodoistAPI()
todoist_api.login(os.environ['TODOIST_LOGIN'], os.environ['TODOIST_PASSWORD'])

CALORIES_PER_SECOND = 0.06805555555
moves_token = os.environ['MOVES_ACCESS_TOKEN']
moves_data_url = 'https://api.moves-app.com/api/1.1/user/summary/daily/{}'

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
    if tasks_num == 0:
        comment = 'Nice!'
    else:
        comment = 'Work!'
    device.print_rows('Today tasks: {}'.format(tasks_num), comment)


def moves_informer(device):
    localtime = time.localtime()
    date = '{}-{}-{}'.format(localtime.tm_year,
                             str(localtime.tm_mon).rjust(2, '0'),
                             str(localtime.tm_mday).rjust(2, '0'))
    moves_data = json.loads(requests.get(
        moves_data_url.format(date), headers={
            'Authorization': 'Bearer {}'.format(moves_token)
        }).text
    )[0]
    if not moves_data['summary']:
        device.print_rows('No steps!', 'GO TO THE WALK!')
        return
    device.print_rows('Steps: {}'.format(moves_data['summary'][0]['steps']),
                      'Distance: {} m'.format(moves_data['summary'][0]['distance']))
    time.sleep(5)
    device.print_rows('Calories burnt:', '{} kk'.format(
        int(moves_data['summary'][0]['duration']) * CALORIES_PER_SECOND
    ))


def twitter_informer(device):
    localtime = time.localtime()
    date = '{}-{}-{}'.format(localtime.tm_year, localtime.tm_mon, localtime.tm_yday)
    mentions_num = json.loads(requests.get(loklak_url + date).text)['search_metadata']['count']
    device.print_rows('Twitter mentions:', str(mentions_num))
