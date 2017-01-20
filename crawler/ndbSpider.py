import scrapy
from scrapy.selector import Selector
# from scrapy import optional_features
# optional_features.remove('boto')
# command to run: scrapy runspider ndbSpider.py > result.txt

class ndbSpider(scrapy.Spider):
    name = 'nal.usda.spider'
    max = 1000
    offset = max
    next_pag = 0
    start_urls = ['https://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=%s&offset=0&order=asc' % max]

    def parse(self, response):
        items = response.xpath('//table[@class="table table-bordered table-striped table-fixed-header table-hover"]/tbody/tr/td[1]/a/text()').extract()
        # print ">>>>>>>> ", len(items)
        for item in items:
            # yield {"id": str(item).strip()}
            print {"id": str(item).strip()}

        cur_page = response.xpath('//span[@class="currentStep"]/text()').extract_first()
        self.next_pag = self.next_pag + 1
        print "cur_page", cur_page, self.next_pag, self.next_pag * self.max

        if int(cur_page) == self.next_pag:
            self.offset = self.next_pag * self.max
            next_page = 'https://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=%s&offset=%s&order=asc' % (self.max, self.offset)
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        else:
            print 'finished'