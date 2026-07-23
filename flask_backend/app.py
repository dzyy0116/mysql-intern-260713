from flask import Flask, request, jsonify, session
from flask_cors import CORS
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "intern_2026_secret_key_abc123"
CORS(app, supports_credentials=True)

# 数据库连接
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

# ========== 第五周 可视化图表接口 ==========
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

# ========== 第六周【注册、登录、权限校验接口】 ==========
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"code":400, "msg":"用户名和密码不能为空"})

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM user WHERE username=%s", [username])
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"code":400, "msg":"用户名已被占用"})

    hash_pwd = generate_password_hash(password)
    cur.execute("INSERT INTO user(username, password) VALUES(%s,%s)", [username, hash_pwd])
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"code":200, "msg":"注册成功"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM user WHERE username=%s", [username])
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row or not check_password_hash(row[1], password):
        return jsonify({"code":400, "msg":"用户名或密码错误"})

    session["user_id"] = row[0]
    session["username"] = username
    return jsonify({"code":200, "msg":"登录成功", "username":username})

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"code":200, "msg":"已退出登录"})

@app.route("/api/check_login", methods=["GET"])
def check_login():
    if session.get("user_id"):
        return jsonify({"code":200, "isLogin":True, "username":session["username"]})
    return jsonify({"code":401, "isLogin":False, "msg":"未登录"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)