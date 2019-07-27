# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from biz.base_service import BaseService


class BannerService(BaseService):
    """

    """

    def query_banner(self, page_no=1, page_size=5):
        """
        wait
        :param page_no:
        :param page_size:
        :return:
        """
        start_index = self.page_helper(page_no, page_size)
        sql = "select * from t_banner "

        pass

    def add_banner(self, image_url, redirect_url):
        pass

    def delete_banner(self, b_id):
        pass


banner_service = BannerService()
