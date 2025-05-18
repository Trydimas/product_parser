# Product Parser

Парсер товаров с сайта https://alkoteka.com с использованием Scrapy.

## Возможности
- Сбор товаров из заданных категорий
- Учет региона "Краснодар"
- Использование прокси
- Сохранение данных в формате JSON

## Установка

``` 
git clone bashgit@github.com:Trydimas/product_parser.git 
cd product_parser
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
scrapy crawl product_spider -O result.json
```

Если хотите задать свои категории, отредактируйте файл `start_urls.txt`.
