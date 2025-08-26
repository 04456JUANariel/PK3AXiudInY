# 代码生成时间: 2025-08-26 09:09:54
#!/usr/bin/env python

# 引用必要的库
import falcon
import psutil
from falcon import API

# 系统性能监控资源类
class SystemMonitorResource:
    """
    资源类用于处理性能监控相关的请求
    """
    def on_get(self, req, resp):
        """
        GET请求的处理函数，返回系统性能信息
        """
        # 收集系统性能信息
        system_info = self.get_system_info()
        # 设置响应内容为系统性能信息
        resp.media = system_info

    def get_system_info(self):
        """
        获取当前系统的性能信息
        """
        try:
            # 获取CPU使用率
            cpu_usage = psutil.cpu_percent()
            # 获取内存使用情况
            memory = psutil.virtual_memory()
            # 获取磁盘使用情况
            disk = psutil.disk_usage('/')
            # 组装性能信息
            system_info = {
                'cpu_usage': cpu_usage,
                'memory_total': memory.total,
                'memory_used': memory.used,
                'memory_free': memory.free,
                'disk_total': disk.total,
                'disk_used': disk.used,
                'disk_free': disk.free
            }
            return system_info
        except Exception as e:
            # 错误处理
            raise falcon.HTTPInternalServerError(description=str(e))

# 创建FALCON API实例
api = API()

# 添加系统性能监控资源
api.add_route('/system-info', SystemMonitorResource())

# 如果此脚本被直接运行，则启动服务
if __name__ == '__main__':
    # 启动FALCON API服务
    api.run(port=8000, host='0.0.0.0')