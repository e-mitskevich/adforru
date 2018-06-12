#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import random
import re
import traceback

import sys
import telepot
import time
from telepot.loop import MessageLoop


IS_LOCAL = ("darwin" in sys.platform)


CHAT_ID_EUGENE_MITSKEVICH = 136483796
CHAT_ID_KRASIVO = -304487349


base_dir = os.path.dirname(__file__)


GLASNYE = ["а", "о", "и", "е", "ё", "э", "ы", "у", "ю", "я"]
HUI_MAPPING = {
    "а": "я",
    "о": "ё",
    "э": "е",
    "ы": "и",
    "у": "ю"
}


def probability(value):
    return (random.uniform(0, 1) < value)


def has_glasnye(text):
    for char in text:
        if char in GLASNYE:
            return True
    return False


def has_soglasnye(text):
    for char in text:
        if char not in GLASNYE:
            return True
    return False


def to_slogs(word):
    tmp_word = ""
    for char in word:
        tmp_word += char
        if char in GLASNYE:
            tmp_word += ","
    result = tmp_word.split(",")
    if len(result) > 1 and not has_glasnye(result[-1]):
        result[-2] += result[-1]
        result = result[:-1]
    return result


def is_pervui_slog_udarnyi(word, slogs):
    first_slog = slogs[0]
    return (first_slog not in words_base[word][0] or (first_slog in GLASNYE and first_slog == words_base[word][0]))


def divide_single_slog(word):
    first = ""
    for char in word:
        first += char
        if char in GLASNYE:
            break
    return [first, word.replace(first, "")]


def correct_for_base(word):
    if word in words_base:
        return word

    endings = ("и", "е", "ы", "у", "ой")
    for ending in endings:
        if word.endswith(ending):
            tmp = word[:-len(ending)] + "а"
            if tmp in words_base:
                return tmp

    endings = ("е", "у", "а")
    for ending in endings:
        if word.endswith(ending):
            tmp = word[:-len(ending)]
            if tmp in words_base:
                return tmp

    return word


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

        if IS_LOCAL:
            print(word + " -> " + str(slogs))
            print("Word exists: %s" % (word in words_base))

        corrected_word = correct_for_base(word)
        if corrected_word != word and IS_LOCAL:
            print("Corrected: %s" % corrected_word)

        rifma = None

        if not has_glasnye(word) or not has_soglasnye(word):
            continue

        if len(slogs) == 1 and word[-1] not in GLASNYE:
            parts = divide_single_slog(word)
            glasnaya = parts[0][-1]
            rifma = "ху" + HUI_MAPPING.get(glasnaya, glasnaya) + parts[1]

        if len(slogs) in (2, 3) and corrected_word in words_base:
            udarnyi_slog_pervui = is_pervui_slog_udarnyi(corrected_word, slogs)

            if IS_LOCAL:
                print("Pieces from base: %s" % words_base[corrected_word])
                print("Udarnui slog pervyi: %s" % udarnyi_slog_pervui)

            if udarnyi_slog_pervui:
                if len(slogs) == 2 and word == corrected_word and probability(0.75):
                    return ["А " + word + " жарииит", "Кууууууур!"]
                else:
                    glasnaya = slogs[0][-1]
                    rifma = "ху" + HUI_MAPPING.get(glasnaya, glasnaya) + slogs[1]
                    if len(slogs) == 3:
                        rifma += slogs[2]

        if rifma is not None:
            return word + " - " + rifma + "!"

    return None


def handle(msg):
    try:
        print("==============")
        # print("Message: " + str(msg))
        content_type, chat_type, chat_id = telepot.glance(msg)
        text = msg["text"] if 'text' in msg else msg.get('caption', '')
        text = text.lower().replace("-", "")  # ignoring smth like "как-нибудь"

        words = re.findall("[а-яА-Я0-9]+", text)
        if words:
            response = get_rifma(text, words)
            if response is not None:
                # if msg['chat']['type'] != 'private':
                #     bot.forwardMessage(CHAT_ID_EUGENE_MITSKEVICH, chat_id, msg['message_id'])
                #     bot.sendMessage(CHAT_ID_EUGENE_MITSKEVICH, response, parse_mode="HTML")
                # else:
                if isinstance(response, list):
                    bot.sendMessage(chat_id, response[0], parse_mode="HTML")
                    time.sleep(2)
                    bot.sendMessage(chat_id, response[1], parse_mode="HTML")
                else:
                    bot.sendMessage(chat_id, response, parse_mode="HTML")
    except Exception as exc:
        traceback.print_exc()


with open(os.path.join(base_dir, 'config.json'), 'r') as f:
    config = json.load(f)
    TOKEN = config['token']
    PASSWORD = config['password']

with open(os.path.join(base_dir, 'words.json'), 'r') as f:
    words_base = json.load(f)


bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()


print('Started with base of %s words ...' % len(words_base))
# Keep the program running.
while 1:
    time.sleep(10)
