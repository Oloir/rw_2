from scrapy.spiders import SitemapSpider
#SitemapSpider
#scrapy.Spider


class RendezVous(SitemapSpider):
    name = 'rv'
#    allowed_domains = ['rendez-vous.ru']
#    start_urls = ['https://www.rendez-vous.ru/catalog/odezhda/sviter/tommy_hilfiger_mw0mw14421_temno_siniy-2372652/']
    sitemap_urls = ['https://www.rendez-vous.ru/sitemap.xml']
    sitemap_rules = [('/catalog/', 'parse')]


    def parse(self, response):
        # Пляска с костылями для извлечения названия товара, которое, как правило, записывается в два тега
        # (В Scrapy можно делать красивее, через Item, но там сложности с неопределнными праметрами):
        title = []
        title_list = response.css(".item-name-title::text").extract() + response.css(".item-name-title a::text").extract()
        title_string = ''.join(title_list)
        title.append(title_string)

        # Достаю определенные параметры, которые есть у всех товаров. Тут все просто:
        article = response.css(".item-vendor-code::text").extract()
        price = response.css(".item-price-value::attr(content)").extract()

        # Достаю неопределенные параметры, которе варьируются от товара к товару. Сначала их названия:
        data = response.css(".data-title::text").extract()
        # А потом значения:
        data2 = response.css(".table-of-data dd::text").extract()
        # Объединяю их в словарь:
        dic1 = dict(zip(data, data2))

        # Работаю с определнными параметрами, упакоовываю в словарь:
        row_data = zip(title, article, price)
        for item in row_data:
            scraped_info0 = {
                'URL': response.url,
                'Название': item[0],
                'Артикул': item[1],
                'Цена': item[2],
            }
            # И объединяю этот словарь со словарем, в который упакованы неопределенные парамтеры:
            scraped_info = {**scraped_info0, **dic1}
            yield scraped_info