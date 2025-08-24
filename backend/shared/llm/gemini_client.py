"""
Google Gemini LLM 클라이언트
"""

from typing import AsyncIterable
from .base import LLMClient
from shared.config.base import BaseAppSettings
from langchain_google_genai import ChatGoogleGenerativeAI

# 기본 설정 인스턴스 (실제로는 각 서비스에서 주입받아야 함)
settings = BaseAppSettings()

class GeminiClient(LLMClient):
    """Google Gemini LLM 클라이언트"""
    
    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int, timeout: int):
        self._name = "gemini"
        self._opts = dict(temperature=temperature, max_tokens=max_tokens)
        self._api_key = api_key
        self._model = model
        self._timeout = timeout
        
        # LangChain Google GenAI 설정
        self._llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            temperature=temperature,
            max_output_tokens=max_tokens,
            timeout=timeout,
            convert_system_message_to_human=True  # SystemMessage를 HumanMessage로 자동 변환
        )
    
    @property
    def name(self) -> str:
        """클라이언트 이름"""
        return self._name
    
    def invoke(self, prompt, **kwargs) -> str:
        """동기 Gemini LLM 호출"""
        try:
            resp = self._llm.invoke(prompt, **kwargs)
            return getattr(resp, "content", str(resp))
        except Exception as e:
            raise Exception(f"Gemini API call failed: {e}")

    async def ainvoke(self, prompt: str, **kwargs) -> str:
        """비동기 Gemini LLM 호출"""
        try:
            resp = await self._llm.ainvoke(prompt, **kwargs)
            return getattr(resp, "content", str(resp))
        except Exception as e:
            raise Exception(f"Gemini API call failed: {e}")
    
    async def astream(self, prompt: str, **kwargs) -> AsyncIterable[str]:
        """비동기 스트리밍 Gemini LLM 호출"""
        try:
            async for chunk in self._llm.astream(prompt, **kwargs):
                if hasattr(chunk, "content"):
                    yield chunk.content
                else:
                    yield str(chunk)
        except Exception as e:
            raise Exception(f"Gemini API streaming failed: {e}")
        
        # 구현 예시:
        # async for chunk in self._llm.astream(prompt, **kwargs):
        #     yield getattr(chunk, "content", str(chunk))
    
    def with_options(self, **opts) -> "GeminiClient":
        """옵션을 변경한 새로운 Gemini 클라이언트 인스턴스 반환"""
        merged = {**self._opts, **opts}
        return GeminiClient(
            api_key=self._api_key,
            model=self._model,
            temperature=merged.get("temperature", self._opts["temperature"]),
            max_tokens=merged.get("max_tokens", self._opts["max_tokens"]),
            timeout=self._timeout
        )

def create_gemini_client() -> GeminiClient:
    """Gemini 클라이언트 팩토리 함수"""
    return GeminiClient(
        api_key=settings.gemini_api_key or "",
        model=settings.gemini_model,
        temperature=settings.gemini_temperature,
        max_tokens=settings.gemini_max_tokens,
        timeout=settings.gemini_timeout
    )
