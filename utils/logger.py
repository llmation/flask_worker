'''
Author: HongyeLuo hongye_luo@smbu.edu.cn
Date: 2025-02-07 14:46:33
LastEditors: HongyeLuo hongye_luo@smbu.edu.cn
LastEditTime: 2025-02-07 23:05:26
Description: 配置 Flask 应用的日志记录
Copyright (c) 2025 by AustinLo, All Rights Reserved.
'''
import logging
import os

def configure_logger(app):
    """
    配置 Flask 应用的日志记录。
    日志将输出到文件 (worker.log) 和控制台。
    """
    log_dir = 'logs' # 日志文件存放目录
    if not os.path.exists(log_dir):
        os.makedirs(log_dir) # 创建日志目录

    log_file = os.path.join(log_dir, 'worker.log') # 日志文件路径

    # 创建日志记录器
    logger = logging.getLogger(__name__) # 使用模块名作为 logger 名称，方便区分
    logger.setLevel(logging.INFO) # 设置默认日志级别 (可以从配置中读取)

    # 创建文件处理器 (File Handler)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO) # 文件处理器日志级别

    # 创建控制台处理器 (Stream Handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING) # 控制台处理器日志级别 (只输出 WARNING 及以上级别的日志)

    # 定义日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # 将配置好的 logger 附加到 Flask app 上下文，方便在 app 的其他地方使用 current_app.logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO) # 确保 Flask app logger 也设置了级别


    return logger # 返回配置好的 logger 对象 (返回自定义的 logger 实例可能更灵活)

if __name__ == '__main__':
    # 用例 (用于测试 logger.py)
    from flask import Flask
    test_app = Flask(__name__)
    logger = configure_logger(test_app)

    logger.info("This is an info message from utils/logger.py test.")
    logger.warning("This is a warning message from utils/logger.py test.")
    logger.error("This is an error message from utils/logger.py test.")