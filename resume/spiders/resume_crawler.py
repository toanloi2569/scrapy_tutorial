import scrapy
import logging
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from scrapy.spiders.init import InitSpider
from scrapy.linkextractors import LinkExtractor
from resume.items import ResumeItem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Root')

class ResumeSpider(scrapy.Spider):
    name = "resume"

    # def start_requests(self):
    allowed_domains = ["example.com"]
    login_page = 'https://example.com/v2/login'
    start_urls = [
        'https://example.com/v2/candidate/'
    ]

    def parse(self, response):
        """Generate a login request."""
        return FormRequest.from_response(
                    response,
                    formdata={'_username': 'kopas31145@mimpi99.com', '_password': 'Mssv20162569', '_target_path':'/v2/'},
                    callback=self.check_login_response, 
                    dont_filter = True
                )

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "authentication failed" in response.body:
            self.log("Login failed")
            return
        else:
            return Request(url=self.start_urls[0],
               callback=self.parse_resume, 
               dont_filter=True
            )


    def parse_resume(self, response):     
        with open('page.html', 'wb') as f:
            f.write(response.body)           

        resume_divs = response.css('.info-resume').extract()
        for resume_div in resume_divs:
            resume = ResumeItem()
            resume["name"] = resume_div.css('p.name.name-not-viewed span a::text').extract()[0]
            # id_ = scrapy.Field()
            # attach_cv = scrapy.Field()

            # career = scrapy.Field()
            # job_title = scrapy.Field()
            # expected_salary = scrapy.Field()
            # year_of_experience = scrapy.Field()
            # location = scrapy.Field()

            # link = scrapy.Field()
            # link_cv = scrapy.Field()         
                                                                                    
            yield resume

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)