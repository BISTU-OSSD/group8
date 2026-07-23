import sys
import os

# 把项目根目录加入路径，方便导入 app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import json
from app import app

class TestMemoApp(unittest.TestCase):
    """测试类，每个 test_ 开头的方法都会自动执行"""

    def setUp(self):
        """每个测试方法执行前都会调用，准备测试环境"""
        self.client = app.test_client()  # 创建模拟客户端
        app.config['TESTING'] = True     # 开启测试模式

    # ========== 测试1：首页是否能正常打开 ==========
    def test_index_page(self):
        """测试首页是否能正常访问"""
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)  # 200 = 成功

    # ========== 测试2：获取备忘录列表 ==========
    def test_get_memos(self):
        """测试 GET /api/memos 接口"""
        resp = self.client.get('/api/memos')
        self.assertEqual(resp.status_code, 200)
        # 返回的数据应该是列表格式（即使为空也是 []）
        self.assertIsInstance(resp.json, list)

    # ========== 测试3：添加备忘录 ==========
    def test_add_memo(self):
        """测试 POST /api/memo 接口"""
        resp = self.client.post('/api/memo',
            json={'content': '测试内容 - 单元测试专用'})
        self.assertEqual(resp.status_code, 200)
        # 检查返回结果中是否包含 success 字段且为 True
        self.assertTrue(resp.json.get('success', False))

    # ========== 测试4：删除备忘录 ==========
    def test_delete_memo(self):
        """测试 DELETE /api/memo/<id> 接口"""
        # 先添加一条备忘录（获得id）
        add_resp = self.client.post('/api/memo',
            json={'content': '待删除的测试数据'})
        self.assertEqual(add_resp.status_code, 200)

        # 获取所有备忘录，找到刚刚添加的那条的id
        get_resp = self.client.get('/api/memos')
        memos = get_resp.json
        # 找到最新添加的那条（列表第一条，因为按id倒序）
        if memos:
            test_id = memos[0]['id']
            # 执行删除
            del_resp = self.client.delete(f'/api/memo/{test_id}')
            self.assertEqual(del_resp.status_code, 200)
            self.assertTrue(del_resp.json.get('success', False))

    # ========== 测试5：空内容不能添加 ==========
    def test_add_empty_memo(self):
        """测试空内容应该被拒绝"""
        resp = self.client.post('/api/memo',
            json={'content': ''})
        self.assertEqual(resp.status_code, 400)  # 400 = 请求错误
        self.assertIn('error', resp.json)

if __name__ == '__main__':
    unittest.main()
