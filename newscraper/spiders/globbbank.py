from dynamic_scraper.spiders.django_spider import DjangoSpider
from blogapp.models import NewsWebsite, Article, ArticleItem
from scrapy.selector import Selector


class ArticleSpider(DjangoSpider):

    name = 'FirstSpider'
    #base_url = 'https://www.mnb.hu/arfolyamok'
    #start_urls = [base_url]

    def __init__(self, *args, **kwargs):
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self._set_ref_object(NewsWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Article
        self.scraped_obj_item_class = ArticleItem
        super(ArticleSpider, self).__init__(self, *args, **kwargs)

    def parse(self, response):
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    Some new result!")
        sel = Selector(response)
        eur = sel.xpath('//table[@class="datatable"]/tbody/tr[2]/td[4]/text()').extract()[0]
        usd = sel.xpath('//table[@class="datatable"]/tbody/tr[3]/td[4]/text()').extract()[0]
        uah = sel.xpath('//table[@class="datatable"]/tbody/tr[30]/td[4]/text()').extract()[-1]
        rub = sel.xpath('//table[@class="datatable"]/tbody/tr[25]/td[4]/text()').extract()[-1]
        ron = sel.xpath('//table[@class="datatable"]/tbody/tr[23]/td[4]/text()').extract()[-1]
        gbp = sel.xpath('//table[@class="datatable"]/tbody/tr[8]/td[4]/text()').extract()[-1]
        chf = sel.xpath('//table[@class="datatable"]/tbody/tr[1]/td[4]/text()').extract()[0]
        #for some in page:
        #eur = some.xpath('.//td[1]//text()').extract()[0]
        return ArticleItem(     EUR = eur,
                                USD = usd,
                                UAH = uah,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                title = "NachBank")
