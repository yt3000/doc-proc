import requests
import json
from typing import Optional, Dict
from app.core.config import settings


class LLMClient:
    """统一大模型客户端 - 支持多 provider"""
    
    def __init__(self, provider: str, api_key: str, model_name: str, 
                 base_url: Optional[str] = None, temperature: float = 0.7,
                 max_tokens: int = 4096):
        self.provider = provider
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url or self._get_default_base_url(provider)
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def _get_default_base_url(self, provider: str) -> str:
        """获取默认 Base URL"""
        defaults = {
            "ollama": "http://localhost:11434",
            "openai": "https://api.openai.com/v1",
            "anthropic": "https://api.anthropic.com/v1"
        }
        return defaults.get(provider, "")
    
    def chat(self, messages: list, system_prompt: Optional[str] = None) -> str:
        """
        调用大模型进行对话
        
        Args:
            messages: 消息列表
            system_prompt: 系统提示
            
        Returns:
            模型回复
        """
        if self.provider == "ollama":
            return self._call_ollama(messages, system_prompt)
        elif self.provider == "openai":
            return self._call_openai(messages, system_prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(messages, system_prompt)
        else:
            raise ValueError(f"不支持的模型提供商：{self.provider}")
    
    def _call_ollama(self, messages: list, system_prompt: Optional[str] = None) -> str:
        """调用 Ollama API"""
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=settings.API_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()
            return result.get("message", {}).get("content", "")
        except requests.exceptions.Timeout:
            raise Exception("Ollama API 调用超时")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API 调用失败：{str(e)}")
    
    def _call_openai(self, messages: list, system_prompt: Optional[str] = None) -> str:
        """调用 OpenAI API"""
        url = f"{self.base_url}/chat/completions"
        
        all_messages = []
        if system_prompt:
            all_messages.append({"role": "system", "content": system_prompt})
        all_messages.extend(messages)
        
        payload = {
            "model": self.model_name,
            "messages": all_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=settings.API_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            raise Exception("OpenAI API 调用超时")
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API 调用失败：{str(e)}")
    
    def _call_anthropic(self, messages: list, system_prompt: Optional[str] = None) -> str:
        """调用 Anthropic API"""
        url = f"{self.base_url}/messages"
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "system": system_prompt or "",
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=settings.API_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]
        except requests.exceptions.Timeout:
            raise Exception("Anthropic API 调用超时")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Anthropic API 调用失败：{str(e)}")
