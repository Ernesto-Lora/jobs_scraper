import scrapy

class TeflSpider(scrapy.Spider):
    name = "tefl_jobs"
    start_urls = ["https://www.theteflacademy.com/blog/tefl-jobs/teach-in-japan-as-an-assistant-language-teacher/"]

    def parse(self, response):
        yield {
            'job_title': response.css("h1::text").get(),
            'salary': response.css(".item--salary .item-description span::text").get(default="N/A"),
            'description': response.css(".item--description .item-description span::text").getall(),
            'requirements': response.css(".item--requirements .item-description span::text").getall(),
            'benefits': response.css(".item--benefits .item-description span::text").getall(),
            'location': response.css(".singular-job__details__head__content h3::text").get(default="N/A"),
            'business_name': response.css(".item--recruiter .item-description span::text").get(default="N/A"),
        }