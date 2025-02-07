# flask_worker

## description

a python_flask worker demo for llmation

## structure

flask_worker/

������ worker.py          # ��ʼ�� Flask Ӧ�ã�ע����ͼ

������ config.py          # �����ļ������Ӧ������ (API ��Կ��ģ������.etc)

������ blueprints/        # ���Blueprints ��������ģ�黮��

��   ������ chat_bp.py     # chat ������ص���ͼ (���� /chat ·��)

������ services/          # ���ҵ���߼���������� Flask ��ܽ���

��   ������ llm_service.py # ��ģ�ͽ������� (��װ��ģ�� API ����)

������ utils/             # ���ͨ�ù��ߺ�����ģ��

��   ������ api_client.py  # ��װͨ�õ� API �ͻ���

��   ������ logger.py      # ��־��¼

������ tests/             # ��Ų����ļ�

��   ������ test_chat_bp.py # chat ��ͼ�Ĳ���

��   ������ test_llm_service.py # llm ����Ĳ���

������ requirements.txt   # ��Ŀ����

������ .env               # ���������ļ�

������ README.md          # ��Ŀ˵���ĵ�
