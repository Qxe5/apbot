import http.client
import json
import time
import os.path

while True:
    for board in ['/b/', '/soc/']:
        conn = http.client.HTTPSConnection('boards.4chan.org')
        conn.request('GET', board + 'catalog')

        resp = conn.getresponse().read()
        resp = resp[resp.index(b'{"threads"') : resp.index(b':15};') + 4]
        resp = json.loads(resp).get('threads')

        ids = []
        for thread in resp:
            post = resp.get(thread).get('teaser').lower()

            keywords = ['loli', 'shota', 'wickr']
            if any([keyword in post for keyword in keywords]):
                ids.append(thread)

        for id in ids:
            conn.request('GET', board + 'thread/' + id)
            resp = conn.getresponse()

            if resp.status == 200:
                filepath = 'serve/thread' + board + id + '.html'

                if not os.path.exists(filepath):
                    print('Creating ' + id + ' ...', end = ' ')
                else:
                    print('Updating ' + id + ' ...', end = ' ')
                print('[' + board + ']')

                with open(filepath, 'wb') as thread:
                    thread.write(resp.read())

    conn.close()
    time.sleep(120)
