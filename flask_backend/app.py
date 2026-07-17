from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 任务2 GET接口：接收URL参数
@app.route("/api/get_demo", methods=["GET"])
def get_demo():
    input_text = request.args.get("text", "")
    return jsonify({"msg": f"参数是{input_text}"})

# 任务3 POST接口：同时接收url param + json body
@app.route("/api/post_demo", methods=["POST"])
def post_demo():
    param_text = request.args.get("param_text", "")
    body_json = request.get_json()
    body_text = body_json.get("body_text", "") if body_json else ""
    return jsonify({
        "msg": f"body中的参数是{body_text}，param中的参数是{param_text}"
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)