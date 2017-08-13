# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

from util import text

class TmallViewsPipeline(object):
    def process_item(self, item, spider):
        # class__ = self.__class__
        if item is not None:
            if item["p_standard_price"] is None:
                item["p_standard_price"] = item["p_shop_price"]
            if item["p_shop_price"] is None:
                item["p_shop_price"] = item["p_standard_price"]

            item["p_collect_count"] = text.to_int(item["p_collect_count"])
            item["p_comment_count"] = text.to_int(item["p_comment_count"])
            item["p_month_sale_count"] = text.to_int(item["p_month_sale_count"])
            item["p_sale_count"] = text.to_int(item["p_sale_count"])
            item["p_standard_price"] = text.to_string(item["p_standard_price"], "0")
            item["p_shop_price"] = text.to_string(item["p_shop_price"], "0")
            item["p_pay_count"] = item["p_pay_count"] if item["p_pay_count"] is not "-" else "0"
            print('+'*50)
            print(item)
            print('+'*50)
            return item
        else:
            raise DropItem("Item is None %s" % item)
