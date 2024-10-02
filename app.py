import requests as r
from flask import Flask, abort
from pyhocon import ConfigFactory
import redis

rd = redis.Redis(host='localhost', port=6379, decode_responses=True)

conf = ConfigFactory.parse_file('resources/app.conf')

host = conf.get_string('test.app.server.host')
port = conf.get_int('test.app.server.port')

app = Flask(__name__)


@app.route("/<page>")
def hello_world(page):
    cached_page = rd.get(page)

    if cached_page:
        return cached_page

    try:
        response = r.get(f"https://ru.wikipedia.org/wiki/{page}")
        print(response.raise_for_status())
    except r.RequestException:
        abort(404)

    rd.set(page, response.content)

    return response.content


if __name__ == '__main__':
    app.run(host=host, port=port)
