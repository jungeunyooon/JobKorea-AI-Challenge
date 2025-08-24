"""
LLM 클라이언트 기본 인터페이스
"""

from abc import ABC, abstractmethod
from typing import AsyncIterable

class LLMClient(ABC):
    """LLM 클라이언트 기본 클래스"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """클라이언트 이름"""
        pass
    
    @abstractmethod
    def invoke(self, prompt, **kwargs) -> str:
        """동기 LLM 호출"""
        pass

    @abstractmethod
    async def ainvoke(self, prompt: str, **kwargs) -> str:
        """비동기 LLM 호출"""
        pass
    
    @abstractmethod
    async def astream(self, prompt: str, **kwargs) -> AsyncIterable[str]:
        """비동기 스트리밍 LLM 호출"""
        pass
    
    @abstractmethod
    def with_options(self, **opts) -> "LLMClient":
        """옵션을 변경한 새로운 클라이언트 인스턴스 반환"""
        pass