'''
Author: HongyeLuo hongye_luo@smbu.edu.cn
Date: 2025-02-07 14:44:44
LastEditors: HongyeLuo hongye_luo@smbu.edu.cn
LastEditTime: 2025-02-07 20:23:06
FilePath: \flask_worker\config.py
Description: 模型配置文件
Copyright (c) 2025 by AustinLo, All Rights Reserved.
'''
import os
class Config:
    DEBUG = True  # 默认开启 Debug 模式，生产环境改为 False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

    # Worker Token 配置
    WORKER_TOKEN = os.environ.get('WORKER_TOKEN', 'WORKER_TOKEN') # 默认值 'WORKER_TOKEN'

    # 大模型配置
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    # 模型列表配置
    MODELS_CONFIG = {
        "deepseek-coder": {
            "description": "DeepSeek Coder",
            "default_top_p": 0.8,
            "temperature": 0.5,
        },
        "claude-3.5-sonnet": {
            "description": "claude 3.5 Sonnet",
            "default_top_p": 0.9,
            "temperature": 0.5,
        },
        "chinese-llama": {
            "description": "chinese Llama",
            "default_top_p": 0.7,
            "temperature": 0.5,
        },
    }#top_p, temperature 按实际需要更改

    # 支持的 Transformers 模型列表 (可以考虑移动到 services/llm_service.py，如果模型加载逻辑更复杂)
    SUPPORTED_TRANSFORMERS_MODELS = ["meta/llama-2-7b"]