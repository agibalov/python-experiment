import sys

import requests
from eliot import start_action, add_destinations, log_call
from eliottree import render_tasks, tasks_from_iterable

messages = []


def collect_messages(message):
    messages.append(message)


add_destinations(collect_messages)


@log_call
def get_some_data(url):
    requests.get(url)

try:
    with start_action(action_type='SomeOuterAction', x=123) as action:
        action.log(message_type='my_dummy_message', text='something is about to happen')
        url = 'http://4ut23y74283ty872y3t47823t.com/'
        with start_action(action_type='SomeInnerAction', url=url):
            get_some_data(url)
except:
    render_tasks(sys.stdout.write, tasks_from_iterable(messages), colorize=True)
