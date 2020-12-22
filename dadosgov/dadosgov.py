
import scrapy as sc
import unidecode

class DataGov_br(sc.Spider):
    name = "DataGov.br"
    dataset = []
    url = 'https://dados.gov.br'

    def start_requests(self):
        
        base_query = 'ufrn'

        queries = [
            'matricula'
        ]

        for query in queries:
            query_url = self.url + '/dataset' + '?q=' + base_query + '+' + query
            yield sc.Request(url=query_url, callback=self.parse_first_page)

        self.save_dataset()
            
    def save_dataset(self):
        print("Done.")


    def parse_first_page(self, response):
        pagination = response.css('div.pagination')
        pagination_max = 1;

        if (pagination):
            pagination = pagination[0]
            pagination_str = pagination.xpath(".//li//text()").extract()
            pagination_max = int(pagination_str[-2])

        for p in range(pagination_max):
            page_url = response.url + '&page=' + str(p+1)
            yield sc.Request(url=page_url, callback=self.parse_pages)

    def parse_pages(self, response):
        datasets = response.css('h3.dataset-heading')
        for dataset in datasets:
            dataset_url = self.url + dataset.xpath('.//a//@href').extract_first()
            yield sc.Request(url=dataset_url, callback=self.parse_dataset)
    
    def parse_dataset(self, response):
        dataset_url = response.url
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",dataset_url)
        article = response.css('article.module')
        headings = article.css('a.heading')
        for heading in headings:
            data_url = self.url + heading.xpath('./@href').extract_first()
            yield sc.Request(url=data_url, callback=self.parse_data)

    def parse_data(self, response):
        data_url   = response.xpath("//a[contains(@class, 'btn')]/@href").extract_first()
        data_title = response.xpath("//h1[contains(@class,'page-heading')]/text()").extract_first()
        
        data_description = ''.join([x.extract().strip() for x in response.xpath(".//div[contains(@class,'prose')]//text()")])

        table_info  = response.xpath(".//table[contains(@class, 'table-condensed')]")[0]
        table_field = table_info.xpath("./tbody/tr/th/text()").extract()
        table_value = table_info.xpath("./tbody/tr/td/text()").extract()
        data_info   = dict()
        for field,value in zip(table_field, table_value):
            field = unidecode.unidecode(field.strip().lower().replace(' ','_'))
            value = value.strip()
            data_info[field] = value
        
        data = { 
                    'url'         : data_url,
                    'title'       : data_title,
                    'description' : data_description,
                    'info'        : data_info
               }

        self.dataset.append(data);

    def __del__(self):
        import json
        print("Closing...")
        with open('/mnt/c/dev/source/crawl_py/datagov/query.json', 'w+', encoding='utf-8') as json_file:
            json.dump(self.dataset, json_file, ensure_ascii=False, indent=4)
        print("... closed.")

