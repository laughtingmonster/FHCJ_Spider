# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import re
from FengHuangCaiJing.utils.hanzi2pinyin import PinYin


class HA_CWJK_Pipeline(object):

    def process_item(self, item, spider):

        save_json(item)

# 保存item的同时，将中文转换为拼音首字母组合
def save_json(item):
    py = PinYin()
    py.load_word()
    han_pin = []
    filename = item.__class__.__name__ + '.json'
    templatefile = filename.replace('.json', '_template.json')
    with open(filename, 'a', encoding='utf-8') as f1, open(templatefile, 'w', encoding='utf-8') as f2:

        data = json.dumps(dict(item), ensure_ascii=False)  # 显示中文

        def get_pinyin(han):
            pylist = py.hanzi2pinyin(han)
            # print('pylist: %s, name: %s' % (pylist, han))
            pylist = list(filter(lambda x: x is not '', pylist))
            pyname = ''.join(map(lambda x: x[0], pylist))
            return pyname

        names = re.findall(r'"name"\: "(.*?)"\,', data)
        names = list(set(names))
        # print('names: %s' % names)
        for name in names:
            h2p_dict = {}
            h2p_dict['han'] = name
            pyname = get_pinyin(name)
            print("pyname: %s" % pyname)
            h2p_dict['pin'] = pyname
            han_pin.append(h2p_dict)
        
        titles = re.findall(r'"title"\: "(.*?)"\,', data)
        if titles:
            titles = list(set(titles))
            for title in titles:
                h2p_dict = {}
                h2p_dict['han'] = title
                pytitle = get_pinyin(title)
                print('pytitle: %s' % pytitle)
                h2p_dict['pin'] = pytitle
                han_pin.append(h2p_dict)
        
        json.dump(han_pin, f2, ensure_ascii=False)  #  w模式 覆盖

        def repl(match):
            name = match.group(1)
            for temp in han_pin:         
                if temp.get('han') == name:
                    pin = temp.get('pin')
                    pin = r'"name": "%s",' % pin
                    return pin

        def repl_1(match):
            title = match.group(1)
            for temp in han_pin:
                if temp.get('han') == title:
                    pin = temp.get('pin')
                    pin = r'"title": "%s",' % pin
                    return pin

        newdata = re.sub(r'"name"\: "(.*?)"\,', repl, data)
        newdata = re.sub(r'"title"\: "(.*?)"\,', repl_1, newdata)

        f1.write(newdata + '\n')
        # print(newdata)
        print('================== %s =====================' % filename)


