#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
import traceback

import telepot
import time
from telepot.loop import MessageLoop


CHAT_ID_EUGENE_MITSKEVICH = 136483796
CHAT_ID_KRASIVO = -304487349


base_dir = os.path.dirname(__file__)


with open(os.path.join(base_dir, 'config.json'), 'r') as f:
    config = json.load(f)
    TOKEN = config['token']
    PASSWORD = config['password']


with open(os.path.join(base_dir, 'words.json'), 'r') as f:
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


def get_udarnyi_slog(word, slogs):
    i = 0
    while i < len(slogs):
        if not list(filter(lambda piece: slogs[i] in piece, words_base[word])):
            break
        i += 1
    return i + 1


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

        # print(word + " -> " + "".join(slogs))
        print("Word exists: %s" % (word in words_base))

        if len(slogs) not in (2, 3) or word.endswith("й") or word not in words_base:
            continue

        rifma = None
        udarnyi_slog = get_udarnyi_slog(word, slogs)
        print("Pieces from base: %s" % words_base[word])
        print("Udarnui slog: %s" % udarnyi_slog)

        if len(slogs) == 2:
            if udarnyi_slog == 1:
                glasnaya = slogs[0][-1]
                rifma = "ху" + HUI_MAPPING.get(glasnaya, glasnaya) + slogs[1]

        if len(slogs) == 3:
            if udarnyi_slog == 1:
                glasnaya = slogs[0][-1]
                rifma = "ху" + HUI_MAPPING.get(glasnaya, glasnaya) + slogs[1] + slogs[2]
            elif udarnyi_slog == 2:
                glasnaya = slogs[1][-1]
                rifma = "ху" + HUI_MAPPING.get(glasnaya, glasnaya) + slogs[2]

        if rifma is not None:
            return word + " - " + rifma + "!"
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
            response = get_rifma(text, words)
            if response is not None:
                # print(msg)
                # print(msg['chat']['type'])
                if msg['chat']['type'] != 'private':
                    # print("Channel")
                    # if chat_id != CHAT_ID_EUGENE_MITSKEVICH:
                    bot.forwardMessage(CHAT_ID_EUGENE_MITSKEVICH, chat_id, msg['message_id'])
                    bot.sendMessage(CHAT_ID_EUGENE_MITSKEVICH, response, parse_mode="HTML")
                else:
                    # print("Net")
                    bot.sendMessage(chat_id, response, parse_mode="HTML")
    except Exception as exc:
        traceback.print_exc()


bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')
# Keep the program running.
while 1:
    time.sleep(10)
