from langchain_openai import ChatOpenAI
from .base import LLMClient
from shared.config.base import BaseAppSettings
from typing import AsyncIterable

# 기본 설정 인스턴스 (실제로는 각 서비스에서 주입받아야 함)
settings = BaseAppSettings()

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int, timeout: int):
        self._name = "openai"
        self._model = model 
        self._opts = dict(temperature=temperature, max_tokens=max_tokens)
        self._llm = ChatOpenAI(
            api_key=settings.openai_api_key,   # 최신 langchain_openai는 api_key 인자 지원
            model=model,
            timeout=timeout,
            max_retries=3,
            **self._opts
        )

    @property
    def name(self) -> str:
        """클라이언트 이름"""
        return self._name

    @property
    def model(self) -> str:
        """사용 중인 LLM 모델명"""
        return self._model

    def invoke(self, prompt, **kwargs) -> str:
        """동기 OpenAI LLM 호출"""
        resp = self._llm.invoke(prompt, **kwargs)
        return getattr(resp, "content", str(resp))

    async def ainvoke(self, prompt: str, **kwargs) -> str:
        """비동기 OpenAI LLM 호출"""
        resp = await self._llm.ainvoke(prompt, **kwargs)
        return getattr(resp, "content", str(resp))

    async def astream(self, prompt: str, **kwargs) -> AsyncIterable[str]:
        async for chunk in self._llm.astream(prompt, **kwargs):
            yield getattr(chunk, "content", str(chunk))

    def with_options(self, **opts) -> "OpenAIClient":
        merged = {**self._opts, **opts}
        clone = OpenAIClient(
            api_key=self._llm.api_key,  # 내부 보유 값
            model=self._llm.model_name,
            temperature=merged.get("temperature", self._opts["temperature"]),
            max_tokens=merged.get("max_tokens", self._opts["max_tokens"]),
            timeout=self._llm.timeout
        )
        return clone
