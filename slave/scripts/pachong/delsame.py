# -*- coding: utf-8 -*-

import re
if __name__ == '__main__':
    pattern = u"(message((\d)+))"
    prog = re.compile(pattern)
    # read text from file
    f = open("name.txt", "r", encoding='utf-8')
    text = f.read()
    f.close()
    print(text.encode("utf-8"))
    result = prog.findall(text)
    message_map = dict()
    redupicate_count = 0
    for message in result:
        if message_map.has_key(message[0]) == True:
            print(message[0], "is reduplicate")
            redupicate_count += 1
        else:
            message_map[message[0]] = 1
        print("total reduplicate message is ", redupicate_count)
