import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
kwargs = {
            'id': 1,
            'do_action': 'yes',
}

# 'followall' is the name of one of the spiders of the project.
process.crawl('FirstSpider', **kwargs)
process.start() # the script will block here until the crawling is finished
