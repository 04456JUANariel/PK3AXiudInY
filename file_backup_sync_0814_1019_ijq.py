# 代码生成时间: 2025-08-14 10:19:07
# file_backup_sync.py

# 导入必要的模块
import os
import shutil
import falcon
from datetime import datetime
from falcon import API

class FileBackupSync:
    """文件备份和同步工具"""

    def __init__(self, source_dir, backup_dir):
        """初始化文件备份和同步工具
        
        :param source_dir: 源目录路径
        :param backup_dir: 备份目录路径
        """
        self.source_dir = source_dir
        self.backup_dir = backup_dir

    def backup_files(self):
        """备份文件
        
        将源目录中的文件复制到备份目录中
        """
        for filename in os.listdir(self.source_dir):
            file_path = os.path.join(self.source_dir, filename)
            backup_path = os.path.join(self.backup_dir, filename)
            try:
                if os.path.isfile(file_path):
                    shutil.copy2(file_path, backup_path)
                else:
                    shutil.copytree(file_path, backup_path)
            except Exception as e:
                print(f"Error backing up file {filename}: {str(e)}")

    def sync_files(self):
        """同步文件
        
        将备份目录中的文件同步到源目录中
        """
        for filename in os.listdir(self.backup_dir):
            file_path = os.path.join(self.backup_dir, filename)
            source_path = os.path.join(self.source_dir, filename)
            try:
                if os.path.isfile(file_path):
                    shutil.copy2(file_path, source_path)
                else:
                    shutil.copytree(file_path, source_path)
            except Exception as e:
                print(f"Error syncing file {filename}: {str(e)}")

# 定义FALCON API
class FileBackupSyncAPI:
    def on_get(self, req, resp):
        """GET请求处理"""
        source_dir = req.get_param('source_dir')
        backup_dir = req.get_param('backup_dir')
        if source_dir and backup_dir:
            backup_sync_tool = FileBackupSync(source_dir, backup_dir)
            backup_sync_tool.backup_files()
            backup_sync_tool.sync_files()
            resp.media = {"message": "Files backed up and synced successfully"}
        else:
            resp.media = {"error": "Source and backup directories are required"}
            resp.status = falcon.HTTP_BAD_REQUEST

# 创建FALCON应用
app = API()

# 添加路由
app.add_route('/files', FileBackupSyncAPI())
