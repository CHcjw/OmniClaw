"""模型 Provider 抽象层"""

from __future__ import annotations

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Literal

from openai import OpenAI

from backend.app.core.config import get_settings

Role = Literal["system", "user", "assistant"]


@dataclass
class ProviderMessage:
    role: Role
    content: str
     
@dataclass
class ProviderResult:
    text: str
    raw: object | None = None

class BaseProvider(ABC):
    """Provider 抽象基类"""

    @abstractmethod
    def generate(self, messages: list[ProviderMessage]) -> ProviderResult:
        """根据消息队列生成回复"""
        raise NotImplementedError
    
class OpenAICompatibleProvider(BaseProvider):
    """OpenAI 兼容协议 Provider"""

    def __init__(self, api_key: str, model_name: str, base_url: str | None = None) -> None:
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, messages: list[ProviderMessage]) -> ProviderResult:
        payload = [{"role": m.role, "content": m.content} for m in messages]
        resp = self.client.chat.completions.create(
            model=self.model_name,
            messages=payload,
            temperature=0.2,
        )
        text = (resp.choices[0].message.content or "").strip()
        return ProviderResult(text=text, raw=resp)

def get_provider() -> BaseProvider:
    """Provider 工厂：先实现单通道，后续可扩展多 provider"""
    setting = get_settings()
    provider_name = setting.provider.lower()

    if provider_name in {"aliyun", "openai", "compatible"}:
        if not setting.openai_api_key:
            raise ValueError("缺少 OpenAI API Key（或兼容 API Key）")
        return OpenAICompatibleProvider(
            api_key=setting.openai_api_key,
            model_name=setting.model_name,
            base_url=setting.openai_api_base,
        )

    raise ValueError(f"不支持的 Provider: {setting.provider}")

