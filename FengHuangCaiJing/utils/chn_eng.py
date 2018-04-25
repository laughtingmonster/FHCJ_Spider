# -*- coding:utf-8 -*-
import json
import re
import sys
import random
from FengHuangCaiJing.utils.hanzi2pinyin import PinYin


class Chi2Eng(object):

    def __init__(self, sourcefile):
        self.sourcefile = sourcefile
        self.depfile = sourcefile.replace('.json', '_ENG.json')
        self.template = sourcefile.replace('.json', '_template.json')

        self.f1 = open(self.sourcefile, 'r', encoding='utf-8')
        self.f2 = open(self.depfile, 'a', encoding='utf-8')
        self.f3 = open(self.template, 'a', encoding='utf-8')

        self.py = PinYin()
        self.py.load_word()
        
        self.han_pin = []


    def get_pinyin(self, han):
        pylist = self.py.hanzi2pinyin(han)
        pylist = list(filter(lambda x: x is not '', pylist))
        pyname = ''.join(map(lambda x: x[0], pylist))
        return pyname


    def get_han_pin(self):
        n = 0
        for line in self.f1:
            names = re.findall(r'"name"\: "(.*?)"\,', line)
            names = list(set(names))
            for name in names:
                h2p_dict = {}
                h2p_dict['han'] = name
                pyname = self.get_pinyin(name)
                h2p_dict['pin'] = pyname
                self.han_pin.append(h2p_dict)

            titles = re.findall(r'"title"\: "(.*?)"\,', line)
            if titles:
                titles = list(set(titles))
                for title in titles:
                    h2p_dict = {}
                    h2p_dict['han'] = title
                    pyname = self.get_pinyin(title)
                    h2p_dict['pin'] = pyname
                    self.han_pin.append(h2p_dict)

            json.dump(self.han_pin, self.f3, ensure_ascii=False)
            self.f3.close()

            n += 1
            if n == 1:
                break


    def sub_han_pin(self):
        self.get_han_pin()

        def repl(match):
            name = match.group(1)
            for temp in self.han_pin:         
                if temp.get('han') == name:
                    pin = temp.get('pin')
                    pin = r'"name": "%s",' % pin
                    return pin

        def repl_1(match):
            title = match.group(1)
            for temp in self.han_pin:
                if temp.get('han') == title:
                    pin = temp.get('pin')
                    pin = r'"title": "%s",' % pin
                    return pin

        
        for n, line in enumerate(self.f1):
            newline = re.sub(r'"name"\: "(.*?)"\,', repl, line)
            newline = re.sub(r'"title"\: "(.*?)"\,', repl_1, newline)
            self.f2.write(newline)
            print(n)
        
        self.f1.close()
        self.f2.close()



def main():
    sourcefile = sys.argv[1]
    c2e = Chi2Eng(sourcefile)
    c2e.sub_han_pin()

if __name__ == '__main__':
    main()




