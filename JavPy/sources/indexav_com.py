# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import map
import requests
from JavPy.sources.BaseSource import ISearchByActress, IGetBrief
import bs4
from JavPy.functions.datastructure import Brief
from JavPy.utils.common import try_evaluate

import time

class IndexAVCom(ISearchByActress, IGetBrief):

    @classmethod
    def search_by_actress(cls, actress, up_to):
        print(time.clock())
        url = "https://indexav.com/actor/" + actress
        rsp = requests.get(url)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        print(time.clock())
        tab_content = bs.select('.tab-content')[-1]
        print(time.clock())
        boxes = tab_content.children

        res = []

        cnt = 0

        for box in boxes:
            print(time.clock())
            if not isinstance(box, bs4.Tag):
                continue
            # release_date = box.select('.col-sm-2')[0].span.text
            # if u"予定" in release_date:
            #     continue

            brief = cls.__get_brief_by_box(box)

            res.append(brief)
            cnt += 1

            if up_to and cnt >= up_to:
                print(time.clock())
                return res
        return res

    @classmethod
    def get_brief(cls, code):
        url = "https://indexav.com/search?keyword=" + code
        rsp = requests.get(url)

        if rsp.status_code != 200:
            return None

        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        box = bs.find(name='div', attrs={'class': 'bs-callout'})
        if not box:
            return None
        return cls.__get_brief_by_box(box)

    @staticmethod
    def __get_brief_by_box(box):
        code = box.find(name='span', attrs={'class': 'video_id'}).text
        div = box.find(name='div', attrs={'class': 'col-sm-7'})
        actress = ", ".join(map(lambda x: x.text, div.find_all(name='div', attrs={'class': 'col-xs-6'})))
        title = div.find(name='span', attrs={'class': 'video_title'}).text
        img, _ = try_evaluate(lambda: div.find(name='span', attrs={'class': 'preview_btn'}).attrs['rel'])
        release_date = box.find(name='div', attrs={'class': 'col-sm-2'}).span.text

        brief = Brief()
        brief.title = title.strip()
        brief.preview_img_url = img
        brief.code = code.strip()
        brief.actress = actress.strip()
        brief.set_release_date(release_date)
        return brief


if __name__ == '__main__':
    print(IndexAVCom.search_by_actress("深田えいみ", 30))