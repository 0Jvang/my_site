# coding:utf-8
import multiprocessing
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
# unix:file_path 使用socket方式
bind = "0.0.0.0:81"
#socket_file = os.path.join(base_dir,'mysocket','mysock.sock')
#bind = "unix:{}".format(socket_file)
# 2-4 x $(NUM_CORES) range
workers = multiprocessing.cpu_count() * 2 + 1
#worker_class= "gevent"
# port = 8002
backlog = 2048  # 就是设置允许挂起的连接数的最大值
# timeout默认值：30
# reload 默认值：False 重载 更改代码的时候重启workers， 只建议在开发过程中开启。
reload = False
# daemon以守护进程形式来运行Gunicorn进程。默认值：False
daemon = False
# accesslog 设置访问日志存放的地方
# 默认值：None
# accesslog = '/opt/logs/modu_movie/access.log'
log_dir = os.path.join(base_dir, '../log', 'gunicorn')
try:
    os.makedirs(log_dir)
    os.makedirs(log_dir)
except Exception:
    pass
accesslog = os.path.join(log_dir, 'access.log')
# errorlog 设置错误日志的存放地址
# errorlog = '/opt/logs/modu_movie/error.log'
errorlog = os.path.join(log_dir, 'error.log')

# 默认是不会给你做css js文件的转发

# 启动方式 gunicorn -c gunicorn_conf.py movie1.wsgi 切忌在项目文件夹下面执行启动命令

# 查看进程 pstree -ap|grep gunicorn; ps -A
# 重启 kill -HUP pid
# 杀死 kill -9 pid
# 查看端口开放情况 lsof -i:80; netstat -aptn
