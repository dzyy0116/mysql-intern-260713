import requests
from lxml import etree
from db_helper import MySqlHelper
import time
import warnings
warnings.filterwarnings("ignore")

# 数据库连接
db = MySqlHelper(
    host="localhost",
    user="root",
    password="leo20200303",
    database="student_db"
)

def crawl_douban_top100():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    movie_list = []
    for page in range(0, 100, 25):
        url = f"https://movie.douban.com/top250?start={page}"
        resp = requests.get(url, headers=headers, verify=False, timeout=10)
        resp.encoding = "utf-8"
        html = etree.HTML(resp.text)
        items = html.xpath('//div[@class="item"]')
        for item in items:
            rank = int(item.xpath('.//em/text()')[0])
            if rank > 100:
                continue
            # 电影名
            name = item.xpath('.//span[@class="title"][1]/text()')[0].strip()
            # 导演演员年份地区类型
            info_raw = item.xpath('.//div[@class="bd"]/p[1]/text()')
            info_line = info_raw[1].strip() if len(info_raw)>=2 else ""
            parts = info_line.split("\xa0/\xa0")
            director, actors, release_year, region, movie_type = "", "", 0, "", ""
            if len(parts)>=1:
                director = parts[0].replace("导演: ","").strip()
            if len(parts)>=2:
                actors = parts[1].strip()
            if len(parts)>=3:
                try:
                    release_year = int(parts[2].strip())
                except:
                    release_year = 0
            if len(parts)>=4:
                region = parts[3].strip()
            if len(parts)>=5:
                movie_type = parts[4].strip()
            # 评分
            score_text = item.xpath('.//span[@class="rating_num"]/text()')
            score = float(score_text[0]) if score_text else 0.0
            # 评价人数（增加空列表判断，解决下标越界）
            vote_text_list = item.xpath('.//div[@class="star"]/span[4]/text()')
            if vote_text_list:
                vote_str = vote_text_list[0]
                vote_count = int(vote_str.replace("人评价",""))
            else:
                vote_count = 0
            # 简介
            intro_list = item.xpath('.//span[@class="inq"]/text()')
            intro = intro_list[0].strip() if intro_list else ""

            movie_list.append((
                rank, name, director, actors, release_year,
                region, movie_type, score, vote_count, intro
            ))
        time.sleep(1)
    return movie_list

def save_to_movie_db(data_list):
    insert_sql = """
    INSERT INTO douban_movie_top100(
        movie_rank, movie_name, director, actors, release_year,
        region, movie_type, score, vote_count, intro
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for data in data_list:
        db.execute(insert_sql, data)
    print(f"成功爬取并入库 {len(data_list)} 部豆瓣TOP100电影")

if __name__ == "__main__":
    movie_data = crawl_douban_top100()
    save_to_movie_db(movie_data)
    # 验证前10条
    res = db.query_all("SELECT movie_rank,movie_name,score FROM douban_movie_top100 ORDER BY movie_rank LIMIT 10;")
    print("已入库电影前10条：")
    for row in res:
        print(row)