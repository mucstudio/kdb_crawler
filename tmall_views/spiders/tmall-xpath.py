# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#chromedriver="/usr/bin/chromedriver"
#l_option = Options()
#l_option.add_argument('headless')
##l_option.add_argument('window-size=1200x600')
##l_option.add_argument('disable-notifications')
#l_option.add_argument('remote-debugging-port=9222')
#l_option.add_argument('disable-gpu')
##l_option.binary_location = chromedriver
##l_option.binary_location = "/usr/bin/chromium-browser"
#l_option.binary_location = "/usr/bin/google-chrome"
#
#web_driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=l_option)
# web_driver = webdriver.Chrome(chromedriver)
web_driver = webdriver.Firefox()


import json

from tmall_views.items import TmallViewsItem
from tmall_views.spiders import util
from util import file
from util import log


def write_to_file(file_path, msg):
    with open("log/%s" % file_path, "a") as f:
        f.write(str(msg) + "\n")


class ToScrapeSpiderXPath(Spider):
    name = "tmall-xpath"

    allowed_domains = ['tmall.com', 'taobao.com']
    start_urls = [
        # 'https://detail.tmall.com/item.htm?spm=a1z10.3-b.w4011-9986777119.15.79c15d8JGRW05&id=539853070197&rn=934e2d1ecc4ab188c0bb95e26877b606&abbucket=4',
        # 'file:///home/kylin/workspace/kdb/kdb_crawler/test/test.html',
    ]
    total_items = 0

    def __init__(self, dt=None, keys=None, *args, **kwargs):
        super(ToScrapeSpiderXPath, self).__init__(*args, **kwargs)
        self.count = 0
        self.error_count = 0
        # if keys is None or dt is None:
        #     return
        file.create_dirs("log/")
        file.delete_dirs("log/")
        self.driver = web_driver
        # self.data_time = dt
        # url = "https://s.taobao.com/search?s=3872&q={q}&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&style=list&initiative_id=tbindexz_" + self.data_time
        from data_model.table import T_Basic_ShopBook
        # url_list = T_Basic_ShopBook.query_url_list()
        # print(url_list)
        # exit(0)
        self.start_urls = T_Basic_ShopBook.query_url_list()
        # for value in keys.split(","):
        #     #self.start_urls.append(url.format(q=value))
        #     pass

    def __del__(self):
        print("URL TOTAL ITEMS:%s\n Error ITEMS:%s" % (self.total_items, self.error_count))
        if self.driver is not None:
            self.driver.quit()

    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True, meta={
            'enable_redirect': True,
            'handle_httpstatus_list': [301, 302]
        })

    def parse(self, response):
        # return self._parse_handler(response)
        return self._parse_handler2(response)

    def _parse_handler2(self, response):
        print("URL SEARCH: " + response.url)
        write_to_file("search_url.log", response.url)
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)

        return self.__parse_tmall(response, selector)

    def _parse_handler(self, response):
        print("URL SEARCH: " + response.url)
        write_to_file("search_url.log", response.url)
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)
        if str(response.url).__contains__("s.taobao.com/search"):
            page = selector.xpath('//a[contains(@trace, "srp_select_pagedown")]/@data-value').extract_first()
            if page is not None:
                page_next_url = str(response.url).split("&s=")[0] + "&s=" + page
                print("start  next  page:" + page_next_url)
                yield Request(page_next_url, callback=self._parse_handler)
            item_urls = selector.css(".title").css(".J_ClickStat").xpath("./@href").extract()
            search_key = util.get_search_key(response.url)
            self.total_items += len(item_urls)
            if item_urls is not None:
                write_to_file("items_urls.log", '\n'.join(str(i) for i in item_urls))
                for i_url in item_urls:
                    yield Request(util.get_item_url(i_url), self.parse_item, meta={'sk': search_key})

    def parse_item(self, response):
        self.count += 1
        print("%s URL ITEM:%s" % (self.count, response.url))
        if str(response.url).__contains__("err.taobao.com"):
            self.__error("出现错误的地址：%s" % response.url)
            return None
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)
        if str(response.url).__contains__("item.taobao.com"):
            return self.__parse_taobao(response, selector)
        elif str(response.url).__contains__("detail.tmall.com"):
            return self.__parse_tmall(response, selector)
        else:
            self.__error("地址不是淘宝或则天猫:%s" % response.url)
            return None

    def __parse_taobao(self, response, selector):
        driver = self.driver
        sk = response.meta['sk']
        g_config = selector.xpath("//script[contains(.,'var g_config =')]").extract_first()
        if g_config is None:
            self.__error("解析失败:%s" % response.url)
            return None
        src_str = g_config.replace("\n\n", "\n").replace("\n\n", "\n")
        item = TmallAndTaoBaoItem()
        item['s_type'] = 1
        item['s_rid'] = src_str.split("item: {")[1].split(",\n")[8].split(":")[1].strip().replace("'", "")
        item['s_created'] = ""
        item['s_modified'] = ""
        item['s_shop_id'] = src_str.split("shop  : {")[1].split(",")[0].split(":")[1].strip().replace("'", "")
        item['s_name'] = util.decode_unicode(src_str.split("shopName         :")[1].split(",")[0].strip()).replace("'", "")
        item['s_seller_id'] = src_str.split("sellerId         :")[1].split(",")[0].strip().replace("'", "")
        item['s_seller_nick'] = src_str.split("sellerNick       :")[1].split(",")[0].strip().replace("'", "")
        item['s_url'] = "https:" + src_str.split("shop  : {")[1].split(",")[1].split(":")[1].strip().replace("'", "")
        item['s_search_key'] = sk
        item["s_raw_html"] = ""

        item['p_name'] = util.decode_unicode(src_str.split("title            :")[1].split(",")[0].strip()).replace("'", "")
        item['p_standard_price'] = selector.css("#J_StrPrice").css(".tb-rmb-num").xpath("./text()").extract_first()
        item['p_shop_price'] = selector.css("#J_PromoPriceNum").xpath("./text()").extract_first()
        item['p_comment_count'] = self._wait_get(lambda dr: Selector(text=self.driver.page_source).xpath("//li/div/div[@class='tb-rate-counter']/a/strong/text()").extract_first())
        '''30天内已售出840件，其中交易成功522件'''
        attribute = self._wait_get(lambda dr: Selector(text=self.driver.page_source).xpath("//li/div/div[@class='tb-sell-counter']/a/@title").extract_first())
        item['p_pay_count'] = selector.xpath("//li/div/div[@class='tb-sell-counter']/a/strong/text()").extract_first()
        item['p_month_sale_count'] = str(attribute).replace("30天内已售出", "")[:str(attribute).replace("30天内已售出", "").rindex("件，其")] if attribute is not None else None
        item['p_sale_count'] = item['p_month_sale_count']
        item['p_collect_count'] = self._wait_get(lambda dr: Selector(text=self.driver.page_source).xpath("//div/ul/li[@class='tb-social-fav']/a/em/text()").re_first("[0-9]+"))
        item['p_nid'] = src_str.split("itemId           :")[1].split(",")[0].strip().replace("'", "")
        item['p_cid'] = src_str.split("item: {")[1].split(",\n")[9].split(":")[1].strip().replace("'", "")
        item['p_url'] = response.url
        item['p_search_key'] = sk
        item['p_raw_html'] = ""
        return item

    def __parse_tmall(self, response, selector):
        driver = self.driver
        # sk = response.meta['sk']
        src_data = selector.xpath("//script[contains(.,'TShop.Setup')]").re_first("{\"api[\s\S]*}\n")
        json_data = json.loads(src_data)
        item_do = json_data["itemDO"]
        item = TmallViewsItem()
        #item['p_isbn'] = selector.xpath("//div[@id='J_AttrList']/ul[@id='J_AttrUL']/li").re("(isbn|ISBN).*:\xa0(.*)</li>")[1]
        #item['p_isbn'] = selector.xpath("//div[@id='J_AttrList']/ul[@id='J_AttrUL']/li").re("(isbn|ISBN).*: (.*)</li>")[1]
        item['p_isbn'] = selector.xpath("//div[@id='J_AttrList']/ul[@id='J_AttrUL']/li").re("(isbn|ISBN).*:.(.*)</li>")[1]
        #print(item['p_isbn'])
        #item['p_isbn'] = selector.xpath("//div[@id='J_AttrList']/ul[@id='J_AttrUL']/li").re_first("ISBN.*:\xa0(.*)</li>")[1]
        item['s_type'] = 2
        item['s_rid'] = item_do["rootCatId"]
        item['s_created'] = ""
        item['s_modified'] = ""
        item['s_shop_id'] = json_data["rstShopId"]
        item['s_name'] = util.url_decode(item_do["sellerNickName"])
        item['s_seller_id'] = json_data["rateConfig"]["sellerId"]
        item['s_seller_nick'] = item['s_name']
        item['s_url'] = "https:" + selector.xpath("//div[@class='slogo']/a/@href").extract_first()
        # item['s_search_key'] = sk
        item["s_raw_html"] = ""

        item['p_name'] = item_do["title"]
        item['p_standard_price'] = selector.xpath("//div[@class='tm-fcs-panel']/dl/dd/span/text()").extract_first()
        item['p_shop_price'] = selector.xpath("//div[@class='tm-fcs-panel']/dl/dd/div/span[@class='tm-price']/text()").extract_first()
        item['p_comment_count'] = self._wait_get(lambda dr: Selector(text=self.driver.page_source).css(".tm-ind-reviewCount").xpath("./div[@class='tm-indcon']/span[@class='tm-count']/text()").extract_first())
        item['p_pay_count'] = 0
        item['p_month_sale_count'] = selector.css(".tm-ind-sellCount").xpath("./div/span[@class='tm-count']/text()").extract_first()
        item['p_sale_count'] = item['p_month_sale_count']
        item['p_collect_count'] = self._wait_get(lambda dr: Selector(text=self.driver.page_source).css("#J_CollectCount").xpath("./text()").re_first("[0-9]+"))
        item['p_nid'] = item_do["itemId"]
        item['p_cid'] = item_do["categoryId"]
        item['p_url'] = response.url
        # item['p_search_key'] = sk
        item["p_raw_html"] = ""
        return item

    def _wait_get(self, method):
        """
        延时获取，如果10秒钟还没有获取完成，则返回失败
        :param method:
        :return:
        """
        result = None
        try:
            result = WebDriverWait(self.driver, 10).until(method)
        except:
            self.__error("超时获取：%s  %s" % (self.driver.current_url, self.driver.title))
            log.e()
        return result

    def __error(self, msg):
        self.error_count += 1
        write_to_file("error.log", msg)

