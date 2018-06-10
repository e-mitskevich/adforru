#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re

import sys
import telepot
import time
from telepot.loop import MessageLoop


CHAT_ID_EUGENE_MITSKEVICH = 136483796
CHAT_ID_TEST_GROUP = -278932543
CHAT_ID_KRASIVO = -304487349


with open('config.json', 'r') as f:
    config = json.load(f)
    TOKEN = config['token']
    PASSWORD = config['password']


with open('words.json', 'r') as f:
    words_base = json.load(f)


GLASNYE = ["а", "о", "и", "е", "ё", "э", "ы", "у", "ю", "я"]
HUI_MAPPING = {
    "а": "я",
    "о": "ё",
    "э": "е",
    "ы": "и",
    "у": "ю"
}


def to_slogs(word):
    slogs = []
    current_slog = ""
    current_slog_has_glasnye = False
    index = 0
    for char in word:
        if (index == 0 or (char in GLASNYE) or not current_slog_has_glasnye) and not (char in GLASNYE and current_slog_has_glasnye):
            current_slog += char
        else:
            slogs.append(current_slog)
            current_slog = char
            current_slog_has_glasnye = False

        if char in GLASNYE:
            current_slog_has_glasnye = True
        # print(current_slog)

        if index == len(word) - 1 and current_slog not in slogs:
            if current_slog_has_glasnye:
                slogs.append(current_slog)
            else:
                slogs[-1] = slogs[-1] + current_slog
        index += 1
    return slogs


def get_rifma(text, words):

    if text.endswith("кто?"):
        return "Конь в пальто!"
    if text.endswith("нет"):
        return "Нет - пидора ответ!"
    if "300" in words or "триста" in words:
        return "Триста - отсоси у тракториста!"

    for i in range(1, min(5, len(words)) + 1):
        word = words[-i]
        slogs = to_slogs(word)
        print(word + " -> " + str(slogs))
        if len(slogs) != 3 or word.endswith("й") or word not in words_base:
            continue

        print(words_base[word])

        udarenie_na_vtoroi = not list(filter(lambda piece: slogs[1] in piece, words_base[word]))
        if udarenie_na_vtoroi:
            glasnaya = slogs[-2][-1]
            return word + " - ху" + HUI_MAPPING.get(glasnaya, glasnaya) + slogs[-1] + "!"

        glasnaya = slogs[0][-1]
        if len(slogs) > 3:
            slogs = [slogs[0]] + slogs[-2:]
            glasnaya = "ё"
        slogs_rest = len(slogs) - 1
        return word + " - ху" + HUI_MAPPING.get(glasnaya, glasnaya) + "".join(slogs[-slogs_rest:]) + "!"

    return None


def handle(msg):
    try:
        print("==============")
        # print("Message: " + str(msg))
        content_type, chat_type, chat_id = telepot.glance(msg)
        text = msg["text"] if 'text' in msg else msg.get('caption', '')
        text = text.lower()

        words = re.findall("[а-яА-Я0-9]+", text)
        if words:
            bot.forwardMessage(CHAT_ID_TEST_GROUP, chat_id, msg['message_id'])
            # bot.sendMessage(CHAT_ID_TEST_GROUP, ",".join(to_slogs(last_word)), parse_mode="HTML")

            response = get_rifma(text, words)
            if response is not None:
                bot.sendMessage(CHAT_ID_TEST_GROUP, response, parse_mode="HTML")
    except Exception as exc:
        print("EXCEPTION: " + exc)


bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')
# Keep the program running.
while 1:
    time.sleep(10)
