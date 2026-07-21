from flask import Flask, render_template_string, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "memos.json"

# ===== 重点：HTML 定义在全局，放在所有函数外面 =====
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>一句话备忘录 One-Line Memo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: "Microsoft Yahei", sans-serif;
        }
        body {
            max-width: 700px;
            margin: 40px auto;
            padding: 0 20px;
            background-color: #f5f7fa;
        }
        h1 {
            text-align: center;
            color: #222;
            margin-bottom: 30px;
        }
        .input-box {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        #content {
            flex: 1;
            padding: 12px 16px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 6px;
            outline: none;
        }
        #content:focus {
            border-color: #409eff;
        }
        button {
            padding: 12px 22px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 15px;
        }
        .save-btn {
            background-color: #409eff;
            color: white;
        }
        .memo-item {
            background: white;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        }
        .memo-text {
            flex: 1;
        }
        .memo-time {
            font-size: 12px;
            color: #999;
            margin-top: 6px;
        }
        .del-btn {
            background-color: #f56c6c;
            color: white;
            padding: 6px 12px;
            font-size: 13px;
        }
        .empty-tip {
            text-align: center;
            color: #888;
            margin-top: 50px;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <h1>一句话备忘录</h1>
    <form action="/add" method="POST" class="input-box">
        <input type="text" id="content" name="content" placeholder="输入你要记录的内容..." required>
        <button class="save-btn" type="submit">保存</button>
    </form>
    <div class="memo-list">
        {% if memos %}
            {% for memo in memos %}
                <div class="memo-item">
                    <div class="memo-text">
                        <div>{{ memo.content }}</div>
                        <div class="memo-time">{{ memo.time }}</div>
                    </div>
                    <a href="/delete/{{ memo.id }}">
                        <button class="del-btn">删除</button>
                    </a>
                </div>
            {% endfor %}
        {% else %}
            <div class="empty-tip">暂无备忘录，快记录第一条内容吧</div>
        {% endif %}
    </div>
</body>
</html>
"""

# 下面是你原来的所有函数代码
def init_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def get_all_memos():
    init_data()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        memos = json.load(f)
    memos.sort(key=lambda x: x["time"], reverse=True)
    return memos

def save_memos(memos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    memos = get_all_memos()
    return render_template_string(HTML_TEMPLATE, memos=memos)

@app.route("/add", methods=["POST"])
def add_memo():
    content = request.form.get("content", "").strip()
    if content:
        memos = get_all_memos()
        new_memo = {
            "id": len(memos) + 1,
            "content": content,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        memos.append(new_memo)
        save_memos(memos)
    return redirect(url_for("index"))

@app.route("/delete/<int:memo_id>", methods=["GET"])
def delete_memo(memo_id):
    memos = get_all_memos()
    memos = [item for item in memos if item["id"] != memo_id]
    save_memos(memos)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)