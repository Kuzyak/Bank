from dynamic_scraper.spiders.django_spider import DjangoSpider
from blogapp.models import NewsWebsite, Article, ArticleItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from inline_requests import inline_requests
import json
import requests
import time
from datetime import date
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
#import timezone


class ArticleSpider(DjangoSpider):

    name = 'FirstSpider'
    #base_url = 'https://www.mnb.hu/arfolyamok'
    #start_urls = [base_url]
    to_email = settings.EMAIL_HOST_USER
    from_email = to_email

    def __init__(self, *args, **kwargs):
        self._set_ref_object(NewsWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Article
        self.scraped_obj_item_class = ArticleItem
        super(ArticleSpider, self).__init__(self, *args, **kwargs)

    def kraken(self, response):
        try:
            sel = Selector(response)
            some = sel.xpath('//div[@id="ticker-top"]//div/text()').extract()
            sends1 = "{0:.2f}".format(float(some[1][1:].replace(",",""))) + "/" + some[7].split(".")[0]
            sends2 = response.request.meta['Work']
            curs = response.request.meta['curs']
            curs[sends2] = sends1
            curs["num"] = curs["num"] + 1
            if response.request.meta['num'] == "1":
                yield Request("https://www.kraken.com/charts", cookies={"ticker_pair":"ETHUSD"}, meta={"Work":"ETHUSD","num":"2", "curs":curs}, dont_filter=True, callback=self.kraken)
            elif response.request.meta['num'] == "2":
                yield Request("https://www.kraken.com/charts", cookies={"ticker_pair":"XRPUSD"}, meta={"Work":"XRPUSD","num":"3", "curs":curs}, dont_filter=True, callback=self.kraken)
            elif response.request.meta['num'] == "3":
                yield Request("https://www.kraken.com/charts", cookies={"ticker_pair":"XLMUSD"}, meta={"Work":"XLMUSD","num":"4", "curs":curs}, dont_filter=True, callback=self.kraken)
            elif response.request.meta['num'] == "4":
                yield Request("https://www.kraken.com/charts", cookies={"ticker_pair":"LTCUSD"}, meta={"Work":"LTCUSD","num":"5", "curs":curs}, dont_filter=True, callback=self.kraken)
            elif response.request.meta['num'] == "5":
                yield Request("https://www.kraken.com/charts", cookies={"ticker_pair":"XBTUSD"}, meta={"Work":"BTCUSD","num":"6", "curs":curs}, dont_filter=True, callback=self.kraken)
            if response.request.meta['num'] != "6":
                return
            else:
                print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    kraken    ----------------------------")
                for x in range(10):
                    kraken_del = Article.objects.filter(title="kraken")
                    if len(kraken_del) > 49:
                        kraken_del.first().delete()
                    else:
                        break
                yield ArticleItem(  EUR = "1",
                                    USD = curs["BTCUSD"],
                                    CNY = curs["ETHUSD"],
                                    RUB = curs["XRPUSD"],
                                    RON = curs["BCHUSD"],
                                    GBP = curs["XLMUSD"],
                                    CHF = curs["LTCUSD"],
                                    description = "EUR = None\nUSD = BTC_USD\nCNY = ETH_USD\nRUB = XRP_USD\nRON = BCH_USD\nGBP = XLM_USD\nCHF = LTC_USD",
                                    url = "https://www.kraken.com/charts",
                                    title = "kraken")
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    kraken ERROR    *******************************")

    def binance(self, response):
        try:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    binance    ----------------------------")
            sel = Selector(response)
            result = sel.xpath('//table[@class="table table-bordered table-hover"]/tbody/tr')#.extract()
            BTC_EUR = " — "
            BTC_USD = " — "
            ETH_USD = " — "
            XRP_USD = " — "
            BCH_USD = " — "
            XLM_USD = " — / — "
            LTC_USD = " — "
            for some in result:
                name = ' '.join(some.xpath('./td[2]/font/text()').extract())
                if name == 'BTC':
                    BTC_USD = some.xpath('./td[3]/text()').extract_first() + "/" + some.xpath('./td[5]/text()').extract_first()
                elif name == 'ETH':
                    ETH_USD = some.xpath('./td[3]/text()').extract_first() + "/" + some.xpath('./td[5]/text()').extract_first()
                elif name == 'XRP':
                    XRP_USD = some.xpath('./td[3]/text()').extract_first() + "/" + some.xpath('./td[5]/text()').extract_first()
                elif name == 'BCC':
                    BCH_USD = some.xpath('./td[3]/text()').extract_first() + "/" + some.xpath('./td[5]/text()').extract_first()
                elif name == 'XLM':
                    XLM_USD = some.xpath('./td[3]/text()').extract_first() + "/" + some.xpath('./td[5]/text()').extract_first()
                elif name == 'LTC':
                    LTC_USD = some.xpath('./td[3]/text()').extract_first() + "/" + some.xpath('./td[5]/text()').extract_first()
            if XLM_USD == " — / — ":
                some = Article.objects.filter(title="kraken").last()
                some = some.GBP.split('/')
                XLM_USD = "{0:.2f}".format(float(some[0])) + "/" + ("{0:,.2f}".format(float(some[1].replace(",",""))/20)).split(".")[0]
            for x in range(10):
                binance_del = Article.objects.filter(title="binance")
                if len(binance_del) > 49:
                    binance_del.first().delete()
                else:
                    break
            yield ArticleItem(      EUR = "1",
                                    USD = BTC_USD,
                                    CNY = ETH_USD,
                                    RUB = XRP_USD,
                                    RON = BCH_USD,
                                    GBP = XLM_USD,
                                    CHF = LTC_USD,
                                    description = "EUR = None\nUSD = BTC_USD\nCNY = ETH_USD\nRUB = XRP_USD\nRON = BCH_USD\nGBP = XLM_USD\nCHF = LTC_USD",
                                    url = "https://info.binance.com/en",
                                    title = "binance")
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    binance ERROR    *******************************")

    def bittrex(self, response):
        try:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    bittrex    ----------------------------")
            sel = Selector(response)
            result = json.loads(sel.xpath('//text()').extract_first())
            result = result['Data']
            BTC_EUR = " — "
            BTC_USD = " — "
            ETH_USD = " — "
            XRP_USD = " — "
            BCH_USD = " — "
            XLM_USD = " — / — "
            LTC_USD = " — "
            for some in range(0,len(result)):
                name = result[some]["CoinInfo"]["Name"]
                code = result[some]["ConversionInfo"]["RAW"][0].split('~')
                if name == 'BTC':
                    BTC_USD = "{0:.2f}".format(float(code[5])) + "/" + "{0:,.2f}".format(float(code[13])).split(".")[0]
                elif name == 'ETH':
                    ETH_USD = "{0:.2f}".format(float(code[5])) + "/" + "{0:,.2f}".format(float(code[13])).split(".")[0]
                elif name == 'XRP':
                    XRP_USD = "{0:.2f}".format(float(code[5])) + "/" + "{0:,.2f}".format(float(code[13])).split(".")[0]
                elif name == 'BCH':
                    BCH_USD = "{0:.2f}".format(float(code[5])) + "/" + "{0:,.2f}".format(float(code[13])).split(".")[0]
                elif name == 'XLM':
                    XLM_USD = "{0:.2f}".format(float(code[5])) + "/" + "{0:,.2f}".format(float(code[13])).split(".")[0]
                elif name == 'LTC':
                    LTC_USD = "{0:.2f}".format(float(code[5])) + "/" + "{0:,.2f}".format(float(code[13])).split(".")[0]
            for x in range(10):
                bittrex_del = Article.objects.filter(title="bittrex")
                if len(bittrex_del) > 49:
                    bittrex_del.first().delete()
                else:
                    break
            yield ArticleItem(      EUR = "1",
                                    USD = BTC_USD,
                                    CNY = ETH_USD,
                                    RUB = XRP_USD,
                                    RON = BCH_USD,
                                    GBP = XLM_USD,
                                    CHF = LTC_USD,
                                    description = "EUR = None\nUSD = BTC_USD\nCNY = ETH_USD\nRUB = XRP_USD\nRON = BCH_USD\nGBP = XLM_USD\nCHF = LTC_USD",
                                    url = "https://www.cryptocompare.com/coins/list/USD/1",
                                    title = "bittrex")
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    bittrex ERROR    *******************************")

    @inline_requests
    def parse(self, response):
        try:
            #
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    bitfinex    ----------------------------")
            sel = Selector(response)
            result = sel.xpath('(//table[@class="compact striped"])[1]/tbody/tr')#.extract()
            result2 = sel.xpath('(//table[@class="compact striped"])[2]/tbody/tr')#.extract()
            BTC_EUR = " — "
            BTC_USD = " — "
            ETH_BTC = " — "
            XRP_BTC = " — "
            BCH_BTC = " — "
            XLM_BTC = " — / — / — "
            LTC_BTC = " — "
            for some in result:
                name = ' '.join(some.xpath('./td[1]/text()').extract()).strip()
                if name == 'BTC EUR':
                    BTC_EUR = "{0:.2f}".format(float(some.xpath('./td[2]/text()').extract_first()))
                elif name == 'BTC USD':
                    BTC_USD = "{0:.2f}".format(float(some.xpath('./td[2]/text()').extract_first()))
                elif name == 'ETH BTC':
                    ETH_BTC = some.xpath('./td[2]/text()').extract_first()
                elif name == 'XRP BTC':
                    XRP_BTC = some.xpath('./td[2]/text()').extract_first()
                elif name == 'BCH BTC':
                    BCH_BTC = some.xpath('./td[2]/text()').extract_first()
                elif name == 'LTC BTC':
                    LTC_BTC = some.xpath('./td[2]/text()').extract_first()
            for some in result2:
                name = ' '.join(some.xpath('./td[1]/text()').extract()).strip()
                if name == 'BTC EUR' and BTC_EUR != " — ":
                    BTC_EUR = BTC_EUR + "/" + some.xpath('./td[2]/text()').extract_first().strip().split(".")[0]
                elif name == 'BTC USD' and BTC_USD != " — ":
                    BTC_USD = BTC_USD + "/" + some.xpath('./td[2]/text()').extract_first().strip().split(".")[0]
                elif name == 'ETH BTC' and ETH_BTC != " — ":
                    ETH_BTC = ETH_BTC + "/" + some.xpath('./td[2]/text()').extract_first().strip().split(".")[0]
                elif name == 'XRP BTC' and XRP_BTC != " — ":
                    XRP_BTC = XRP_BTC + "/" + some.xpath('./td[2]/text()').extract_first().strip().split(".")[0]
                elif name == 'BCH BTC' and BCH_BTC != " — ":
                    BCH_BTC = BCH_BTC + "/" + some.xpath('./td[2]/text()').extract_first().strip().split(".")[0]
                elif name == 'LTC BTC' and LTC_BTC != " — ":
                    LTC_BTC = LTC_BTC + "/" + some.xpath('./td[2]/text()').extract_first().strip().split(".")[0]
            for some in result:
                name = ' '.join(some.xpath('./td[1]/text()').extract()).strip()
                if name == 'ETH USD' and ETH_BTC != " — ":
                    ETH_BTC = ETH_BTC + "/" + "{0:.2f}".format(float(some.xpath('./td[2]/text()').extract_first()))
                elif name == 'XRP USD' and XRP_BTC != " — ":
                    XRP_BTC = XRP_BTC + "/" + "{0:.2f}".format(float(some.xpath('./td[2]/text()').extract_first()))
                elif name == 'BCH USD' and BCH_BTC != " — ":
                    BCH_BTC = BCH_BTC + "/" + "{0:.2f}".format(float(some.xpath('./td[2]/text()').extract_first()))
                elif name == 'LTC USD' and LTC_BTC != " — ":
                    LTC_BTC = LTC_BTC + "/" + "{0:.2f}".format(float(some.xpath('./td[2]/text()').extract_first()))
            try:
                bitfinex = Article.objects.filter(title="bitfinex").last()
                if BTC_EUR == " — ":
                    BTC_EUR = bitfinex.EUR
                if BTC_USD == " — ":
                    BTC_USD = bitfinex.USD
                if ETH_BTC == " — ":
                    ETH_BTC = bitfinex.CNY
                if XRP_BTC == " — ":
                    XRP_BTC = bitfinex.RUB
                if BCH_BTC == " — ":
                    BCH_BTC = bitfinex.RON
                if LTC_BTC == " — ":
                    LTC_BTC = bitfinex.CHF
            except:
                pass
            for x in range(10):
                bitfinex_del = Article.objects.filter(title="bitfinex")
                if len(bitfinex_del) > 49:
                    bitfinex_del.first().delete()
                else:
                    break
            yield ArticleItem(  EUR = BTC_EUR,
                                USD = BTC_USD,
                                CNY = ETH_BTC,
                                RUB = XRP_BTC,
                                RON = BCH_BTC,
                                GBP = XLM_BTC,
                                CHF = LTC_BTC,
                                description = "EUR = BTC_EUR\nUSD = BTC_USD\nCNY = ETH_BTC\nRUB = XRP_BTC\nRON = BCH_BTC\nGBP = XLM_BTC\nCHF = LTC_BTC",
                                url = "https://www.bitfinex.com/stats",
                                title = "bitfinex")
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    bitfinex ERROR    *******************************")

        #kraken
        time.sleep(1)
        yield Request("https://www.kraken.com/charts", cookies={"ticker_pair":"BCHUSD"}, meta={"Work":"BCHUSD","num":"1","curs":{"num":0}}, callback=self.kraken)
        #binance
        time.sleep(1)
        yield Request("https://info.binance.com/en", callback=self.binance)
        #cryptocompare
        time.sleep(1)
        yield Request("https://min-api.cryptocompare.com/data/top/totalvol?limit=100&page=0&tsym=USD", callback=self.bittrex)
        #poloniex - bad
