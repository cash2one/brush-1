# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import os
from zhihu_oauth import ZhihuClient


TOKEN_FILE = 'token.pkl'


client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)

# question = client.question(35166763)
# question = client.from_url('https://www.zhihu.com/question/35166763')
# print(question.title)
# with open("name.txt", 'a', encoding='utf-8') as f:
#     for answer in question.answers:
#         if answer.author.name != "匿名用户" and answer.author.name != "[已重置]":
#                 print(answer.author.name)
#                 f.write(answer.author.name+'\n')



me = client.me()

print('name', me.name)
print('headline', me.headline)
print('description', me.description)

print('following topic count', me.following_topic_count)
print('following people count', me.following_topic_count)
print('followers count', me.follower_count)

print('voteup count', me.voteup_count)
print('get thanks count', me.thanked_count)

print('answered question', me.answer_count)
print('question asked', me.question_count)
print('collection count', me.collection_count)
print('article count', me.articles_count)
print('following column count', me.following_column_count)













