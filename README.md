# flask_worker

## description

a python_flask worker demo for llmation

## structure

flask_worker/

├── worker.py          # 初始化 Flask 应用，注册蓝图

├── config.py          # 配置文件，存放应用配置 (API 密钥，模型名称.etc)

├── blueprints/        # 存放Blueprints ，按功能模块划分

│   └── chat_bp.py     # chat 功能相关的蓝图 (处理 /chat 路由)

├── services/          # 存放业务逻辑服务，与具体 Flask 框架解耦

│   └── llm_service.py # 大模型交互服务 (封装大模型 API 调用)

├── utils/             # 存放通用工具函数或模块

│   └── api_client.py  # 封装通用的 API 客户端

│   └── logger.py      # 日志记录

├── tests/             # 存放测试文件

│   ├── test_chat_bp.py # chat 蓝图的测试

│   └── test_llm_service.py # llm 服务的测试

├── requirements.txt   # 项目依赖

├── .env               # 环境变量文件

└── README.md          # 项目说明文档
