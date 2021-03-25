from utils.google_crawler import get_google_URL_from_topic,get_google_URL_from_keyword,get_google_news_infon_by_URL_list
from utils.yahoo_crawler import get_yahoo_URL_from_topic,get_yahoo_URL_from_keyword,get_yahoo_news_infon_by_URL_list

from utils.Elasticsearch_uitle import Elast
from multiprocessing import Pool
import time

import argparse
import yaml
from easydict import EasyDict

def get_config_from_yaml(yaml_file):
  with open(yaml_file, 'r',encoding="utf-8") as config_file:
    try:
      config_dict = yaml.load(config_file)
      config = EasyDict(config_dict)
      return config
    except ValueError:
      print('INVALID YAML file format.. Please provide a good yaml file')
      exit(-1)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Crawler')
    arg_parser.add_argument(
        '--config',
        default="./cfg/crawler.yaml",
        help='The path of configuration file in yaml format')
    args = arg_parser.parse_args()
    config = get_config_from_yaml(args.config)
    print(config)

    google_URL_list = []
    yahoo_URL_list = []
    results = []

    start = time.time()

    if config["yahoo_get_org_topic"]:
        google_URL_list += get_google_URL_from_topic()
    if config["yahoo_search_key_word"] != None:
        google_URL_list += get_google_URL_from_keyword(config["google_search_key_word"])

    results += get_google_news_infon_by_URL_list(google_URL_list,config["google_Parallel"])

    print("google news 資料抓取時間:",time.time()-start)
    start = time.time()

    if config["yahoo_get_org_topic"]:
        yahoo_URL_list += get_yahoo_URL_from_topic()
    if config["yahoo_search_key_word"] != None:
        yahoo_URL_list += get_yahoo_URL_from_keyword(config["yahoo_search_key_word"])

    results += get_yahoo_news_infon_by_URL_list(yahoo_URL_list,config["yahoo_Parallel"])

    print("yahoo news 資料抓取時間:",time.time()-start)
    print(len(results))

    # E = Elast()
    # E.load_elasticsearch()
    # E.import_data(results)

    # for result in results:
    #     print(result)





