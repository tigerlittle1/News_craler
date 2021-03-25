from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request
import time
from utils.crawker import Crawker, Crawker_Thread

def format_date(date):
    date = date.sp;it("T")
    return date[0] + " " + date[1][:-1]

def get_google_news_infon_by_URL(URL = ""):
    topic = list(URL.keys())[0]
    cramker = Crawker(URL[topic])
    results = []
    news_count = 0
    news = None
    while True:
        soup = cramker.get_soup()
        news = soup.find_all('article', {'class':"MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne"})
        #print(dad)
        #news = soup.find_all('h3', {'class': 'ipQwMb ekueJc RD0gLb'})

        if news_count != len(news):
            news_count = len(news)
        else:
            break
        time.sleep(0.3)
        cramker.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    for iteam in news:

        try:
            title=iteam.h3.a.text
        except:
            title="None"
        try:
            href="https://news.google.com/"+iteam.h3.a["href"][2:]
        except:
            href="None"
        try:
            infon=iteam.find('div', {'jsname': "jVqMGc"}).span.text
        except:
            infon="None"
        try:
            source_time = iteam.find('div',{'class':"SVJrMe"})
            source=source_time.a.text
        except:
            source="None"
        try:
            times=format_date(source_time.time["datetime"])
        except:
            times="2000-01-01 01:01:01"
        try:
            come_from="google news"
        except:
            come_from="google news"

        results.append({"title" : title,
                        "href":href,
                        "infon":infon,
                        "source":source,
                        "times":times,
                        "topic":topic,
                        "come_from":come_from})

    print(topic, len(results))
    cramker.driver.close()
    return results

def get_google_news_infon_by_URL_list(URLs = [],para = True):
    # print(URLs)
    threading_s = []
    results = []
    if para:
        for i, URL in enumerate(URLs):
            threading_s.append(Crawker_Thread(target=get_google_news_infon_by_URL,
                                              args=(URL)))
            threading_s[i].start()

        for i in range(len(URLs)):
            results += threading_s[i].get_result()
    else:
        for i in range(len(URLs)):
            results += get_google_news_infon_by_URL(URLs[i])
    return results

def get_google_URL_from_topic():
    cramker = Crawker("https://news.google.com/topstories?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant")
    soup = cramker.get_soup()
    URL = []
    i = 0
    for iteam in soup.find_all('a', {'class': 'SFllF'}):
        if "topics" in iteam["href"][2:]:
            #topic.append(iteam["aria-label"])
            # print("https://news.google.com/"+iteam["href"][2:])
            URL.append({iteam["aria-label"]:"https://news.google.com/" + iteam["href"][2:]})
            i += 1
    cramker.driver.close()
    return URL

def get_google_URL_from_keyword(keywords=[]):
    #https: // news.google.com / search?q=
    URL = []
    if type(keywords) != str:
        for keyword in keywords:
            URL.append({keyword:"https://www.news.google.com/search?q=" + urllib.request.quote(keyword.encode("utf-8"))})
        return URL
    else:
        return {keyword:"https://www.news.google.com/search?q=" + urllib.request.quote(keyword.encode("utf-8"))}


if __name__ == '__main__':
    URL_list = get_URL_from_topic()
    URL_list += get_URL_from_keyword(["川普", "中國", "台北市立動物園", "捷運", "明星", "AI", "人工智慧"])
    results = get_google_news_infon_by_URL_list(URL_list)