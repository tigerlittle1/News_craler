資料抓取 Web_crawler.py:
    get_google_URL_from_topic()#抓取google news的分類主題及其對應的URL
    get_google_URL_from_keyword(list) #依照給定list中的關鍵字抓取其對應的URL
    get_google_news_infon_by_URL_list(URL,para) #依照給定的URL抓取新聞內容(para為是否要平行化)
    get_yahoo_URL_from_topic() #抓取google news的分類主題及其對應的URL
    get_yahoo_URL_from_keyword(list) #依照給定list中的關鍵字抓取其對應的URL
    get_yahoo_news_infon_by_URL_list(URL,para) #依照給定的URL抓取新聞內容(para為是否要平行化)

    Web_crawler的所有設定在cfg/crawler.yaml中可以做設定:
        google_Parallel : 是否要爬取google news的topic
        google_get_org_topic : 是否平行化
        google_search_key_word : google news要爬取新聞的關鍵字
        yahoo_Parallel : 是否要爬取yahoo news的topic
        yahoo_get_org_topic : 是否平行化
        yahoo_search_key_word : yahoo news要爬取新聞的關鍵字

    直接執行Web_crawler.py即可進行google 及 yahoo 新聞資料的爬取並且匯入Elasticsearch

Elasticsearch 搜尋 Elasticsearch_search.py
    es.search(query)#給定query即可回傳搜尋結果

    Web_crawler的所有設定在cfg/crawler.yaml中可以做設定:
        query_file : query檔案路徑，內附了10個query檔案於query的資料夾
        size : 搜尋結果回傳數量

    直接執行Elasticsearch_search.py即可進行搜尋


資料夾結構:
-cfg#設定檔
-query#10個query檔案
-utils#其他程序


