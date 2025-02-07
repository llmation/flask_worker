'''
Author: HongyeLuo hongye_luo@smbu.edu.cn
Date: 2025-02-07 14:44:32
LastEditors: HongyeLuo hongye_luo@smbu.edu.cn
LastEditTime: 2025-02-07 20:56:26
FilePath: \\\flask_worker\worker.py
Description: 主应用入口
Copyright (c) 2025 by AustinLo, All Rights Reserved.
'''
from flask import Flask
from blueprints.chat_bp import chat_bp  # 导入chat_bp蓝图
from config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config) # 从配置类加载配置

# 配置日志, 可加入更详细日志
logging.basicConfig(level=logging.INFO) # 设置日志级别为 INFO
app.logger.setLevel(logging.INFO) # 设置 Flask app logger 级别为 INFO

# 注册蓝图
app.register_blueprint(chat_bp)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5001) # 从配置中读取 debug 模式, 监听所有地址，默认端口 5001