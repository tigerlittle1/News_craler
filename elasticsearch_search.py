from utils.Elasticsearch_uitle import Elast
import argparse
import yaml
from easydict import EasyDict

#topic : "COVID-19"  or title : "COVID-19" or infon : "COVID-19" or infon : "武漢肺炎"

#title : "大學繁星" or title : "繁星" or infon  : "繁星"

#(title : "鮭魚"  or  title : "改名" )and (infon: "改名" or infon : "改名")

#(title : "疫苗" or infon : "疫苗") and (title : "接種" or infon : "接種") and (title : "意願" or infon : "意願")

#(title : "深度學習"  or  infon : "深度學習" ) and not (title : "課程" or infon : "課程")

#title : "股票" or title : "股市" or infon: "股票" or infon : "股市"

#title : "水庫" or  infon : "缺水" or title : "缺水" or  infon : "水庫"

#topic : "健康" and not (title : "COVID-19" or infon: "COVID-19" or title : "武漢肺炎" or infon: "武漢肺炎")

#title : "旅遊泡泡" or infon : "旅遊泡泡"

#title : "氣象" or title : "天氣" or infon : "氣象" or infon : "天氣"



def get_config_from_yaml(yaml_file):
  with open(yaml_file, 'r') as config_file:
    try:
      config_dict = yaml.load(config_file)
      config = EasyDict(config_dict)
      return config
    except ValueError:
      print('INVALID YAML file format.. Please provide a good yaml file')
      exit(-1)

if __name__ == '__main__':
  arg_parser = argparse.ArgumentParser(description='Elasticsearch search')
  arg_parser.add_argument(
    '--config',
    default="./cfg/search.yaml",
    help='The path of configuration file in yaml format')
  args = arg_parser.parse_args()
  config = get_config_from_yaml(args.config)
  print(config)

  es = Elast()
  import json

  with open(config["query_file"], newline='',encoding="utf-8") as jsonfile:
    query = json.load(jsonfile)

  query["size"] = config["size"]
  result = es.search(query)

  for news in result:
    print(news['_source'])
