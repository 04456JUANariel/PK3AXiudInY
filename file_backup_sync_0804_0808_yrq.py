# 代码生成时间: 2025-08-04 08:08:03
# file_backup_sync.py
# 使用 FALCON 框架创建的文件备份和同步工具

import os
import shutil
from datetime import datetime
import falcon

# 配置常量
BACKUP_DIR = 'backup'
SYNC_DIR = 'sync'
LOG_FILE = 'log.txt'

class FileBackupSync:
    """文件备份和同步处理类"""

    def __init__(self):
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        if not os.path.exists(SYNC_DIR):
            os.makedirs(SYNC_DIR)

    def backup_files(self, source_dir):
        """备份文件到指定目录"""
        try:
            # 确保源目录存在
            if not os.path.exists(source_dir):
                raise FileNotFoundError(f"源目录 {source_dir} 不存在")
            # 创建备份目录
            backup_path = os.path.join(BACKUP_DIR, datetime.now().strftime('%Y%m%d%H%M%S'))
            os.makedirs(backup_path)
            # 复制文件
            for item in os.listdir(source_dir):
                s = os.path.join(source_dir, item)
                d = os.path.join(backup_path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            return True
        except Exception as e:
            with open(LOG_FILE, 'a') as log:
                log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 备份错误：{e}
")
            return False

    def sync_files(self, source_dir, target_dir):
        """同步文件到指定目录"""
        try:
            # 确保源目录和目标目录存在
            if not os.path.exists(source_dir):
                raise FileNotFoundError(f"源目录 {source_dir} 不存在")
            if not os.path.exists(target_dir):
                raise FileNotFoundError(f"目标目录 {target_dir} 不存在")
            # 同步文件
            for item in os.listdir(source_dir):
                s = os.path.join(source_dir, item)
                d = os.path.join(target_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            return True
        except Exception as e:
            with open(LOG_FILE, 'a') as log:
                log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 同步错误：{e}
")
            return False

class FileBackupSyncAPI:
    """API 处理类"""
    def on_get(self, req, resp):
        """GET 请求处理函数"""
        try:
            backup_sync = FileBackupSync()
            source_dir = req.params.get('source')
            action = req.params.get('action', 'backup')

            if action == 'backup':
                result = backup_sync.backup_files(source_dir)
            elif action == 'sync':
                target_dir = req.params.get('target')
                result = backup_sync.sync_files(source_dir, target_dir)
            else:
                resp.status = falcon.HTTP_400
                return

            if result:
                resp.media = {'message': '操作成功'}
            else:
                resp.media = {'message': '操作失败'}
        except Exception as e:
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_500

# 初始化 FALCON API
api = falcon.API()
api.add_route('/file-backup-sync', FileBackupSyncAPI())

if __name__ == '__main__':
    # 运行 API 服务
    import falcon
    from wsgiref import simple_server

    httpd = simple_server.make_server('localhost', 8000, api)
    print('Serving on port 8000...')
    httpd.serve_forever()