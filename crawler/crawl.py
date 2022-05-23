import pymongo
from pymongo import MongoClient
import datetime

cluster = MongoClient("mongodb://root:example@localhost/")
print(f'cluster : {cluster}')

db = cluster["patent_project"]
collection = db["crawling_keywords"]

def get_oldest_keyword():
    global collection

    # 한번도 크롤링한 적 없는 키워드를 crawling한다.
    results = collection.find({"last_crawling": None}).limit(1)
    result_list = list(results)

    # 모두 크롤링한 적이 있다면 가장 예전에 크롤링한 키워드를 조회
    if len(result_list) == 0:
        oneMongthAgo = datetime.datetime.now() - datetime.timedelta(days=30)
        results = collection.find({
            "last_crawling.crawling_date": {"$lt": oneMongthAgo}
            }).sort("last_crawling.crawling_date", 1).limit(1)

        result_list = list(results)

    if len(result_list) == 0:
        return None
    else:
        return result_list[0]

# Crawling할 키워드를 가져온다.
to_crawl = get_oldest_keyword()

print(to_crawl)