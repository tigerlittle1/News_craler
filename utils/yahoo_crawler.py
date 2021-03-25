from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request
import time
import datetime
try:
    from utils.crawker import Crawker, Crawker_Thread
except:
    from crawker import Crawker, Crawker_Thread

def format_date(date):
    now = datetime.datetime.now()
    delet_time = None
    if "天" in date:
        if "前天" in date:
            delet_time = datetime.timedelta(days = 2)
        elif "昨天" in date:
            delet_time = datetime.timedelta(days = 1)
        else:
            delet_time = datetime.timedelta(days=int(date.split(" ")[0]))
    elif "時" in date:
        delet_time = datetime.timedelta(hours=int(date.split(" ")[0]))
    elif "分" in date:
        delet_time = datetime.timedelta(minutes=int(date.split(" ")[0]))
    else:
        delet_time = datetime.timedelta(seconds=int(date.split(" ")[0]))


    return (now - delet_time).strftime("%Y-%m-%d %H:%M:%S")

def get_yahoo_news_infon_by_URL(URL = ""):
    topic = list(URL.keys())[0]
    cramker = Crawker(URL[topic])
    time.sleep(1)
    results = []
    news_count = -1
    news = None
    count = 0
    while True:
        cramker.driver.execute_script("var q=document.documentElement.scrollTop=100000")
        soup = cramker.get_soup()

        news = soup.find_all('li', {'class':"StreamMegaItem"})

        if news_count != len(news):
            news_count = len(news)
            count += 1
        else:
            count += 1
            cramker.driver.execute_script("var q=document.documentElement.scrollTop=100000")

        if count > 20:
            break
        time.sleep(1)


    for iteam in news:

        try:
            title_soup = iteam.find('h3',{'class': "Mb(5px)"})
            title=title_soup.a.text
        except:
            title="None"
        try:
            href="https://tw.news.yahoo.com/"+title_soup.a["href"]
        except:
            href="None"
        try:
            infon=iteam.find('p').text
        except:
            infon="None"
        try:
            source_time = iteam.find('div',{'class':"C(#959595) Fz(13px) C($c-fuji-grey-f) Fw(n)! Mend(14px)! D(ib) Mb(6px)"})
            source= source_time.text.split(" • ")[0]
        except:
            source="None"
        try:
            #print(source_time.text.split(" • ")[1])
            times=format_date(source_time.text.split(" • ")[1])
        except:
            times="2000-01-01 01:01:01"

        try:
            come_from="yahoo news"
        except:
            come_from="yahoo news"

        results.append({"title" : title,
                        "href":href,
                        "infon":infon,
                        "source":source,
                        "times":times,
                        "topic":topic,
                        "come_from":come_from})

    cramker.driver.close()
    print(topic,len(results))
    return results

def get_yahoo_news_infon_by_URL_list(URLs = [],para = True):
    #print(URLs)
    threading_s = []
    results = []
    if para:
        for i,URL in enumerate(URLs):
            threading_s.append(Crawker_Thread(target=get_yahoo_news_infon_by_URL,
                                              args=(URL)))
            threading_s[i].start()

        for i in range(len(URLs)):
            results += threading_s[i].get_result()
    else:
        for i in range(len(URLs)):
            results += get_yahoo_news_infon_by_URL(URLs[i])
    return results

def get_yahoo_URL_from_topic():
    # URL = []
    # cramker = Crawker("https://tw.news.yahoo.com")
    # soup = cramker.get_soup()
    # iteams = soup.find_all('li',{'class':"_yb_vcd2n _yb_qedzn"})
    # for iteam in iteams:
    #     URL.append({iteam.a.text:iteam.a["href"]})

    URL = [{"政治":"https://tw.news.yahoo.com/politics/archive"},
           {"財經":"https://tw.news.yahoo.com/finance/archive"},
           {"娛樂":"https://tw.news.yahoo.com/entertainment/archive"},
           {"運動":"https://tw.news.yahoo.com/sports/archive"},
           {"社會地方":"https://tw.news.yahoo.com/society/archive"},
           {"國際":"https://tw.news.yahoo.com/world/archive"},
           {"生活":"https://tw.news.yahoo.com/lifestyle/archive"},
           {"健康":"https://tw.news.yahoo.com/health/archive"},
           {"科技":"https://tw.news.yahoo.com/technology/archive"}]
    return URL

def get_yahoo_URL_from_keyword(keywords=[]):
    #https: // news.google.com / search?q=
    URL = []
    if type(keywords) != str:
        for keyword in keywords:
            URL.append({keyword:"https://tw.news.yahoo.com/search?p=" + urllib.request.quote(keyword.encode("utf-8"))})
        return URL
    else:
        return {keyword:"https://tw.news.yahoo.com/search?p=" + urllib.request.quote(keyword.encode("utf-8"))}


if __name__ == '__main__':
    URL = get_URL_from_keyword(["川普", "中國", "台北市立動物園", "捷運", "明星", "AI", "人工智慧"])
    URL += get_URL_from_topic()
    result = get_yahoo_news_infon_by_URL_list(URL)
    #print(get_yahoo_news_infon_by_URL({1:"https://tw.news.yahoo.com/politics/archive"}))