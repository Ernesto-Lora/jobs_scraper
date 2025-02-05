import scrapy
from urllib.parse import urljoin

class TeflSpider(scrapy.Spider):
    name = "tefl_jobs"
    start_urls = ["https://www.theteflacademy.com/tefl-jobs/"]

    def parse(self, response):
        # Extract all job URLs from the principal page
        job_urls = response.css(".section--tefl-jobs-listing h3 a::attr(href)").getall()
        print("AAAAAAAAAAAAAAAAAAAAA URL")
        print(job_urls)
        
        # Follow each job URL and call parse_job to scrape the details
        for url in job_urls:
            yield response.follow(url, self.parse_job)

        # Check for the "next page" link
        next_page = response.css('#is-load-more::attr(href)').get()
       
        if next_page:
            next_page_url = urljoin("https://www.theteflacademy.com/tefl-jobs/", next_page)
            print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO NEXT PAGE MODIFYED")
            print(next_page_url)
            yield response.follow(next_page_url, self.parse)

    def parse_job(self, response):
        # Scrape the job details
        yield {
            'job_title': response.css("h1::text").get(),
            'salary': response.css(".item--salary .item-description span::text").get(default="N/A"),
            'description': response.css(".item--description .item-description span::text").getall(),
            'requirements': response.css(".item--requirements .item-description span::text").getall(),
            'benefits': response.css(".item--benefits .item-description span::text").getall(),
            'location': response.css(".singular-job__details__head__content h3::text").get(default="N/A"),
            'business_name': response.css(".item--recruiter .item-description span::text").get(default="N/A"),
        }