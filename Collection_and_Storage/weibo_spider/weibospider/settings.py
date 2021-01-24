# -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False

# change cookie to yours
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie': '_T_WM=14187112880; WEIBOCN_FROM=1110005030; SCF=AiAipGh00357bXS6pKbBXZKPNaBzlakQ5fh8KarzPRmhUL4BhUfPIleM1r9ElUaWNlDAPBJuBMKG5ogy14gKT-4.; SUB=_2A25y5mUHDeRhGeVK4lYV9SrIyzyIHXVuKQtPrDV6PUJbktAKLVajkW1NTEmHb4n2CuegLCrvEoIWfUU1zDwlJgoL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWznAmxkLlVX1sJaK26SuK35NHD95Q0Sh.XSh-XSh57Ws4Dqcjci--RiKy8i-8Fi--ci-8siK.Xi--Xi-z4iKyhi--ciK.ci-8si--ciKLFi-zEi--4iKL2i-2E; SSOLoginState=1608652119; MLOGIN=1; M_WEIBOCN_PARAMS=lfid%3D230677MSFT%26luicode%3D20000174%26fid%3D1076033494454400%26uicode%3D10000011'}

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'middlewares.IPProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
}

ITEM_PIPELINES = {
    'pipelines.MongoDBPipeline': 300,
}

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
