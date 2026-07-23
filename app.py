from flask import Flask, request, redirect, render_template_string
import time
import json
import os

app = Flask(__name__)
DATA_FILE = "memos.json"

def load_memos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memos(memos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    memos = load_memos()

    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if content:
            memos.append({
                "content": content,
                "time": time.strftime("%Y-%m-%d %H:%M")
            })
            save_memos(memos)
        return redirect("/")

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>一句话备忘录</title>
        <style>
            body {
                background: url('/static/notebook-bg.jpg') no-repeat center center fixed !important;
                background-size: cover !important;
                font-family: "Microsoft YaHei", sans-serif;
                margin: 0;
                padding: 40px 0;
            }
            .box {
                width: 600px;
                margin: auto;
                background: rgba(255,255,255,0.92);
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.15);
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
            }
            input[type="text"] {
                width: 75%;
                padding: 10px;
                font-size: 16px;
            }
            button {
                padding: 10px 18px;
                font-size: 15px;
                cursor: pointer;
            }
            .memo {
                margin-top: 15px;
                padding: 12px;
                border-radius: 8px;
                background: #fafafa;
                position: relative;
            }
            .del-btn {
                position: absolute;
                right: 10px;
                top: 10px;
                background: #e74c3c;
                color: #fff;
                border: none;
                padding: 5px 10px;
                border-radius: 6px;
                cursor: pointer;
            }
            small {
                color: #888;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>一句话备忘录</h1>
            <form method="POST">
                <input name="content" placeholder="写点什么..." required>
                <button type="submit">保存</button>
            </form>

            {% for memo in memos %}
            <div class="memo">
                {{ memo.content }}
                <br>
                <small>{{ memo.time }}</small>
                <form method="POST" action="/delete/{{ loop.index0 }}" style="display:inline;">
                    <button class="del-btn" type="submit">删除</button>
                </form>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """, memos=memos)

#test
@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    memos = load_memos()
    if 0 <= index < len(memos):
        memos.pop(index)
        save_memos(memos)
    return redirect("/")

@app.route('/api/memos', methods=['GET'])
def api_get_memos():
    return json.dumps(load_memos(), ensure_ascii=False)

@app.route('/api/memo', methods=['POST'])
def api_add_memo():
    data = request.get_json()
    if not data or not data.get('content', '').strip():
        return json.dumps({'error': '内容不能为空'}), 400
    memos = load_memos()
    new_id = max([m.get('id', 0) for m in memos], default=0) + 1
    memos.append({'id': new_id, 'content': data['content'].strip()})
    save_memos(memos)
    return json.dumps({'success': True, 'id': new_id}), 200

@app.route('/api/memo/<int:memo_id>', methods=['DELETE'])
def api_delete_memo(memo_id):
    memos = load_memos()
    for i, m in enumerate(memos):
        if m.get('id') == memo_id:
            memos.pop(i)
            save_memos(memos)
            return json.dumps({'success': True}), 200
    return json.dumps({'error': '备忘录不存在'}), 404

if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=False)
