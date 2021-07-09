import http.client
import json
import time
import os.path

while True:
    conn = http.client.HTTPSConnection('boards.4chan.org')
    conn.request('GET', '/b/catalog')

    resp = conn.getresponse().read()
    resp = resp[resp.index(b'var catalog =') + 14 : resp.index(b':15};') + 4]
    resp = json.loads(resp).get('threads')

    ids = []
    for thread in resp:
        post = resp.get(thread).get('teaser').lower()

        if 'loli' in post or 'shota' in post:
            ids.append(thread)

    for id in ids:
        conn.request('GET', '/b/thread/' + id)
        resp = conn.getresponse()

        if resp.status == 200:
            filepath = 'serve/thread/' + id + '.html'

            if not os.path.exists(filepath):
                print('Creating ' + id + ' ...')
            else:
                print('Updating ' + id + ' ...')

            with open(filepath, 'wb') as thread:
                thread.write(resp.read())

    conn.close()
    time.sleep(120)
