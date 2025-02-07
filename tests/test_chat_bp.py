import json
import pytest
from flask import Flask
from blueprints.chat_bp import chat_bp

# Dummy LLM service function to simulate process_conversation behavior.
def dummy_process_conversation(model_name, top_p, conversation_data, temperature, framework):
  return "dummy response"

# Set the transformers_models attribute on the dummy process_conversation function.
dummy_process_conversation.transformers_models = {"dummy_model"}

@pytest.fixture
def app(monkeypatch):
  app = Flask(__name__)
  # Configure testing values.
  app.config['WORKER_TOKEN'] = "valid_token"
  app.config['MODELS_CONFIG'] = {
    "dummy_model": {"temperature": 0.7, "default_top_p": 0.95},
    "openai_model": {"temperature": 0.5, "default_top_p": 0.9}
  }
  # Monkeypatch the llm service function within the blueprint.
  monkeypatch.setattr("flask_worker.blueprints.chat_bp.process_conversation", dummy_process_conversation)
  app.register_blueprint(chat_bp)
  return app

@pytest.fixture
def client(app):
  return app.test_client()

def test_get_models(client):
  response = client.get("/api/chat/models")
  data = response.get_json()
  expected_models = list(client.application.config['MODELS_CONFIG'].keys())
  assert response.status_code == 200
  assert "supported_models" in data
  assert set(data["supported_models"]) == set(expected_models)

def test_generate_chat_success_openai(client):
  headers = {
    "Authorization": "Bearer valid_token",
    "Content-Type": "application/json"
  }
  payload = {
    "model": {
      "name": "openai_model",
      "framework": "openai",
      "configuration": {}
    },
    "conversation": ["Hello"]
  }
  response = client.post("/api/chat/generate", data=json.dumps(payload), headers=headers)
  data = response.get_json()
  assert response.status_code == 200
  assert "response" in data
  assert data["response"] == "dummy response"

def test_generate_chat_success_transformers(client):
  headers = {
    "Authorization": "Bearer valid_token",
    "Content-Type": "application/json"
  }
  payload = {
    "model": {
      "name": "dummy_model",
      "framework": "transformers",
      "configuration": {"temperature": 0.8, "top_p": 0.99}
    },
    "conversation": ["Hi there"]
  }
  response = client.post("/api/chat/generate", data=json.dumps(payload), headers=headers)
  data = response.get_json()
  assert response.status_code == 200
  assert "response" in data
  assert data["response"] == "dummy response"

def test_generate_chat_missing_authorization(client):
  headers = {
    "Content-Type": "application/json"
  }
  payload = {
    "model": {
      "name": "openai_model",
      "framework": "openai",
      "configuration": {}
    },
    "conversation": ["Hello"]
  }
  response = client.post("/api/chat/generate", data=json.dumps(payload), headers=headers)
  data = response.get_json()
  assert response.status_code == 401
  assert "error" in data

def test_generate_chat_invalid_token(client):
  headers = {
    "Authorization": "Bearer invalid_token",
    "Content-Type": "application/json"
  }
  payload = {
    "model": {
      "name": "openai_model",
      "framework": "openai",
      "configuration": {}
    },
    "conversation": ["Hello"]
  }
  response = client.post("/api/chat/generate", data=json.dumps(payload), headers=headers)
  data = response.get_json()
  assert response.status_code == 401
  assert "error" in data

def test_generate_chat_invalid_content_type(client):
  headers = {
    "Authorization": "Bearer valid_token",
    "Content-Type": "text/plain"
  }
  payload = {
    "model": {
      "name": "openai_model",
      "framework": "openai",
      "configuration": {}
    },
    "conversation": ["Hello"]
  }
  response = client.post("/api/chat/generate", data=json.dumps(payload), headers=headers)
  data = response.get_json()
  assert response.status_code == 415
  assert "error" in data

def test_generate_chat_invalid_json(client):
  headers = {
    "Authorization": "Bearer valid_token",
    "Content-Type": "application/json"
  }
  invalid_json = "{invalid_json}"  # intentionally malformed JSON
  response = client.post("/api/chat/generate", data=invalid_json, headers=headers)
  data = response.get_json()
  assert response.status_code == 400
  assert "error" in data

def test_generate_chat_missing_fields(client):
  headers = {
    "Authorization": "Bearer valid_token",
    "Content-Type": "application/json"
  }
  # Missing the 'conversation' field.
  payload = {
    "model": {
      "name": "openai_model",
      "framework": "openai",
      "configuration": {}
    }
  }
  response = client.post("/api/chat/generate", data=json.dumps(payload), headers=headers)
  data = response.get_json()
  assert response.status_code == 400
  assert "error" in data

def test_generate_chat_unsupported_framework(client):
  headers = {
    "Authorization": "Bearer valid_token",
    "Content-Type": "application/json"
  }
  payload = {
    "model": {
      "name": "openai_model",
      "framework": "unsupported",
      "configuration": {}
    },
    "conversation": ["Hello"]
  }
  response = client.post("/api/chat/generate", data=json.dumps(payload), headers=headers)
  data = response.get_json()
  assert response.status_code == 400
  assert "error" in data
