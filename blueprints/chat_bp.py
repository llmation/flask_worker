'''
Author: HongyeLuo hongye_luo@smbu.edu.cn
Date: 2025-02-07 14:45:25
LastEditors: HongyeLuo hongye_luo@smbu.edu.cn
LastEditTime: 2025-02-07 21:01:42
FilePath: \flask_worker\blueprints\chat_bp.py
Description:

Copyright (c) 2025 by AustinLo, All Rights Reserved.
'''
from flask import Blueprint, request, jsonify, current_app
from services.llm_service import process_conversation  # 导入 LLM 服务

chat_bp = Blueprint('chat_bp', __name__)

# Worker Token 验证 (移动到 config 中作为配置项，这里使用配置项)
def verify_token(token):
    valid_token = current_app.config['WORKER_TOKEN']
    return token == valid_token

# 获取支持的模型列表
@chat_bp.route('/api/chat/models', methods=['GET'])
def get_models():
    models = list(current_app.config['MODELS_CONFIG'].keys()) # 从配置中获取模型列表
    return jsonify({"supported_models": models}), 200

# 用于生成 chat 的路由
@chat_bp.route('/api/chat/generate', methods=['POST'])
def generate_chat():
    # Authentication
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header[len('Bearer '):]
    if not verify_token(token):
        return jsonify({"error": "Invalid Worker Token"}), 401

    # 检查 Content-Type
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415

    # 解析 JSON 请求体
    try:
        request_data = request.get_json()
    except Exception as e:
        current_app.logger.error(f"Invalid JSON request body: {e}") # 使用 Flask app logger 记录错误
        return jsonify({"error": "Invalid JSON request body", "details": str(e)}), 400

    # 提取模型和对话数据
    model_data = request_data.get('model')
    conversation_data = request_data.get('conversation')
    framework = model_data.get('framework', 'openai')  # 默认使用 OpenAI

    if not model_data or not conversation_data:
        return jsonify({"error": "Missing 'model' or 'conversation' in request body"}), 400

    model_name = model_data.get('name')
    configuration = model_data.get('configuration')
    top_p = configuration.get('top_p') if configuration else None
    temperature = configuration.get('temperature') if configuration else None

    # 从模型配置中获取默认值
    model_config = current_app.config['MODELS_CONFIG'].get(model_name, {})
    if temperature is None:
        temperature = model_config.get("temperature", 0.5)
    if top_p is None:
        top_p = model_config.get("default_top_p", 0.9)

    # 检查模型是否支持 (框架级别的检查，服务层可能还需要更细致的检查)
    if framework == 'transformers':
        supported_models = process_conversation.transformers_models # 访问服务层函数上的属性
        if model_name not in supported_models: # 使用服务层提供的模型列表
            return jsonify({"error": f"Transformers model '{model_name}' not found or not loaded"}), 400 # 更精确的错误信息
    elif framework == 'openai':
        if model_name not in current_app.config['MODELS_CONFIG']: # 检查 OpenAI 模型是否在配置中
            return jsonify({"error": f"Unsupported OpenAI model name: '{model_name}'"}), 400
    else:
        return jsonify({"error": f"Unsupported framework: '{framework}'"}), 400

    # 模型处理 - 调用服务层函数
    try:
        response_message = process_conversation(
            model_name, top_p, conversation_data, temperature, framework
        )
    except Exception as e: # 捕获服务层抛出的异常
        current_app.logger.error(f"Error during model processing: {e}") # 记录更详细的错误日志
        return jsonify({"error": "Model processing failed", "details": str(e)}), 500


    # 构建 JSON 响应
    response_data = {
        "response": response_message
    }

    # 返回 JSON 响应
    return jsonify(response_data), 200