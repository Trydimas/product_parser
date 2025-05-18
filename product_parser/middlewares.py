import random

class ProxyMiddleware:
    def __init__(self):
        self.proxies = [
            'http://123.456.789.000:8080',
            'http://proxy2.example.com:3128',
        ]

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxies)