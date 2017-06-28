from dynamic_scraper.spiders.django_spider import DjangoSpider
from blogapp.models import NewsWebsite, Article, ArticleItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from inline_requests import inline_requests
import json
import requests
from datetime import date
from datetime import datetime
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
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    ERSTE!")
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
        yield ArticleItem(     EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "http://www.erstebank.hu/ekwa-web-web/exchangeRates.jsp",
                                title = "ERSTE")


    def nach_history(self, response):
        #CHF9    CNY10   EUR21   GBP24   RON59   RUB61   USD71
        #lis = ['22','72','11','62','60','25','10']
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    NachHistory!")
        sel_q = Selector(response)
        rows = sel_q.xpath('//table[@class="pricetable"]/tbody/tr')#.extract()
        data = "".join(rows[0].xpath('.//td[1]/div/span/text()').extract())
        eur = "".join(rows[0].xpath('.//td[22]/div/span/text()').extract())
        usd = "".join(rows[0].xpath('.//td[72]/div/span/text()').extract())
        cny = "".join(rows[0].xpath('.//td[11]/div/span/text()').extract())
        rub = "".join(rows[0].xpath('.//td[62]/div/span/text()').extract())
        ron = "".join(rows[0].xpath('.//td[60]/div/span/text()').extract())
        gbp = "".join(rows[0].xpath('.//td[25]/div/span/text()').extract())
        chf = "".join(rows[0].xpath('.//td[10]/div/span/text()').extract())
        y=0
        step = int("".join(rows[0].xpath('.//td[1]/div/span/text()').extract()).split(" ")[0])
        for some in rows[1:]:
            now = int("".join(some.xpath('.//td[1]/div/span/text()').extract()).split(" ")[0])
            test = now - step
            if (test > 1):
                data_z = int(data.split("/")[-1][:2])
                for num in range(1,test):
                    y=y+1
                    data_x = ""
                    if data_z+num <=9:
                        data_x = "0" + str(data_z + num)
                    else:
                        data_x = str(data_z + num)
                    data = data + "/" + data_x + data.split("/")[-1][2:]
                    eur = eur + "/" + eur.split("/")[-1]
                    usd = usd + "/" + usd.split("/")[-1]
                    cny = cny + "/" + cny.split("/")[-1]
                    rub = rub + "/" + rub.split("/")[-1]
                    ron = ron + "/" + ron.split("/")[-1]
                    gbp = gbp + "/" + gbp.split("/")[-1]
                    chf = chf + "/" + chf.split("/")[-1]
            y=y+1
            data = data + "/" + "".join(some.xpath('.//td[1]/div/span/text()').extract())
            eur = eur + "/" + "".join(some.xpath('.//td[22]/div/span/text()').extract())
            usd = usd + "/" + "".join(some.xpath('.//td[72]/div/span/text()').extract())
            cny = cny + "/" + "".join(some.xpath('.//td[11]/div/span/text()').extract())
            rub = rub + "/" + "".join(some.xpath('.//td[62]/div/span/text()').extract())
            ron = ron + "/" + "".join(some.xpath('.//td[60]/div/span/text()').extract())
            gbp = gbp + "/" + "".join(some.xpath('.//td[25]/div/span/text()').extract())
            chf = chf + "/" + "".join(some.xpath('.//td[10]/div/span/text()').extract())
            step = now
        yield ArticleItem(     EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                description = data,
                                url = "https://www.mnb.hu/en/arfolyam-lekerdezes",
                                title = "NachHistory")

    def budapest(self, response):
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    BUDAPEST!")
        sel_1 = Selector(response)
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

    def cib(self, response):
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    CIB!")
        sel_2 = Selector(response)
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

    def granit(self, response):
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    GRANIT!")
        sel_5 = Selector(response)
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

    def otp(self, response):
        #['CHF'4, 'CNY'5, 'CZK', 'DKK', 'EUR'8, 'GBP'9, 'HRK', 'JPY', 'NOK', 'PLN', 'RON'14, 'RSD', 'RUB'16, 'SEK', 'TRY', 'UAH', 'USD'20]
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    OTP!")
        sel_8 = Selector(response)
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

    def raiffeisen(self, response):
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    RAIFFEISEN!")
        sel_9 = Selector(response)
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

    def k_and_h(self, response):
        #actualDateInLong =
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   K&H!")
        sel_q = Selector(response)
        data = sel_q.xpath('//body/script[@type="text/javascript"]').extract()[-3].split("actualDateInLong = ")[-1].split(";")[0]
        payload = {'_rateslisterportlet_WAR_ratescalculatorportlet_dateInLong': data}
        headers = {     'Accept': 'application/json, text/javascript, */*',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        respons3 = requests.post('https://www.kh.hu/valuta-deviza-arfolyam?p_p_id=rateslisterportlet_WAR_ratescalculatorportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getRates&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_pos=2&p_p_col_count=6',
                                    headers = headers,
                                    data=payload)
        sel_14 = Selector(respons3)
        result = json.loads(sel_14.xpath('//p').extract()[0][3:-4])
        for some in range(0,len(result["results"][0]["results"][1]["results"])):
            if result["results"][0]["results"][1]["results"][some]["currencyCode"] == 'CHF':
                chf = str(result["results"][0]["results"][1]["results"][some]["bidPrice"]) + "/" + str(result["results"][0]["results"][1]["results"][some]["askPrice"])
            elif result["results"][0]["results"][1]["results"][some]["currencyCode"] == 'EUR':
                eur = str(result["results"][0]["results"][1]["results"][some]["bidPrice"]) + "/" + str(result["results"][0]["results"][1]["results"][some]["askPrice"])
            elif result["results"][0]["results"][1]["results"][some]["currencyCode"] == 'GBP':
                gbp = str(result["results"][0]["results"][1]["results"][some]["bidPrice"]) + "/" + str(result["results"][0]["results"][1]["results"][some]["askPrice"])
            elif result["results"][0]["results"][1]["results"][some]["currencyCode"] == 'USD':
                usd = str(result["results"][0]["results"][1]["results"][some]["bidPrice"]) + "/" + str(result["results"][0]["results"][1]["results"][some]["askPrice"])
        try:
            for some in range(0,len(result["results"][1]["results"][0]["results"])):
                if result["results"][1]["results"][0]["results"][some]["currencyCode"] == 'CNY':
                    cny = str(result["results"][1]["results"][0]["results"][some]["bidPrice"]) + "/" + str(result["results"][1]["results"][0]["results"][some]["askPrice"])
                elif result["results"][1]["results"][0]["results"][some]["currencyCode"] == 'RON':
                    ron = str(result["results"][1]["results"][0]["results"][some]["bidPrice"]) + "/" + str(result["results"][1]["results"][0]["results"][some]["askPrice"])
                elif result["results"][1]["results"][0]["results"][some]["currencyCode"] == 'RUB':
                    rub = str(result["results"][1]["results"][0]["results"][some]["bidPrice"]) + "/" + str(result["results"][1]["results"][0]["results"][some]["askPrice"])
        except:
            for some in range(0,len(result["results"][0]["results"][0]["results"])):
                if result["results"][0]["results"][0]["results"][some]["currencyCode"] == 'CNY':
                    cny = str(result["results"][0]["results"][0]["results"][some]["bidPrice"]) + "/" + str(result["results"][0]["results"][0]["results"][some]["askPrice"])
                elif result["results"][0]["results"][0]["results"][some]["currencyCode"] == 'RON':
                    ron = str(result["results"][0]["results"][0]["results"][some]["bidPrice"]) + "/" + str(result["results"][0]["results"][0]["results"][some]["askPrice"])
                elif result["results"][0]["results"][0]["results"][some]["currencyCode"] == 'RUB':
                    rub = str(result["results"][0]["results"][0]["results"][some]["bidPrice"]) + "/" + str(result["results"][0]["results"][0]["results"][some]["askPrice"])
        yield ArticleItem(      EUR = eur,
                                USD = usd,
                                CNY = cny,
                                RUB = rub,
                                RON = ron,
                                GBP = gbp,
                                CHF = chf,
                                #description = des,
                                url = "https://www.kh.hu/valuta-deviza-arfolyam",
                                title = "K&H")

    def mkb(self, response):
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    MKB!")
        sel_7 = Selector(response)
        result = json.loads(sel_7.xpath('//p').extract()[0][3:-4])
        result = result["arfolyamok"][0]["currencies"]
        for some in range(0,len(result)):
            if result[some]["currencyId"] == 'CHF':
                chf = str(result[some]["buy"]) + "/" + str(result[some]["sell"])
            elif result[some]["currencyId"] == 'CNY':
                cny = str(result[some]["buy"]) + "/" + str(result[some]["sell"])
            elif result[some]["currencyId"] == 'EUR':
                eur = str(result[some]["buy"]) + "/" + str(result[some]["sell"])
            elif result[some]["currencyId"] == 'GBP':
                gbp = str(result[some]["buy"]) + "/" + str(result[some]["sell"])
            elif result[some]["currencyId"] == 'RON':
                ron = str(result[some]["buy"]) + "/" + str(result[some]["sell"])
            elif result[some]["currencyId"] == 'RUB':
                rub = str(result[some]["buy"]) + "/" + str(result[some]["sell"])
            elif result[some]["currencyId"] == 'USD':
                usd = str(result[some]["buy"]) + "/" + str(result[some]["sell"])
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

    def kredit(self, response):
        #
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    KREDIT!")
        sel = Selector(response)
        result = sel.xpath('//div[@class="result_list"]/div')[:-1]#.extract()
        print (len(result))
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        name = ''
        thm = ''
        year = ''
        period = ''
        zatrat = ''
        info = 'Info'
        other = ''
        des = 'EUR = name\nUSD = THM\nCNY = year\nRUB = period\nRON = zatrat\nGBP = info\nCHF = other'
        for some in result:
            name = name + some.xpath('.//h3[@class="productname"]/text()').extract()[0] + "/"
            thm = thm + some.xpath('.//div[@class="product_col3"]/text()').extract()[0][:-1] + "/"
            year = year + some.xpath('.//div[@class="col"]/strong/text()').extract()[0][:-1] + "/"
            period = period + some.xpath('.//div[@class="col last"]/strong/text()').extract()[0] + "/"
            zatrat = zatrat + some.xpath('.//div[@class="col kezdeti_koltseg"]/strong/text()').extract()[0][:-3] + "|" + "".join(some.xpath('.//div[@class="col kezdeti_koltseg"]/span/strong/text()').extract())[:-3] + "/"
            other = other + some.xpath('.//div[@class="right"]/text()').extract()[0].split(": ")[-1].split(" ")[0] + "/"
        yield ArticleItem(      EUR = name[:-1],
                                USD = thm[:-1],
                                CNY = year[:-1],
                                RUB = period[:-1],
                                RON = zatrat[:-1].replace(" ",""),
                                GBP = info,
                                CHF = other[:-1],
                                description = des,
                                url = "https://www.bankracio.hu/hitelkalkulator/lakashitel/2-lakasvasarlasi-hitel-uj-lakasra",
                                title = "KREDIT")


    @inline_requests
    def parse(self, response):
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    NachBank!")
        sel = Selector(response)
        result1 = sel.xpath('//table[@class="datatable"]/tbody/tr')[:-1]
        for some1 in result1:
            name = some1.xpath('.//td//text()').extract()[0]
            value = some1.xpath('.//td//text()').extract()[-1]
            if (name == "EUR"):
                eur = value
            elif (name == "USD"):
                usd = value
            elif (name == "CNY"):
                cny = value
            elif (name == "RUB"):
                rub = value
            elif (name == "RON"):
                ron = value
            elif (name == "GBP"):
                gbp = value
            elif (name == "CHF"):
                chf = value
        print (sel.xpath('//table[@class="datatable"]/tbody/tr[5]/td//text()').extract())
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

        #KREDIT
        yield Request("https://www.bankracio.hu/hitelkalkulator/lakashitel/2-lakasvasarlasi-hitel-uj-lakasra", callback=self.kredit)
        #BUDAPEST
        yield Request("https://www.budapestbank.hu/info/arfolyamok/db_arfolyamok.php?sent=1&frm_arfolyam=CCR", callback=self.budapest)

        #CIB
        yield Request("http://www.cib.hu/maganszemelyek/arfolyamok/arfolyamok", callback=self.cib)
        # ERSTE!
        resp4 = yield Request("http://www.erstebank.hu/ekwa-web-web/includes/content/currency/exchangeRates.xhtml")
        yield FormRequest.from_response(resp4,
            formxpath = '//input[@id="exchangeRateForm:j_idt31"]',
            callback=self.erste
        )

        # Valuta History
        resp12 = yield Request("https://www.mnb.hu/en/arfolyam-lekerdezes")
        yield FormRequest.from_response(resp12,
            formxpath = '//input[@id="geterates"]',
            callback=self.nach_history
        )
        #GRANIT
        yield Request("https://granitbank.hu/arfolyamok", callback=self.granit)

        #OTP
        yield Request("https://www.otpbank.hu/portal/hu/Arfolyamok/OTP", callback=self.otp)

        #RAIFFEISEN
        yield Request("https://www.raiffeisen.hu/hasznos/arfolyamok/lakossagi/valutaarfolyamok", callback=self.raiffeisen)

        #K&H   k_and_h
        yield Request("https://www.kh.hu/valuta-deviza-arfolyam", callback=self.k_and_h)

        #MKB
        yield Request("https://www.mkb.hu/apps/rates/rates?type=CAD", callback=self.mkb, method="GET")

        #UNICREDIT

        try:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   UNICREDIT!")
            d = datetime.today()
            date_now = str(d.year)
            if len(str(d.month)) == 1:
                date_now = date_now + "0" + str(d.month)
            else:
                date_now = date_now + str(d.month)
            if len(str(d.day)) == 1:
                date_now = date_now + "0" + str(d.day)
            else:
                date_now = date_now + str(d.day)
            date_now = date_now + "T"
            if len(str(d.hour)) == 1:
                date_now = date_now + "0" + str(d.hour)
            else:
                date_now = date_now + str(d.hour)
            date_now = date_now + "23:00:00.000+0300"
            payload = {'Currency': '*ALL','DateFrom':date_now,'DateTo':date_now}
            headers = {     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
                            'Accept': '*/*',
                            'Content-Type': 'application/json',
                            'EntityCode': 'HU',
                            'Language': 'HU',
                            'SourceSystem': 'PWS',
                            'Product': 'PWS'}
            respons0 = requests.post('https://www.unicreditbank.hu/cwa/GetExchangeRates', headers = headers, data=json.dumps(payload))
            sel_11 = Selector(respons0)
            result = json.loads(sel_11.xpath('//p').extract()[0][3:-4])
            chf = " — "
            cny = " — "
            eur = " — "
            gbp = " — "
            ron = " — "
            rub = " — "
            usd = " — "
            for some in range(0,len(result)):
                if result[some]["CurrencyCode"] in ['CHF','CNY','EUR','GBP','RON','RUB','USD']:
                    if result[some]["CurrencyCode"] == 'CHF':
                        chf = str("%.2f" % result[some]["PurchaseRate"]) + "/" + str("%.2f" % result[some]["SaleRate"])
                    elif result[some]["CurrencyCode"] == 'CNY':
                        cny = str("%.2f" % result[some]["CashPurchaseRate"]) + "/" + str("%.2f" % result[some]["CashSaleRate"])
                    elif result[some]["CurrencyCode"] == 'EUR':
                        eur = str("%.2f" % result[some]["PurchaseRate"]) + "/" + str("%.2f" % result[some]["SaleRate"])
                    elif result[some]["CurrencyCode"] == 'GBP':
                        gbp = str("%.2f" % result[some]["PurchaseRate"]) + "/" + str("%.2f" % result[some]["SaleRate"])
                    elif result[some]["CurrencyCode"] == 'RON':
                        ron = str("%.2f" % result[some]["CashPurchaseRate"]) + "/" + str("%.2f" % result[some]["CashSaleRate"])
                    elif result[some]["CurrencyCode"] == 'RUB':
                        rub = str("%.2f" % result[some]["CashPurchaseRate"]) + "/" + str("%.2f" % result[some]["CashSaleRate"])
                    elif result[some]["CurrencyCode"] == 'USD':
                        usd = str("%.2f" % result[some]["PurchaseRate"]) + "/" + str("%.2f" % result[some]["SaleRate"])
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
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   UNICREDIT! ERROR or Weekend")

        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    SBERBANK!")
        d = datetime.today()
        date_now = str(d.year)
        if len(str(d.month)) == 1:
            date_now = date_now + ".0" + str(d.month)
        else:
            date_now = date_now + "." + str(d.month)
        if len(str(d.day)) == 1:
            date_now = date_now + ".0" + str(d.day)
        else:
            date_now = date_now + "." + str(d.day)
        payload = { 'maxDays':"60",
                    'language':"hu",
                    'rateType':"valuta",
                    'dateFrom':date_now,
                    'allCurrency':"true"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        respons5 = requests.post('https://www.sberbank.hu/servlet/currencyRateServlet',
                                    headers = headers,
                                    data=payload)
        sel_10 = Selector(respons5)
        result = json.loads(sel_10.xpath('//p').extract()[0][3:-4])
        print (result["notFound"])
        if result["notFound"] == False:
            cny = " — "
            ron = " — "
            for some in range(0,len(result["currencyRatesByDay"][0]["currencyRates"])):
                if result["currencyRatesByDay"][0]["currencyRates"][some]["currency"] == 'CHF':
                    chf = str(result["currencyRatesByDay"][0]["currencyRates"][some]["buyRate"]) + "/" + str(result["currencyRatesByDay"][0]["currencyRates"][some]["sellRate"])
                elif result["currencyRatesByDay"][0]["currencyRates"][some]["currency"] == 'EUR':
                    eur = str(result["currencyRatesByDay"][0]["currencyRates"][some]["buyRate"]) + "/" + str(result["currencyRatesByDay"][0]["currencyRates"][some]["sellRate"])
                elif result["currencyRatesByDay"][0]["currencyRates"][some]["currency"] == 'GBP':
                    gbp = str(result["currencyRatesByDay"][0]["currencyRates"][some]["buyRate"]) + "/" + str(result["currencyRatesByDay"][0]["currencyRates"][some]["sellRate"])
                elif result["currencyRatesByDay"][0]["currencyRates"][some]["currency"] == 'RUB':
                    rub = str(result["currencyRatesByDay"][0]["currencyRates"][some]["buyRate"]) + "/" + str(result["currencyRatesByDay"][0]["currencyRates"][some]["sellRate"])
                elif result["currencyRatesByDay"][0]["currencyRates"][some]["currency"] == 'USD':
                    usd = str(result["currencyRatesByDay"][0]["currencyRates"][some]["buyRate"]) + "/" + str(result["currencyRatesByDay"][0]["currencyRates"][some]["sellRate"])
            yield ArticleItem(      EUR = eur,
                                    USD = usd,
                                    CNY = cny,
                                    RUB = rub,
                                    RON = ron,
                                    GBP = gbp,
                                    CHF = chf,
                                    description = date_now,
                                    url = "http://www.sberbank.hu/hu/alkalmazasok/arfolyamok.html",
                                    title = "SBERBANK")
        else:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   SBERBANK! ERROR or Weekend")
        
