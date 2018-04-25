# FHCJ_Spider
使用scrapy框架爬取凤凰财经数据
数据源：沪市，深市的AB股，财务简况，财务指标，利润表，资产负债表，现金流量表
实现功能：
  1，在pipline中将item数据中的中文转为拼音首字母组合，同时生产了中英文对照表的json文件，避免了存储数据时，因中文报错
  2，在middleware中通过redis实现了断点续爬，第一次爬取的时候将downloadermiddleware关闭，中断后爬取的时候打开downloadermiddleware

如有bug，欢迎指正。
转载请注明出处，谢谢！
本人联系方式：626132292@qq.com
