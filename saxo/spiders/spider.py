import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import SaxoItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class SaxoSpider(scrapy.Spider):
	name = 'saxo'
	start_urls = ['https://www.home.saxo/about-us/press-releases']

	def parse(self, response):
		post_links = response.xpath('//section[@data-styles="media-element"]//a/@href').getall() + response.xpath('//div[@class="v2-bbox"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//time/@datetime').get()
		date = ''.join(re.findall(r'\d+\-\d+\-\d+',date))
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="v2-wrapper v2-wrapper--small"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=SaxoItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
