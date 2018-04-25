# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Request
from FengHuangCaiJing.items import FH_CWJK, FH_CWZB, FH_ZCFZB, FH_LRB, FH_XJLLB

class HaSpider(scrapy.Spider):
    name = 'FH'
    # allowed_domains = ['http://app.finance.ifeng.com/']
    # start_urls = ['http://app.finance.ifeng.com/list/stock.php?t=ha&f=symbol&o=asc&p=1']

    def start_requests(self):
        """沪市A股"""
        # url = r"http://app.finance.ifeng.com/list/stock.php?t=ha&f=symbol&o=asc&p={}"
        # for i in range(1, 28):  # 27页
        #     sta_url = url.format(i)
        #     yield Request(url=sta_url, callback=self.parse)

        """沪市B股"""
        # url = r'http://app.finance.ifeng.com/list/stock.php?t=hb&f=symbol&o=asc&p=1'
        # yield Request(url=url, callback=self.parse)

        """深市A股"""
        # url = r'http://app.finance.ifeng.com/list/stock.php?t=sa&f=symbol&o=asc&p={}'
        # for i in range(1, 40):  # 39页
        #     sta_url = url.format(i)
        #     yield Request(url=sta_url, callback=self.parse)

        """深市B股"""
        url = r'http://app.finance.ifeng.com/list/stock.php?t=sb&f=symbol&o=asc&p=1'
        yield Request(url=url, callback=self.parse)

    # 获取沪市A股的代码
    def parse(self, response):

        trs = response.xpath(r'/html/body/div[8]/div/div[2]/div/table//tr')[1:-1]  # 去掉第一行和最后一行无效的
        for tr in trs:
            
            code = tr.xpath(r'./td/a/text()').extract_first()
            cwjk_url = r'http://app.finance.ifeng.com/data/stock/tab_cwjk.php?symbol={}'.format(code)  # 财务简况
            cwzb_url = r'http://app.finance.ifeng.com/data/stock/tab_cwzb.php?symbol={}'.format(code)  # 财务指标
            zcfzb_url = r'http://app.finance.ifeng.com/data/stock/tab_zcfzb.php?symbol={}'.format(code)  # 资产负债表
            lrb_url = r'http://app.finance.ifeng.com/data/stock/tab_lrb.php?symbol={}'.format(code)  # 利润表
            xjllb_url = r'http://app.finance.ifeng.com/data/stock/tab_xjllb.php?symbol={}'.format(code)  # 现金流量表

            yield Request(url=cwjk_url, callback=self.parse_cwjk)
            yield Request(url=cwzb_url, callback=self.parse_cwzb)
            yield Request(url=zcfzb_url, callback=self.parse_zcfzb)
            yield Request(url=lrb_url, callback=self.parse_lrb)
            yield Request(url=xjllb_url, callback=self.parse_xjllb)

    
    # 财务简况
    def parse_cwjk(self, response):
        url = response.url
        code = re.split(r'.*?(\d+)', url)[1]
        cwjk = FH_CWJK()
        cwjk['code'] = code
        cwjk['detail'] = []
        trs = response.xpath(r'/html/body/div[9]/div[2]/div/table//tr')[1:]
        tr_num = len(trs)
        tds = response.xpath(r'/html/body/div[9]/div[2]/div/table//tr[1]/td')[1:]
        td_num = len(tds)
        for x in range(td_num):
            ddl = {}
            ddl['year'] = tds[x].xpath('string(.)').extract_first().strip()
            ddl['data'] = []
            for y in range(tr_num):
                data = {}
                data['name'] = response.xpath(r'/html/body/div[9]/div[2]/div/table//tr[%s]/td[1]'%(y+2))[0].xpath('string(.)').extract_first().strip()
                data['value'] = response.xpath(r'/html/body/div[9]/div[2]/div/table//tr[%s]/td[%s]'%(y+2, x+2))[0].xpath('string(.)').extract_first().strip()
                ddl['data'].append(data)
            cwjk['detail'].append(ddl)

        yield cwjk




    # 财务指标
    def parse_cwzb(self, response):
        trs = response.xpath(r'/html/body/div[9]/div[2]/table//tr')

        tds = response.xpath(r'/html/body/div[9]/div[2]/table//tr[1]/td')[1:]  # 4
        td_num = len(tds)  # 4
        # 最后一个年度显示的页面
        if td_num == 1:
            url = response.url
            yield Request(url=url, callback=self.cwzb_one)

        # 四个年度显示的页面, 取前三个, 避免重复
        else:
            code = re.split(r'.*?(\d+)', response.url)[1]
            cwzb = FH_CWZB()
            cwzb['code'] = code
            cwzb['detail'] = []

            line = []  # 存储表格中的小标题所在行的下标
            for y, tr in enumerate(trs):
                td_nodes = tr.xpath(r'./td')
                if len(td_nodes) == 1:
                    line.append(y)

            for x in range(td_num-1):  # 取前三个

                sub_year = {}
                sub_year['date'] = tds[x].xpath(r'./text()').extract_first().strip()
                sub_year['info'] = []

                for n, num in enumerate(line):

                    sub_detail = {}
                    sub_detail['title'] = trs[num].xpath(r'./td')[0].xpath('string(.)').extract_first().strip()
                    sub_detail['data'] = []

                    if num != line[-1]:
                        for temp in trs[num+1: line[n+1]]:
                            data_dict = {}
                            data_dict['name'] = temp.xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                            data_dict['value'] = temp.xpath(r'./td[%s]'%(x+2))[0].xpath('string(.)').extract_first().strip()
                            sub_detail['data'].append(data_dict)
  
                    else:
                        for temp in trs[num+1: ]:
                            data_dict = {}
                            data_dict['name'] = temp.xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                            data_dict['value'] = temp.xpath(r'./td[%s]'%(x+2))[0].xpath('string(.)').extract_first().strip()
                            sub_detail['data'].append(data_dict)

                    sub_year['info'].append(sub_detail)
                    
                cwzb['detail'].append(sub_year)          
            yield cwzb
                
            # 向后按钮
            gonext_url = response.xpath(r'/html/body/div[9]/div[2]/table//tr[1]/td[1]/a[2]/@href').extract_first()
            gonext_url = response.urljoin(gonext_url)
            yield Request(url=gonext_url, callback=self.parse_cwzb)

    def cwzb_one(self, response):

        code = re.split(r'.*?(\d+)', response.url)[1]
        cwzb = FH_CWZB()
        cwzb['code'] = code
        cwzb['detail'] = [{'date': response.xpath(r'/html/body/div[9]/div[2]/table//tr[1]/td[2]')[0].xpath('string(.)').extract_first().strip(),
                         'info': []}]

        trs = response.xpath(r'/html/body/div[9]/div[2]/table//tr')
        line = []  # 存储表格中的小标题所在行的下标
        for y, tr in enumerate(trs):
            td_nodes = tr.xpath(r'./td')
            if len(td_nodes) == 1:
                line.append(y)
        
        for n, num in enumerate(line):
            sub_detail = {}
            sub_detail['title'] = trs[num].xpath(r'./td')[0].xpath('string(.)').extract_first().strip()
            sub_detail['data'] = []

            if num != line[-1]:
                for temp in trs[num+1: line[n+1]]:
                    data_dict = {}
                    data_dict['name'] = temp.xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                    data_dict['value'] = temp.xpath(r'./td[2]')[0].xpath('string(.)').extract_first().strip()
                    sub_detail['data'].append(data_dict)
  
            else:
                for temp in trs[num+1: ]:
                    data_dict = {}
                    data_dict['name'] = temp.xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                    data_dict['value'] = temp.xpath(r'./td[2]')[0].xpath('string(.)').extract_first().strip()
                    sub_detail['data'].append(data_dict)
            
            cwzb['detail'][0]['info'].append(sub_detail)
        
        yield cwzb

            
    # 资产负债表
    def parse_zcfzb(self, response):

        trs = response.xpath(r'/html/body/div[9]/div[2]/table//tr')
        tds = response.xpath(r'/html/body/div[9]/div[2]/table//tr[1]/td')[1:]
        td_num = len(tds) 
        #
        if td_num != 1:
            code = re.split(r'.*?(\d+)', response.url)[1]
            zcfzb = FH_ZCFZB()
            zcfzb['code'] = code
            zcfzb['detail'] = []

            # 表格中的小标题, 存放下标
            line = []
            
            for n, tr in enumerate(trs):
                # 
                if len(tr.xpath(r'./td')) == 2 or len(tr.xpath(r'./td')) == 1:
                    line.append(n)
            # 取前三个
            for x in range(td_num-1): 
                sub_year = {}
                sub_year['date'] = tds[x].xpath('string(.)').extract_first().strip()
                sub_year['info'] = []

                for n, num in enumerate(line):
                    
                    # 两个小标题紧邻 特殊分析 
                    if num-1 == line[n-1] and num != line[-1]:
                        sub_detail = {}
                        sub_detail['title'] = trs[num-1].xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip() + '/' + trs[num].xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                        sub_detail['data'] = []
                        for temp in trs[num+1: line[n+1]]:
                            data_dict = {}
                            data_dict['name'] = temp.xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                            data_dict['value'] = temp.xpath(r'./td[%s]'%(x+2))[0].xpath('string(.)').extract_first().strip()
                            sub_detail['data'].append(data_dict)
                        sub_year['info'].append(sub_detail)
                    # 中间的小标题
                    elif (num != line[-1]) and (num+1 != line[n+1]):
                        sub_detail = {}
                        sub_detail['title'] = trs[num].xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                        sub_detail['data'] = []
                        for temp in trs[num+1: line[n+1]]:
                            data_dict = {}
                            data_dict['name'] = temp.xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                            data_dict['value'] = temp.xpath(r'./td[%s]'%(x+2))[0].xpath('string(.)').extract_first().strip()
                            sub_detail['data'].append(data_dict)
                        sub_year['info'].append(sub_detail)

                    # 最后一个小标题
                    elif num == line[-1]:
                        sub_detail = {}
                        sub_detail['title'] = trs[num].xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                        sub_detail['data'] = []
                        for temp in trs[num+1: ]:
                            data_dict = {}
                            data_dict['name'] = temp.xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                            data_dict['value'] = temp.xpath(r'./td[%s]'%(x+2)).xpath('string(.)').extract_first().strip()
                            sub_detail['data'].append(data_dict)
                        sub_year['info'].append(sub_detail)
                                     
                zcfzb['detail'].append(sub_year)

            yield zcfzb

            # 向后
            next_url = response.xpath(r'/html/body/div[9]/div[2]/table//tr[1]/td[1]/a[2]/@href').extract_first()
            next_url = response.urljoin(next_url)
            yield Request(url=next_url, callback=self.parse_zcfzb)

        # 最后一条
        else:
            url = response.url
            yield Request(url=url, callback=self.zcfzb_one)


    def zcfzb_one(self, response):
        
        code = re.split(r'.*?(\d+)', response.url)[1]
        zcfzb = FH_ZCFZB()
        zcfzb['code'] = code
        zcfzb['detail'] = [{'date': response.xpath(r'/html/body/div[9]/div[2]/table//tr[1]/td[2]')[0].xpath('string(.)').extract_first().strip(),
                            'info': []}]
        
        trs = response.xpath(r'/html/body/div[9]/div[2]/table//tr')
        line = []

        for n, tr in enumerate(trs):
            # 每一行第二个td标签是空的
            if len(tr.xpath('./td')) != 5:
                line.append(n)
        
        for n, num in enumerate(line):
            
            # 资产和流动资产紧邻 特殊分析 
            if num-1 == line[n-1] and num != line[-1]:
                sub_detail = {}
                sub_detail['title'] = trs[num-1].xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip() + '/' + trs[num].xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                sub_detail['data'] = []
                for temp in trs[num+1: line[n+1]]:
                    data_dict = {}
                    data_dict['name'] = temp.xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                    data_dict['value'] = temp.xpath(r'./td[2]')[0].xpath('string(.)').extract_first().strip()
                    sub_detail['data'].append(data_dict)
                zcfzb['detail'][0]['info'].append(sub_detail)
            # 中间的小标题
            elif (num != line[-1]) and (num+1 != line[n+1]):
                sub_detail = {}
                sub_detail['title'] = trs[num].xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                sub_detail['data'] = []
                for temp in trs[num+1: line[n+1]]:
                    data_dict = {}
                    data_dict['name'] = temp.xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                    data_dict['value'] = temp.xpath(r'./td[2]')[0].xpath('string(.)').extract_first().strip()
                    sub_detail['data'].append(data_dict)
                zcfzb['detail'][0]['info'].append(sub_detail)

            # 最后一个小标题
            elif num == line[-1]:
                sub_detail = {}
                sub_detail['title'] = trs[num].xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                sub_detail['data'] = []
                for temp in trs[num+1: ]:
                    data_dict = {}
                    data_dict['name'] = temp.xpath(r'./td[1]')[0].xpath('string(.)').extract_first().strip()
                    data_dict['value'] = temp.xpath(r'./td[2]')[0].xpath('string(.)').extract_first().strip()
                    sub_detail['data'].append(data_dict)
                zcfzb['detail'][0]['info'].append(sub_detail)
                     
        
        yield zcfzb


    # 利润表
    def parse_lrb(self, response):
        trs = response.xpath('/html/body/div[9]/div[2]/table/tbody/tr')
        tds = response.xpath('/html/body/div[9]/div[2]/table/tbody/tr[1]/td')[1:]
        td_num = len(tds)

        if td_num != 1:
            code = re.split(r'.*?(\d+)', response.url)[1]
            lrb = FH_LRB()
            lrb['code'] = code
            lrb['detail'] = []

            # 取前三个
            for x in range(td_num-1):
                sub_year = {}
                sub_year['end_date'] = tds[x].xpath('string(.)').extract_first().strip()
                sub_year['start_date'] = response.xpath('/html/body/div[9]/div[2]/table//tr[2]/td[%s]'%(x+2)).xpath('string(.)').extract_first().strip()
                sub_year['info'] = []
                for y, tr in enumerate(trs[3:]):
                    sub_detail = {}
                    sub_detail['name'] = tr.xpath('./td[1]')[0].xpath('string(.)').extract_first().strip()
                    sub_detail['value'] = tr.xpath('./td[%s]'%(x+2))[0].xpath('string(.)').extract_first().strip()
                    sub_year['info'].append(sub_detail)
                lrb['detail'].append(sub_year)
            yield lrb
            # 向后
            next_url = response.xpath('/html/body/div[9]/div[2]/table//tr[1]/td[1]/a[2]/@href').extract_first()
            next_url = response.urljoin(next_url)
            yield Request(url=next_url, callback=self.parse_lrb)

        else:
            yield Request(url=response.url, callback=self.lrb_one)


    def lrb_one(self, response):
        trs = response.xpath('/html/body/div[9]/div[2]/table/tbody/tr')[3:]
        lrb = FH_LRB()
        lrb['code'] = re.findall(r'.*?(\d+)', response.url)[0]
        start_date = response.xpath('/html/body/div[9]/div[2]/table//tr[2]/td[2]')[0].xpath('string(.)').extract_first().strip()
        end_date = response.xpath('/html/body/div[9]/div[2]/table//tr[1]/td[2]')[0].xpath('string(.)').extract_first().strip()
        lrb['detail'] = [{"start_date": start_date,
                        "end_date": end_date,
                        "info": []}]
        for tr in trs:
            sub_detail = {}
            sub_detail['name'] = tr.xpath('./td[1]')[0].xpath('string(.)').extract_first().strip()
            sub_detail['value'] = tr.xpath('./td[2]')[0].xpath('sring(.)').extract_first().strip()
            lrb['detail'][0]['info'].append(sub_detail)
        
        yield lrb


    # 现金流量表
    def parse_xjllb(self, response):

        trs = response.xpath('/html/body/div[9]/div[2]/table//tr')[3:]
        tds = response.xpath('/html/body/div[9]/div[2]/table//tr[1]/td')[1:]
        td_num = len(tds)

        if td_num != 1:
            xjllb = FH_XJLLB()
            code = re.findall(r'.*?(\d+)', response.url)[0]
            xjllb['code'] = code
            xjllb['detail'] = []

            # 存放小标题的下标
            line = []
            for i, tr in enumerate(trs):
                if len(tr.xpath('./td')) == 2:
                    line.append(i)

            # 取前三个
            for x in range(td_num-1):
                sub_year = {}
                sub_year['start_date'] = tds[x].xpath('string(.)').extract_first().strip()
                sub_year['end_date'] = response.xpath('/html/body/div[9]/div[2]/table//tr[2]/td[%s]'%(x+2))[0].xpath('string(.)').extract_first()
                sub_year['info'] = []

                for n, num in enumerate(line):
                    sub_detail = {}       
                    sub_detail['title'] = trs[num].xpath('./td[1]')[0].xpath('string(.)').extract_first().strip()
                    sub_detail['data'] = []
                    # 如果不是最后一个小标题
                    if num != line[-1]:                    
                        for tr in trs[num+1: line[n+1]]:
                            data_dict = {}
                            data_dict['name'] = tr.xpath('./td[1]')[0].xpath('string(.)').extract_first().strip()
                            data_dict['value'] = tr.xpath('./td[%s]'%(x+2)).xpath('string(.)').extract_first().strip()
                            sub_detail['data'].append(data_dict)
                    else:
                        for tr in trs[num+1: ]:
                            data_dict = {}
                            data_dict['name'] = tr.xpath('./td[1]')[0].xpath('string(.)').extract_first().strip()
                            data_dict['value'] = tr.xpath('./td[%s]'%(x+2)).xpath('string(.)').extract_first().strip()
                            sub_detail['data'].append(data_dict)
                    sub_year['info'].append(sub_detail)
                xjllb['detail'].append(sub_year)

            yield xjllb

            # 向后
            next_url = response.xpath('/html/body/div[9]/div[2]/table//tr[1]/td[1]/a[2]/@href').extract_first()
            next_url = response.urljoin(next_url)
            yield Request(url=next_url, callback=self.parse_xjllb)

        else:
            yield Request(url=response.url, callback=self.xjllb_one)

    
    def xjllb_one(self, response):
        trs = response.xpath('/html/body/div[9]/div[2]/table//tr')[3:]
        xjllb = FH_XJLLB()
        xjllb['code'] = re.findall(r'.*?(\d+)', response.url)[0]
        start_date = response.xpath('/html/body/div[9]/div[2]/table//tr[2]/td[2]')[0].xpath('string(.)').extract_first().strip()
        end_date = response.xpath('/html/body/div[9]/div[2]/table//tr[1]/td[2]')[0].xpath('string(.)').extract_first().strip()
        xjllb['detail'] = [{'start_date': start_date,
                            'end_date': end_date,
                            'info': []}]

        line = []
        for i, tr in enumerate(trs):
            if len(tr.xpath('./td')) != 2:
                line.append(i)
        
        for n, num in enumerate(line):
            sub_detail = {}
            sub_detail['title'] = trs[num].xpath('./td[1]')[0].xpath('string(.)').extract_first().strip()
            sub_detail['data'] = []
            # 如果不是最后一个标题
            if line[-1] != num:
                for tr in trs[num+1: line[n+1]]:
                    data_dict = {}
                    data_dict['name'] = tr.xpath('./td[1]')[0].xpath('string(.)').extract_first().strip()
                    data_dict['value'] = tr.xpath('./td[2]')[0].xpath('string(.)').extract_first().strip()
                    sub_detail['data'].append(data_dict)
            else:
                for tr in trs[num+1: ]:
                    data_dict = {}
                    data_dict['name'] = tr.xpath('./td[1]')[0].xpath('string(.)').extract_first().strip()
                    data_dict['value'] = tr.xpath('./td[2]')[0].xpath('string(.)').extract_first().strip()
                    sub_detail['data'].append(data_dict)
            xjllb['detail'][0]['info'].append(sub_detail)
        
        yield xjllb


