'''
Author: HongyeLuo hongye_luo@smbu.edu.cn
Date: 2025-02-07 14:45:50
LastEditors: HongyeLuo hongye_luo@smbu.edu.cn
LastEditTime: 2025-02-07 21:02:12
Description: LLM 服务模块, 用于处理对话生成请求
Copyright (c) 2025 by AustinLo, All Rights Reserved.
'''
from openai import OpenAI
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import current_app # 导入 current_app 以访问 Flask 应用上下文

# 初始化 transformers 模型加载字典 (模块级别的变量)
LOADED_MODELS = {}

def load_transformers_model(model_name):
    """加载 Transformers 模型"""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        return tokenizer, model
    except Exception as e:
        current_app.logger.error(f"Error loading model {model_name}: {e}") # 使用 Flask logger
        return None, None

def initialize_transformers_models():
    """初始化加载所有支持的 Transformers 模型"""
    supported_models = current_app.config['SUPPORTED_TRANSFORMERS_MODELS'] # 从配置中获取模型列表
    for model_name in supported_models:
        if model_name not in LOADED_MODELS:
            tokenizer, model = load_transformers_model(model_name)
            if tokenizer and model:
                LOADED_MODELS[model_name] = (tokenizer, model)
                current_app.logger.info(f"Successfully loaded model: {model_name}")
            else:
                current_app.logger.error(f"Failed to load model: {model_name}")

# 在模块初始化时加载 Transformers 模型 (在服务模块被导入时执行)
initialize_transformers_models()

def process_conversation(model_name, top_p, conversation_data, temperature, framework):
    """
    处理对话，根据框架调用不同的模型 API。
    """
    try:
        # Transformers (Llama)
        if framework == 'transformers' and model_name in LOADED_MODELS:
            tokenizer, model = LOADED_MODELS[model_name]
            if not tokenizer or not model:
                raise Exception(f"Failed to retrieve loaded Llama model '{model_name}'") # 抛出异常，让上层处理

            # 拼接输入文本
            input_text = " ".join([msg["content"] for msg in conversation_data])

            # 生成模型输出
            inputs = tokenizer(input_text, return_tensors="pt")
            outputs = model.generate(
                inputs["input_ids"], max_length=150, temperature=temperature, top_p=top_p
            )
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
            # todo 流式输出

        # OpenAI
        elif framework == 'openai':
            openai_client = OpenAI(api_key=current_app.config['OPENAI_API_KEY']) # 从 Flask 配置获取 API 密钥
            response = openai_client.chat.completions.create(
                model=model_name,
                messages=conversation_data,
                top_p=top_p,
                temperature=temperature,
            )
            model="model_name",
            # stream=True, 流式输出(等待本地实现后可直接加入)
            return response.choices[0].message.content

        else:
            raise ValueError(f"Unsupported framework: '{framework}'") # 抛出异常

    except Exception as e:
        current_app.logger.error(f"模型调用过程中发生错误 (Model call error): {str(e)}") # 记录更详细的错误日志
        raise # 重新抛出异常，让 blueprint 层处理

# 将已加载的 transformers 模型列表作为函数属性暴露出去，供 blueprint 使用
process_conversation.transformers_models = list(LOADED_MODELS.keys())