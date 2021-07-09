import http.client
import json
import time

while True:
    conn = http.client.HTTPSConnection('boards.4chan.org')
    conn.request('GET', '/b/catalog')

    resp = conn.getresponse().read()
    resp = resp[resp.index(b'var catalog =') + 14 : resp.index(b':15};') + 4]
    resp = json.loads(resp).get('threads')

    ids = []
    for thread in resp:
        if 'loli' in resp.get(thread).get('teaser').lower():
            ids.append(thread)

    for id in ids:
        conn.request('GET', '/b/thread/' + id)
        resp = conn.getresponse()

        if resp.status == 200:
            with open('serve/thread/' + id + '.html', 'wb') as thread:
                thread.write(resp.read())

    conn.close()
    time.sleep(120)
