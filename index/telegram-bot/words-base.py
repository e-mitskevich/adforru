import json
import re
from collections import OrderedDict

import requests

sources = [
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-a-vse-slova.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-b.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-v.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-g.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-d.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-e.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-jo.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-zh.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-z.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-i.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-j.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-k.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-l.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-m.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-n.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-o.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-p.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-r.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-s.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-t.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-y.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-f.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-x.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-cs.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-ch.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-sh.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-sch.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-ji.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-je.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-jy.htm',
    'http://povto.ru/books/slovari/orfograficheskiy-slovar-online/orfograficheskii-slovar-online-bukva-ja.htm'
]

words = OrderedDict()


def add_from_source(url, is_additional=False):
    print("Fetching " + url if not is_additional else "Fetching ADDITIONAL " + url)
    content = str(requests.get(url).content, "utf-8").lower()


    count0 = len(words)
    local_words = re.findall("<big>(.*?)<b>(.*?)</b>(.*?)</big>", content)
    for word_pieces in local_words:
        if word_pieces[0] == "":
            word_pieces = word_pieces[1:]
        if word_pieces[-1] == "":
            word_pieces = word_pieces[:-1]
        word = "".join(word_pieces)

        if word not in words:
            words[word] = word_pieces
    print("%s words" % (len(words) - count0))

    count0 = len(words)
    local_words = re.findall("<big>(.*?)</big>", content)
    # print(local_words[0])
    for word in local_words:
        if "<b>" not in word and word not in words:
            words[word] = word
    print("%s words" % (len(words) - count0))

    relative_url_parts = url.split("/")[-1].split(".")[0].split("-")
    relative_url_part = relative_url_parts[-2] + "-" + relative_url_parts[-1]

    additional_urls = set()
    for additional_url in re.findall("\"((.*?)%s_(.*?))\"" % relative_url_part, content, re.MULTILINE):
        additional_url = additional_url[0].split("#")[0]
        if not additional_url.startswith("http://"):
            additional_url = "http://povto.ru/books/slovari/orfograficheskiy-slovar-online/" + additional_url
        additional_urls.add(additional_url)

    if additional_urls:
        print("%s additional urls" % len(additional_urls))
        for additional_url in additional_urls:
            add_from_source(additional_url, True)


for source in sources:
    add_from_source(source)

print(words.get("аэропорт"))

if words:
    with open('words.json', 'w') as f:
        f.write(json.dumps(words))

with open('words.json', 'r') as f:
    words = json.load(f)
print(words.get("брюзга"))
