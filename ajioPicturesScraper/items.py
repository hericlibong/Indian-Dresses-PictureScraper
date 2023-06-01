# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AjiopicturesscraperItem(scrapy.Item):
    category = scrapy.Field()
    productId = scrapy.Field()
    name = scrapy.Field()
    brandName = scrapy.Field()
    currentPrice = scrapy.Field()
    originalPrice = scrapy.Field()
    currency = scrapy.Field()
    discountPercent = scrapy.Field()
    imagePrimary = scrapy.Field()
    extraImagePrimary = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
