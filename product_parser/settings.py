BOT_NAME = "product_parser"

SPIDER_MODULES = ["product_parser.spiders"]
NEWSPIDER_MODULE = "product_parser.spiders"

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1.5

DOWNLOADER_MIDDLEWARES = {
    'product_parser.middlewares.ProxyMiddleware': 350,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
}

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ru",
}