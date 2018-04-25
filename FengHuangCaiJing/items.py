# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy import Field


class FH_CWJK(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = Field()  # 股票代码  
    detail = Field()  # 详细数据
    # date = Field()  # 截止日期
    # net_profit = Field()  # 净利润(万元)
    # kcfjcxsyhdjlr = Field()  # 扣除非经常性损益后的净利润(万元)
    # net_asset = Field()  # 净资产(万元)
    # wfplr = Field()  # 未分配利润(万元)
    # zbgj = Field()  # 资本公积(万元)
    # mgsy = Field()  # 每股收益(元)
    # jqmgsy = Field()  # 加权每股收益(元)
    # kcfjcxsyhdmgsy = Field()  # 扣除非经常性损益后的每股收益(元)
    # kcfjcxsyhdmgsy_jq = Field()  # 扣除非经常性损益后的每股收益(加权)(元)
    # mgjzc = Field()  # 每股净资产(元)
    # tzhdmgjzc = Field()  # 调整后的每股净资产(元)
    # jzcsyl = Field()  # 净资产收益率
    # jqjzcsyl = Field()  # 加权净资产收益率
    # kcfjcxsyhdjzcsyl = Field()  # 扣除非经常性损益的净资产收益率
    # kcfjcxsyhdjzcsyl_jq = Field()  # 扣除非经常性损益的净资产收益率(加权)
    # mgjyhdcsdxjllje = Field()  # 每股经营活动产生的现金流量净额(元)


class FH_CWZB(scrapy.Item):
    code = Field()
    detail = Field()


class FH_ZCFZB(scrapy.Item):
    code = Field()
    detail = Field()


class FH_LRB(scrapy.Item):
    code = Field()
    detail = Field()


class FH_XJLLB(scrapy.Item):
    code = Field()
    detail = Field()
