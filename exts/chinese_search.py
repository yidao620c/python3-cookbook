# -*- coding: utf-8 -*- 

def setup(app): 
    import sphinx.search as search
    import zh
    search.languages["zh_CN"] = zh.SearchChinese