# encoding:utf-8
'''
author: ztcooper
contact: 1060214139@qq.com
LICENSE: MIT

通过DocID构造接口链接
'''

import re
from GetAPI import GetAPI
from DataOutput import DataOutput


class UrlManager(object):

    def get_DocID(self, Index):
        p_docid = re.compile(r'"文书ID\\":\\"(.*?)\\"')
        print("获取url中……")
        data = GetAPI().get_data(Index)
        return p_docid.findall(data)

    def add_docids(self, Index, db):
        docids = self.get_DocID(Index)
        for docid in docids:
            db.insert_docid(docid)      # docid存入数据库

    def get_docid(self, db):
        if db.cur.execute('SELECT docid FROM info WHERE status = 0'):   # 未访问id
            docid = db.cur.fetchone()[0]
        elif db.cur.execute('SELECT docid FROM info WHERE status = -1'):    # 异常id
            docid = db.cur.fetchone()[0]
        if docid:
            db.change_status(docid, 2)      # 更改状态为正在访问
            return docid
        return None
