# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/2/13 19:45
# Desc  : python 调用ChatGPT
import openai

openai.api_key = ""

completion = openai.Completion.create(
    # engine="text-davinci-003",
    engine="gpt-3.5-turbo",
    prompt="请赞美一个20岁女性,不低于200字",
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,

)

response = completion.choices[0].text
print(response)
