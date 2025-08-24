"""
Anthropic Claude LLM 클라이언트
"""

from typing import AsyncIterable
from langchain_anthropic import ChatAnthropic
from .base import LLMClient
from shared.config.base import BaseAppSettings

# 기본 설정 인스턴스 (실제로는 각 서비스에서 주입받아야 함)
settings = BaseAppSettings()

class ClaudeClient(LLMClient):
    """Anthropic Claude LLM 클라이언트"""
    
    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int, timeout: int):
        self._name = "claude"
        self._opts = dict(temperature=temperature, max_tokens=max_tokens)
        self._api_key = api_key
        self._model = model
        self._timeout = timeout
        
        self._llm = ChatAnthropic(
            anthropic_api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            model_kwargs={"timeout": timeout}  # timeout을 model_kwargs로 전달
        )
    
    @property
    def name(self) -> str:
        """클라이언트 이름"""
        return self._name
    
    async def ainvoke(self, prompt: str, **kwargs) -> str:
        """비동기 Claude LLM 호출"""
        try:
            resp = await self._llm.ainvoke(prompt, **kwargs)
            return getattr(resp, "content", str(resp))
        except Exception as e:
            raise Exception(f"Claude API call failed: {e}")
        
        # 구현 예시:
        # resp = await self._llm.ainvoke(prompt, **kwargs)
        # return getattr(resp, "content", str(resp))
    
    async def astream(self, prompt: str, **kwargs) -> AsyncIterable[str]:
        """비동기 스트리밍 Claude LLM 호출"""
        try:
            async for chunk in self._llm.astream(prompt, **kwargs):
                if hasattr(chunk, "content"):
                    yield chunk.content
                else:
                    yield str(chunk)
        except Exception as e:
            raise Exception(f"Claude API streaming failed: {e}")
        
        # 구현 예시:
        # async for chunk in self._llm.astream(prompt, **kwargs):
        #     yield getattr(chunk, "content", str(chunk))
    
    def with_options(self, **opts) -> "ClaudeClient":
        """옵션을 변경한 새로운 Claude 클라이언트 인스턴스 반환"""
        merged = {**self._opts, **opts}
        return ClaudeClient(
            api_key=self._api_key,
            model=self._model,
            temperature=merged.get("temperature", self._opts["temperature"]),
            max_tokens=merged.get("max_tokens", self._opts["max_tokens"]),
            timeout=self._timeout
        )

def create_claude_client() -> ClaudeClient:
    """Claude 클라이언트 팩토리 함수"""
    return ClaudeClient(
        api_key=settings.claude_api_key or "",
        model=settings.claude_model,
        temperature=settings.claude_temperature,
        max_tokens=settings.claude_max_tokens,
        timeout=settings.claude_timeout
    )
