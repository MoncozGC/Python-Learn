# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/10 17:18
# Desc  : 语音识别(Failed)

import speech_recognition as sr
from googletrans import Translator

# 初始化语音识别器
from utils.comm_util import print_ts

recognizer = sr.Recognizer()

# 从文件中识别语音（请将file_name替换为你的音频文件）
file_name = './data/snap.wav'
with sr.AudioFile(file_name) as source:
    audio = recognizer.record(source)
    text = recognizer.recognize_google(audio, language='zh-CN')  # 你可以将'zh-CN'替换为其他语言代码
    print_ts(text)
print_ts("准备翻译")
# 初始化翻译器
translator = Translator()

# 翻译文本
translated = translator.translate(text, src='zh-CN', dest='en')  # 将中文文本翻译成英文

# 打印翻译结果
print(translated.text)
