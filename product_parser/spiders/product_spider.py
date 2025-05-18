import scrapy
import json
import time
from urllib.parse import urljoin

class ProductSpider(scrapy.Spider):
    name = "product_spider"

    custom_settings = {
        'COOKIES_ENABLED': True,
    }

    def start_requests(self):
        try:
            with open('start_urls.txt') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            urls = [
                "https://alkoteka.com/catalog/slaboalkogolnye-napitki-2",
                "https://alkoteka.com/catalog/vino",
                "https://alkoteka.com/catalog/konyak",
            ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_category,
                cookies={"city": "КРАСНОДАР"},
                meta={'category_url': url}
            )

    def parse_category(self, response):
        product_links = response.css("div.catalog__item a.catalog__item-title::attr(href)").getall()
        for link in product_links:
            yield response.follow(
                link, callback=self.parse_product,
                cookies={"city": "КРАСНОДАР"},
                meta={"section": self.get_section(response)}
            )

        next_page = response.css("a.pagination__item--arrow::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page, callback=self.parse_category,
                cookies={"city": "КРАСНОДАР"},
                meta=response.meta
            )

    def parse_product(self, response):
        def extract_text(sel):
            return sel.get(default="").strip()

        title = extract_text(response.css("h1.product__title::text"))
        volume = response.css("span.product__volume::text").get()
        if volume and volume not in title:
            title = f"{title}, {volume}"

        original_price = float(response.css("span.product-price__old::text").re_first(r"\d+").replace(" ", "") or 0)
        current_price = float(response.css("span.product-price__current::text").re_first(r"\d+").replace(" ", "") or 0)

        discount = 0
        sale_tag = ""
        if original_price and current_price < original_price:
            discount = round((original_price - current_price) / original_price * 100)
            sale_tag = f"Скидка {discount}%"

        metadata = {}
        for row in response.css("ul.characteristics__list li"):
            key = extract_text(row.css("span::text")).replace(":", "")
            val = extract_text(row.css("p::text"))
            if key and val:
                metadata[key] = val

        yield {
            "timestamp": int(time.time()),
            "RPC": response.url.split("/")[-1],
            "url": response.url,
            "title": title,
            "marketing_tags": [],
            "brand": extract_text(response.css("a.product__brand::text")),
            "section": response.meta.get("section", []),
            "price_data": {
                "current": current_price,
                "original": original_price or current_price,
                "sale_tag": sale_tag,
            },
            "stock": {
                "in_stock": bool(response.css("div.product__availability--in")),
                "count": 0,
            },
            "assets": {
                "main_image": response.css("div.product__gallery img::attr(src)").get(),
                "set_images": response.css("div.product__gallery img::attr(src)").getall(),
                "view360": [],
                "video": [],
            },
            "metadata": {
                "__description": extract_text(response.css("div.product__description p::text")),
                **metadata,
            },
            "variants": self.count_variants(metadata),
        }

    def get_section(self, response):
        return response.css("ul.breadcrumbs__list li a::text").getall()[1:]

    def count_variants(self, metadata):
        keys = [k.lower() for k in metadata.keys()]
        return int("объем" in keys or "цвет" in keys)