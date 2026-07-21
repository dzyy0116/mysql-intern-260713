from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# 数据库连接工具函数
def get_db_conn():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="leo20200303",
        database="student_db",
        charset="utf8"
    )
    return conn

# ========== 第四周原有测试接口 ==========
@app.route("/api/get_demo", methods=["GET"])
def get_demo():
    input_text = request.args.get("text", "")
    return jsonify({"msg": f"参数是{input_text}"})

@app.route("/api/post_demo", methods=["POST"])
def post_demo():
    param_text = request.args.get("param_text", "")
    body_json = request.get_json()
    body_text = body_json.get("body_text", "") if body_json else ""
    return jsonify({
        "msg": f"body中的参数是{body_text}，param中的参数是{param_text}"
    })

# ========== 第五周 数据库可视化接口 ==========
# 1. 按上映年份统计电影数量（柱状图）
@app.route("/api/chart/year_count", methods=["GET"])
def chart_year():
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    SELECT release_year, COUNT(*) as count 
    FROM douban_movie_top100 
    WHERE release_year != 0 
    GROUP BY release_year 
    ORDER BY release_year
    """
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    data = [{"year":row[0], "count":row[1]} for row in res]
    return jsonify({"code":200, "data":data})

# 2. 按制片地区统计电影数量（柱状图）
@app.route("/api/chart/region_count", methods=["GET"])
def chart_region():
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    SELECT region, COUNT(*) as count 
    FROM douban_movie_top100 
    WHERE region != '' 
    GROUP BY region
    """
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    data = [{"name":row[0], "value":row[1]} for row in res]
    return jsonify({"code":200, "data":data})

# 3. 按影片类型统计（饼图）
@app.route("/api/chart/type_count", methods=["GET"])
def chart_type():
    conn = get_db_conn()
    cur = conn.cursor()
    sql = "SELECT movie_type FROM douban_movie_top100 WHERE movie_type != ''"
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    type_dict = {}
    for r in rows:
        type_list = r[0].split(" ")
        for t in type_list:
            type_dict[t] = type_dict.get(t, 0) + 1
    data = [{"name":k, "value":v} for k,v in type_dict.items()]
    return jsonify({"code":200, "data":data})

# 4. 评分&评价人数散点图
@app.route("/api/chart/score_vote", methods=["GET"])
def chart_score_vote():
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    SELECT score, vote_count, movie_name 
    FROM douban_movie_top100
    """
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    data = [{"score":float(row[0]), "vote":row[1], "name":row[2]} for row in res]
    return jsonify({"code":200, "data":data})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)