import scrapy
import json

from scrapy import Item, Field
from ajioPicturesScraper.items import AjiopicturesscraperItem


class AjiopicturesSpider(scrapy.Spider):
    name = "ajiopictures"
    allowed_domains = ["ajio.com"]
    #start_urls = ["https://www.ajio.com/api/category/830303004?fields=SITE&currentPage=1&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&gridColumns=3&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=false&displayRatings=true"]
                # https://www.ajio.com/api/category/830316007?fields=SITE&currentPage=1&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&gridColumns=3&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=false&displayRatings=true
    
    cats_id = ['830303004','830316007']

    def start_requests(self):
        for cat in self.cats_id:
            start_url = f'https://www.ajio.com/api/category/{cat}?fields=SITE&currentPage=1&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&gridColumns=3&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=false&displayRatings=true'
            yield scrapy.Request(url=start_url, callback=self.parse)



    
    
    
    def parse(self, response):
        parse_json = json.loads(response.body)
        data = parse_json['products']
        for item in data :
            category = item['rilfnlBreadCrumbList']['rilfnlBreadCrumb'][0]['name']
            productId = item['code']
            name = item['name']
            brand = item['fnlColorVariantData']['brandName']
            price = item['price']['value']
            originalPrice = item['wasPriceData']['value']
            currency = item['price']['currencyIso']
            try:
                discountPercent = item['discountPercent'].replace('off', '').strip()
            except :
                discountPercent = None
            imagePrimary = item['images'][0]['url']
            extraImagePrimary = [extra_image['images'][0]['url'] for extra_image in item['extraImages']]
            
            custom_items = AjiopicturesscraperItem(
            category=category,    
            productId=productId,
            name=name,
            brandName=brand,
            currentPrice=price,
            originalPrice=originalPrice,
            currency=currency,
            discountPercent=discountPercent,
            imagePrimary=imagePrimary,
            extraImagePrimary=extraImagePrimary
            

        )
            custom_items['image_urls'] = [imagePrimary] + extraImagePrimary
            yield custom_items

        
        page = parse_json['pagination']['currentPage'] 
        next_page = page + 1
        for cat in self.cats_id:

            url = f'https://www.ajio.com/api/category/{cat}?fields=SITE&currentPage={next_page}&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&gridColumns=3&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=false&displayRatings=true'
            if next_page <= parse_json['pagination']['totalPages']:
                yield scrapy.Request(url=url, callback=self.parse)