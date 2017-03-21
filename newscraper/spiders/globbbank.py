from dynamic_scraper.spiders.django_spider import DjangoSpider
from blogapp.models import NewsWebsite, Article, ArticleItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from inline_requests import inline_requests
import json
#from django.utils import timezone


class ArticleSpider(DjangoSpider):

    name = 'FirstSpider'
    #base_url = 'https://www.mnb.hu/arfolyamok'
    #start_urls = [base_url]

    def __init__(self, *args, **kwargs):
        self._set_ref_object(NewsWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Article
        self.scraped_obj_item_class = ArticleItem
        super(ArticleSpider, self).__init__(self, *args, **kwargs)


    def erste(self, response):
        #['USD', 'EUR', 'CHF', 'AUD', 'CAD', 'CZK', 'DKK', 'GBP', 'HRK', 'JPY', 'NOK', 'PLN', 'RON', 'SEK']
        sel_q = Selector(response)
        eur = sel_q.xpath('//tbody[@id="exchangeRateForm:dailyRateTable:tbody"]/tr[2]/td[3]/span/text()').extract()[0]
        eur = eur + "/" + sel_q.xpath('//tbody[@id="exchangeRateForm:dailyRateTable:tbody"]/tr[2]/td[5]/span/text()').extract()[0]
        usd = sel_q.xpath('//tbody[@id="exchangeRateForm:dailyRateTable:tbody"]/tr[1]/td[3]/span/text()').extract()[0]
        usd = usd + "/" + sel_q.xpath('//tbody[@id="exchangeRateForm:dailyRateTable:tbody"]/tr[1]/td[5]/span/text()').extract()[0]
        cny = " — "
        rub = " — "
        ron = sel_q.xpath('//tbody[@id="exchangeRateForm:dailyRateTable:tbody"]/tr[13]/td[3]/span/text()').extract()[0]
        ron = ron + "/" + sel_q.xpath('//tbody[@id="exchangeRateForm:dailyRateTable:tbody"]/tr[13]/td[5]/span/text()').extract()[0]
        gbp = sel_q.xpath('//tbody[@id="exchangeRateForm:dailyRateTable:tbody"]/tr[8]/td[3]/span/text()').extract()[0]
        gbp = gbp + "/" + sel_q.xpath('//tbody[@id="exchangeRateForm:dailyRateTable:tbody"]/tr[8]/td[5]/span/text()').extract()[0]
        chf = sel_q.xpath('//tbody[@id="exchangeRateForm:dailyRateTable:tbody"]/tr[3]/td[3]/span/text()').extract()[0]
        chf = chf + "/" + sel_q.xpath('//tbody[@id="exchangeRateForm:dailyRateTable:tbody"]/tr[3]/td[5]/span/text()').extract()[0]
        return ArticleItem(     EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "http://www.erstebank.hu/ekwa-web-web/exchangeRates.jsp",
                                title = "ERSTE")


    @inline_requests
    def parse(self, response):
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    NachBank!")
        sel = Selector(response)
        eur = sel.xpath('//table[@class="datatable"]/tbody/tr[2]/td[4]/text()').extract()[0]
        usd = sel.xpath('//table[@class="datatable"]/tbody/tr[3]/td[4]/text()').extract()[0]
        cny = sel.xpath('//table[@class="datatable"]/tbody/tr[5]/td[4]/text()').extract()[-1]
        rub = sel.xpath('//table[@class="datatable"]/tbody/tr[25]/td[4]/text()').extract()[-1]
        ron = sel.xpath('//table[@class="datatable"]/tbody/tr[23]/td[4]/text()').extract()[-1]
        gbp = sel.xpath('//table[@class="datatable"]/tbody/tr[8]/td[4]/text()').extract()[-1]
        chf = sel.xpath('//table[@class="datatable"]/tbody/tr[1]/td[4]/text()').extract()[0]
        yield ArticleItem(      EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = 'https://www.mnb.hu/arfolyamok',
                                title = "NachBank")
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    BUDAPEST!")
        resp1 = yield Request("https://www.budapestbank.hu/info/arfolyamok/db_arfolyamok.php?sent=1&frm_arfolyam=CCR")
        sel_1 = Selector(resp1)
        eur = sel_1.xpath('//div[@class="table"]/table/tr[7]/td[6]/text()').extract()[0]
        eur = eur + "/" + sel_1.xpath('//div[@class="table"]/table/tr[7]/td[8]/text()').extract()[0]
        usd = sel_1.xpath('//div[@class="table"]/table/tr[13]/td[6]/text()').extract()[0]
        usd = usd + "/" + sel_1.xpath('//div[@class="table"]/table/tr[13]/td[8]/text()').extract()[0]
        cny = " — "
        rub = " — "
        ron = " — "
        gbp = sel_1.xpath('//div[@class="table"]/table/tr[8]/td[6]/text()').extract()[0]
        gbp = gbp + "/" + sel_1.xpath('//div[@class="table"]/table/tr[8]/td[8]/text()').extract()[0]
        chf = sel_1.xpath('//div[@class="table"]/table/tr[4]/td[6]/text()').extract()[0]
        chf = chf + "/" + sel_1.xpath('//div[@class="table"]/table/tr[4]/td[8]/text()').extract()[0]
        yield ArticleItem(      EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "https://www.budapestbank.hu/info/arfolyamok/db_arfolyamok.php?sent=1&frm_arfolyam=CCR",
                                title = "BUDAPEST")
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    CIB!")
        resp2 = yield Request("http://www.cib.hu/maganszemelyek/arfolyamok/arfolyamok")
        sel_2 = Selector(resp2)
        eur = sel_2.xpath('//div[@class="Content"]/table/tr[7]/td[3]/text()').extract()[0]
        eur = eur + "/" + sel_2.xpath('//div[@class="Content"]/table/tr[7]/td[5]/text()').extract()[0]
        usd = sel_2.xpath('//div[@class="Content"]/table/tr[14]/td[3]/text()').extract()[0]
        usd = usd + "/" + sel_2.xpath('//div[@class="Content"]/table/tr[14]/td[5]/text()').extract()[0]
        cny = " — "
        rub = " — "
        ron = " — "
        gbp = sel_2.xpath('//div[@class="Content"]/table/tr[8]/td[3]/text()').extract()[0]
        gbp = gbp + "/" + sel_2.xpath('//div[@class="Content"]/table/tr[8]/td[5]/text()').extract()[0]
        chf = sel_2.xpath('//div[@class="Content"]/table/tr[4]/td[3]/text()').extract()[0]
        chf = chf + "/" + sel_2.xpath('//div[@class="Content"]/table/tr[4]/td[5]/text()').extract()[0]
        yield ArticleItem(      EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "http://www.cib.hu/maganszemelyek/arfolyamok/arfolyamok",
                                title = "CIB")
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    ERSTE!")
        resp4 = yield Request("http://www.erstebank.hu/ekwa-web-web/includes/content/currency/exchangeRates.xhtml")
        yield FormRequest.from_response(resp4,
            formxpath = '//input[@id="exchangeRateForm:j_idt31"]',
            callback=self.erste
        )
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    GRANIT!")
        resp5 = yield Request("https://granitbank.hu/arfolyamok")
        sel_5 = Selector(resp5)
        eur = sel_5.xpath('//table[@class="rate_main"]/tr[4]/td[3]/text()').extract()[0]
        eur = eur + "/" + sel_5.xpath('//table[@class="rate_main"]/tr[4]/td[5]/text()').extract()[0]
        usd = sel_5.xpath('//table[@class="rate_main"]/tr[10]/td[3]/text()').extract()[0]
        usd = usd + "/" + sel_5.xpath('//table[@class="rate_main"]/tr[10]/td[5]/text()').extract()[0]
        cny = " — "
        rub = " — "
        ron = " — "
        gbp = sel_5.xpath('//table[@class="rate_main"]/tr[5]/td[3]/text()').extract()[0]
        gbp = gbp + "/" + sel_5.xpath('//table[@class="rate_main"]/tr[5]/td[5]/text()').extract()[0]
        chf = sel_5.xpath('//table[@class="rate_main"]/tr[2]/td[3]/text()').extract()[0]
        chf = chf + "/" + sel_5.xpath('//table[@class="rate_main"]/tr[2]/td[5]/text()').extract()[0]
        yield ArticleItem(      EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "https://granitbank.hu/arfolyamok",
                                title = "GRANIT")
        #
        '''
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    K&H!")
        resp6 = yield Request("https://granitbank.hu/arfolyamok")
        sel_6 = Selector(resp6)

        eur = sel_6.xpath('//table[@class="rate_main"]/tr[4]/td[3]/text()').extract()[0]
        eur = eur + "/" + sel_6.xpath('//table[@class="rate_main"]/tr[4]/td[5]/text()').extract()[0]
        usd = sel_6.xpath('//table[@class="rate_main"]/tr[10]/td[3]/text()').extract()[0]
        usd = usd + "/" + sel_6.xpath('//table[@class="rate_main"]/tr[10]/td[5]/text()').extract()[0]
        cny = " — "
        rub = " — "
        ron = " — "
        gbp = sel_6.xpath('//table[@class="rate_main"]/tr[5]/td[3]/text()').extract()[0]
        gbp = gbp + "/" + sel_6.xpath('//table[@class="rate_main"]/tr[5]/td[5]/text()').extract()[0]
        chf = sel_6.xpath('//table[@class="rate_main"]/tr[2]/td[3]/text()').extract()[0]
        chf = chf + "/" + sel_6.xpath('//table[@class="rate_main"]/tr[2]/td[5]/text()').extract()[0]
        yield ArticleItem(      EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "https://granitbank.hu/arfolyamok",
                                title = "K&H")
        '''
        #
        '''
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    MKB!")
        resp7 = yield Request("https://www.mkb.hu/apps/rates/rates?type=CAD")
        sel_7 = Selector(resp7)
        eur = sel_7.xpath('//table[@class="rate_main"]/tr[4]/td[3]/text()').extract()[0]
        eur = eur + "/" + sel_7.xpath('//table[@class="rate_main"]/tr[4]/td[5]/text()').extract()[0]
        usd = sel_7.xpath('//table[@class="rate_main"]/tr[10]/td[3]/text()').extract()[0]
        usd = usd + "/" + sel_7.xpath('//table[@class="rate_main"]/tr[10]/td[5]/text()').extract()[0]
        cny = " — "
        rub = " — "
        ron = " — "
        gbp = sel_7.xpath('//table[@class="rate_main"]/tr[5]/td[3]/text()').extract()[0]
        gbp = gbp + "/" + sel_7.xpath('//table[@class="rate_main"]/tr[5]/td[5]/text()').extract()[0]
        chf = sel_7.xpath('//table[@class="rate_main"]/tr[2]/td[3]/text()').extract()[0]
        chf = chf + "/" + sel_7.xpath('//table[@class="rate_main"]/tr[2]/td[5]/text()').extract()[0]
        yield ArticleItem(      EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "https://www.mkb.hu/apps/rates/rates?type=CAD",
                                title = "MKB")
        '''
        #['CHF'4, 'CNY'5, 'CZK', 'DKK', 'EUR'8, 'GBP'9, 'HRK', 'JPY', 'NOK', 'PLN', 'RON'14, 'RSD', 'RUB'16, 'SEK', 'TRY', 'UAH', 'USD'20]
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    OTP!")
        resp8 = yield Request("https://www.otpbank.hu/portal/hu/Arfolyamok/OTP")
        sel_8 = Selector(resp8)
        #print (sel_8.xpath('//thead//tr/td[1]/b/text()').extract())
        eur = sel_8.xpath('//thead//tr[8]/td[4]/text()').extract()[0]
        eur = eur + "/" + sel_8.xpath('//thead//tr[8]/td[5]/text()').extract()[0]
        usd = sel_8.xpath('//thead//tr[20]/td[4]/text()').extract()[0]
        usd = usd + "/" + sel_8.xpath('//thead//tr[20]/td[5]/text()').extract()[0]
        cny = sel_8.xpath('//thead//tr[5]/td[8]/text()').extract()[0]
        cny = cny + "/" + sel_8.xpath('//thead//tr[5]/td[9]/text()').extract()[0]
        rub = " — "
        ron = " — "
        gbp = sel_8.xpath('//thead//tr[9]/td[4]/text()').extract()[0]
        gbp = gbp + "/" + sel_8.xpath('//thead//tr[9]/td[5]/text()').extract()[0]
        chf = sel_8.xpath('//thead//tr[4]/td[4]/text()').extract()[0]
        chf = chf + "/" + sel_8.xpath('//thead//tr[4]/td[5]/text()').extract()[0]
        yield ArticleItem(      EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "https://www.otpbank.hu/portal/hu/Arfolyamok/OTP",
                                title = "OTP")
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    RAIFFEISEN!")
        resp9 = yield Request("https://www.raiffeisen.hu/hasznos/arfolyamok/lakossagi/valutaarfolyamok")
        sel_9 = Selector(resp9)
        eur = sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[6]/td[4]/text()').extract()[0]
        eur = eur + "/" + sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[6]/td[6]/text()').extract()[0]
        usd = sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[2]/td[4]/text()').extract()[0]
        usd = usd + "/" + sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[2]/td[6]/text()').extract()[0]
        cny = " — "
        rub = sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[13]/td[4]/text()').extract()[0]
        rub = rub + "/" + sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[13]/td[6]/text()').extract()[0]
        ron = sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[12]/td[4]/text()').extract()[0]
        ron = ron + "/" + sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[12]/td[6]/text()').extract()[0]
        gbp = sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[7]/td[4]/text()').extract()[0]
        gbp = gbp + "/" + sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[7]/td[6]/text()').extract()[0]
        chf = sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[3]/td[4]/text()').extract()[0]
        chf = chf + "/" + sel_9.xpath('//table[@class="table table-striped table-bordered rai"]/tbody/tr[3]/td[6]/text()').extract()[0]
        yield ArticleItem(      EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "https://www.raiffeisen.hu/hasznos/arfolyamok/lakossagi/valutaarfolyamok",
                                title = "RAIFFEISEN")

        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    SBERBANK!")
        #resp10 = yield Request("http://www.sberbank.hu/hu/alkalmazasok/arfolyamok.html")
        #sel_10 = Selector(resp10)
        #result = json.loads(resp10.body)
        #print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #print (reply['currencyRatesByDay'][0]['currencyRates'][0])
        #for obj in result:
        #    print (obj.get('CurrencyCode', ''))
        '''
        eur = sel_10.xpath('//table[@class="rate_main"]/tr[4]/td[3]/text()').extract()[0]
        eur = eur + "/" + sel_10.xpath('//table[@class="rate_main"]/tr[4]/td[5]/text()').extract()[0]
        usd = sel_10.xpath('//table[@class="rate_main"]/tr[10]/td[3]/text()').extract()[0]
        usd = usd + "/" + sel_10.xpath('//table[@class="rate_main"]/tr[10]/td[5]/text()').extract()[0]
        cny = " — "
        rub = " — "
        ron = " — "
        gbp = sel_10.xpath('//table[@class="rate_main"]/tr[5]/td[3]/text()').extract()[0]
        gbp = gbp + "/" + sel_10.xpath('//table[@class="rate_main"]/tr[5]/td[5]/text()').extract()[0]
        chf = sel_10.xpath('//table[@class="rate_main"]/tr[2]/td[3]/text()').extract()[0]
        chf = chf + "/" + sel_10.xpath('//table[@class="rate_main"]/tr[2]/td[5]/text()').extract()[0]
        yield ArticleItem(      EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "http://www.sberbank.hu/hu/alkalmazasok/arfolyamok.html",
                                title = "SBERBANK")
        '''

        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    UNICREDIT!")
        #resp11 = yield Request("https://www.unicreditbank.hu/hu/maganszemelyek/exchange_rate.html")
        #sel_11 = Selector(resp11)
        #rawreply = resp11.read()
        #reply = json.loads(rawreply.decode())
        #result = json.loads(resp11.body.decode('utf-8') )
        #print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #print (reply[0])
        #for obj in result:
            #print (obj.get('CurrencyCode', ''))

        '''
        eur = sel_11.xpath('//table[@class="rate_main"]/tr[4]/td[3]/text()').extract()[0]
        eur = eur + "/" + sel_11.xpath('//table[@class="rate_main"]/tr[4]/td[5]/text()').extract()[0]
        usd = sel_11.xpath('//table[@class="rate_main"]/tr[10]/td[3]/text()').extract()[0]
        usd = usd + "/" + sel_11.xpath('//table[@class="rate_main"]/tr[10]/td[5]/text()').extract()[0]
        cny = " — "
        rub = " — "
        ron = " — "
        gbp = sel_11.xpath('//table[@class="rate_main"]/tr[5]/td[3]/text()').extract()[0]
        gbp = gbp + "/" + sel_11.xpath('//table[@class="rate_main"]/tr[5]/td[5]/text()').extract()[0]
        chf = sel_11.xpath('//table[@class="rate_main"]/tr[2]/td[3]/text()').extract()[0]
        chf = chf + "/" + sel_11.xpath('//table[@class="rate_main"]/tr[2]/td[5]/text()').extract()[0]
        yield ArticleItem(      EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "https://www.unicreditbank.hu/hu/maganszemelyek/exchange_rate.html",
                                title = "UNICREDIT")
        '''
