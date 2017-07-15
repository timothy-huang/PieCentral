#!/usr/bin/env python3

"""
Watch `PieCentral` for pull requests and flashes devices for testing purposes.
"""

import atexit
from base64 import b64encode
import datetime
import json
import logging
import queue
import sched
import sys
import threading
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlencode

import pytz

LOGGER = logging.getLogger()

# Set with GitHub username and personal access token (`https://github.com/settings/tokens`)
GITHUB_USER = None
GITHUB_TOKEN = None

REPO_OWNER = 'pioneers'
REPO_NAME = 'PieCentral'

API_BASE_URL = 'https://api.github.com'
API_BASE_ENDPOINT = '/repos/{owner}/{repo}/'.format(owner=REPO_OWNER, repo=REPO_NAME)

LOCAL_TZ = pytz.timezone('America/Los_Angeles')

PRODUCER_INTERVAL = 300  # seconds


def send_request(endpoint, user=GITHUB_USER, token=GITHUB_TOKEN, **parameters):
    if parameters:
        endpoint = endpoint + '?' + urlencode(parameters)
    request = Request(urljoin(API_BASE_URL, endpoint))
    if user is not None and token is not None:
        credentials = (user + ':' + token).encode('utf-8')
        credentials = b64encode(credentials).decode('utf-8')
        request.add_header('Authorization', 'Basic ' + credentials)
    with urlopen(request) as response:
        LOGGER.debug('Made request to: %s', endpoint)
        return json.load(response)


def localize_timestamp(utc_dt):
    return LOCAL_TZ.normalize(utc_dt.replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ))


def iso_to_utc(iso_dt_str):
    return datetime.datetime.strptime(iso_dt_str, '%Y-%m-%dT%H:%M:%SZ')


def recent(local_timestamp):
    now = localize_timestamp(datetime.datetime.utcnow())
    time_elapsed = (now - local_timestamp).total_seconds()
    return 0 <= time_elapsed < PRODUCER_INTERVAL


def is_relevant_file(file_data):
    filename = file_data['filename']
    return filename.startswith('hibike') and filename.endswith('cpp')


def is_relevant_commit(commit):
    timestamp = localize_timestamp(iso_to_utc(commit['commit']['committer']['date']))
    if not recent(timestamp):
        return False

    endpoint = urljoin(API_BASE_ENDPOINT, 'commits/{sha}'.format(sha=commit['sha']))
    return any(map(is_relevant_file, send_request(endpoint)['files']))


def is_relevant_pull_request(pull_request):
    update_timestamp = localize_timestamp(iso_to_utc(pull_request['updated_at']))
    if not recent(update_timestamp) or pull_request['state'] != 'open':
        return False

    endpoint = 'pulls/{number}/commits'.format(number=pull_request['number'])
    endpoint = urljoin(API_BASE_ENDPOINT, endpoint)
    return any(map(is_relevant_commit, send_request(endpoint)))


def produce_pull_requests(scheduler, pr_queue):
    LOGGER.info('Scanning GitHub ...')
    pull_requests = send_request(urljoin(API_BASE_ENDPOINT, 'pulls'))
    for pull_request in filter(is_relevant_pull_request, pull_requests):
        message = 'Pushing job for pull request {number} ...'
        LOGGER.info(message.format(number=pull_request['number']))
        pr_queue.put(pull_request)

    LOGGER.info('Scan complete')
    scheduler.enter(PRODUCER_INTERVAL, 1, produce_pull_requests,
                    argument=(scheduler, pr_queue))


def test_branch(head_branch):
    pass


def consume_pull_requests(pr_queue, stop_event):
    while not stop_event.is_set():
        try:
            LOGGER.debug('Polling pull request queue ...')
            pull_request = pr_queue.get(timeout=1)  # Non-blocking
        except queue.Empty:
            LOGGER.debug('Pull request queue is empty.')
            continue

        *_, head_branch = pull_request['head']['label'].split(':')
        message = 'Processing pull request {number} (head: "{head}") ...'
        LOGGER.info(message.format(number=pull_request['number'],
                                   head=head_branch))

        test_branch(head_branch)
        pr_queue.task_done()


def terminate(consumer_thread, stop_event):
    LOGGER.info('Waiting for consumer thread to terminate ...')
    stop_event.set()
    consumer_thread.join()
    LOGGER.info('Consumer thread stopped.')
    LOGGER.info('Terminating logging ...')
    logging.shutdown()


def main():
    # Switch to `logging.INFO` for less noisy output
    logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s',
                        level=logging.DEBUG, stream=sys.stdout)
    LOGGER.info('Root logger initialized')

    pr_queue = queue.Queue()
    stop_event = threading.Event()

    consumer_thread = threading.Thread(target=consume_pull_requests, name='',
                                       args=(pr_queue, stop_event))
    consumer_thread.start()
    atexit.register(terminate, consumer_thread, stop_event)

    scheduler = sched.scheduler()
    produce_pull_requests(scheduler, pr_queue)

    try:
        scheduler.run()
    except KeyboardInterrupt:
        terminate(consumer_thread, stop_event)


if __name__ == '__main__':
    main()
