# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import os
from zhihu_oauth import ZhihuClient
import random

TOKEN_FILE = 'token.pkl'


client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)


# for _ in range(1000):
#     num = random.randint(20000000, 39999999)
for num in [40023941, 36582119, 23434853, 37027323, 39124944, 22345285, 26992616, 28066166, 41035200, 21396519,
            35947787, 36851579, 21372989, 47955389, 37236484, 19861023, 25877081, 27063206,
            29166103, 23246914, 38540397, 36543921, 32158092, 41207814, 41404094, 36734444, 31819473, 29336768,
            32171411, 37184080, 20468104, 36238122, 36573907, 23415802, 30605806, 37737298,
            37059032, 48837193, 48296279, 41053015, 22978737, 22621327, 42082026, 30470093, 41038770,
            21155222, 28489148, 32081129, 32369239, 30830614, 29213441, 41113819, 36770197, 48831736,
            35990525, 48779414, 22364486, 33032798, 29604768, 21900376, 26500277]:
    n = 0
    try:
        question = client.question(num)
        # question = client.from_url('https://www.zhihu.com/question/35166763')
        print(question.title)
        with open("name.txt", 'a', encoding='utf-8') as f:
            for answer in question.answers:
                n += 1
                try:
                    if answer.author.name != "匿名用户" and answer.author.name != "[已重置]":
                        print(answer.author.name)
                        f.write(answer.author.name+'\n')
                except:
                    pass
                print(n)
    except:
        print("空")

#初始登录
# me = client.me()
# #
# print('name', me.name)
# print('headline', me.headline)
# print('description', me.description)
# #
# print('following topic count', me.following_topic_count)
# print('following people count', me.following_topic_count)
# print('followers count', me.follower_count)
# #
# print('voteup count', me.voteup_count)
# print('get thanks count', me.thanked_count)
#
# print('answered question', me.answer_count)
# print('question asked', me.question_count)
# print('collection count', me.collection_count)
# print('article count', me.articles_count)
# print('following column count', me.following_column_count)













