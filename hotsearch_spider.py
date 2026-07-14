import requests
from lxml import etree
from db_helper import MySqlHelper

# 数据库连接
db = MySqlHelper(
    host="localhost",
    user="root",
    password="leo20200303",
    database="student_db"
)

def crawl_baidu_hot_html():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    url = "https://top.baidu.com/board?tab=realtime"
    # 关闭SSL校验，解决Mac下SSL报错
    resp = requests.get(url, headers=headers, verify=False, timeout=10)
    resp.encoding = "utf-8"
    html = etree.HTML(resp.text)
    hot_list = []
    # 匹配热搜条目通用xpath
    items = html.xpath('//div[contains(@class,"HotItem")]')
    for item in items[:10]:
        # 排名
        rank_text = item.xpath('.//span[contains(@class,"index")]/text()')
        rank = int(rank_text[0]) if rank_text else 0
        # 标题
        title_text = item.xpath('.//div[contains(@class,"title_")]/text()')
        title = title_text[0].strip() if title_text else "无标题"
        # 热度
        hot_text = item.xpath('.//span[contains(@class,"hotScore")]/text()')
        hot_val = int(hot_text[0]) if hot_text else 0
        hot_list.append((rank, title, hot_val))
    return hot_list

def save_to_mysql(data_list):
    insert_sql = "INSERT INTO baidu_hotsearch(hot_rank, title, hot_value) VALUES (%s, %s, %s)"
    for data in data_list:
        db.execute(insert_sql, data)
    print(f"成功插入 {len(data_list)} 条实时热搜数据")

if __name__ == '__main__':
    # 爬虫爬取网页数据
    hot_data = crawl_baidu_hot_html()
    # 存入数据库
    save_to_mysql(hot_data)
    # 查询验证
    res = db.query_all("SELECT * FROM baidu_hotsearch ORDER BY hot_rank")
    print("入库热搜列表：")
    for row in res:
        print(row)