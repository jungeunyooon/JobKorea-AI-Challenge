"""
LLM 클라이언트 레지스트리 - 다중 제공자 관리 및 폴백 시스템
"""

from typing import Dict, List, Optional, Type, Union
import logging
from .base import LLMClient
from shared.config.base import BaseAppSettings

# 임시 설정 인스턴스 (각 서비스에서 주입받아 사용)
settings = BaseAppSettings()

logger = logging.getLogger(__name__)

class LLMRegistry:
    """LLM 클라이언트 레지스트리"""
    
    def __init__(self):
        self._clients: Dict[str, Type[LLMClient]] = {}
        self._instances: Dict[str, LLMClient] = {}
        
    def register(self, name: str, client_class: Type[LLMClient]) -> None:
        """LLM 클라이언트 클래스 등록"""
        self._clients[name] = client_class
        logger.info(f"LLM client '{name}' registered")
    
    def create_client(self, name: str) -> Optional[LLMClient]:
        """클라이언트 인스턴스 생성"""
        if name not in self._clients:
            logger.error(f"Unknown LLM client: {name}")
            return None
            
        try:
            client_class = self._clients[name]
            
            if name == "openai":
                from .openai_client import OpenAIClient
                return OpenAIClient(
                    api_key=settings.openai_api_key or "",
                    model=settings.openai_model,
                    temperature=settings.openai_temperature,
                    max_tokens=settings.openai_max_tokens,
                    timeout=settings.openai_timeout
                )
            elif name == "claude":
                from .claude_client import ClaudeClient
                return ClaudeClient(
                    api_key=settings.claude_api_key,
                    model=settings.claude_model,
                    temperature=settings.claude_temperature,
                    max_tokens=settings.claude_max_tokens,
                    timeout=settings.claude_timeout
                )
            elif name == "gemini":
                from .gemini_client import GeminiClient
                return GeminiClient(
                    api_key=settings.gemini_api_key,
                    model=settings.gemini_model,
                    temperature=settings.gemini_temperature,
                    max_tokens=settings.gemini_max_tokens,
                    timeout=settings.gemini_timeout
                )
            else:
                logger.error(f"No factory method for client: {name}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to create LLM client '{name}': {e}")
            return None
    
    def get_client(self, name: str, use_cache: bool = True) -> Optional[LLMClient]:
        """클라이언트 인스턴스 반환 (캐시 사용 가능)"""
        if use_cache and name in self._instances:
            return self._instances[name]
            
        client = self.create_client(name)
        if client and use_cache:
            self._instances[name] = client
            
        return client
    
    def get_available_clients(self) -> List[str]:
        """사용 가능한 클라이언트 목록 반환 (API 키 확인)"""
        available = []
        
        # OpenAI 확인
        if settings.openai_api_key:
            available.append("openai")
            
        # Claude 확인  
        if settings.claude_api_key:
            available.append("claude")
            
        # Gemini 확인
        if settings.gemini_api_key:
            available.append("gemini")
            
        return available
    
    def get_client_with_fallback(self, 
                                preferred_order: Optional[List[str]] = None) -> Optional[LLMClient]:
        """폴백 지원 클라이언트 반환"""
        if not preferred_order:
            preferred_order = ["gemini", "openai", "claude"]
            
        available = self.get_available_clients()
        
        # 선호 순서대로 시도
        for client_name in preferred_order:
            if client_name in available:
                client = self.get_client(client_name)
                if client:
                    logger.info(f"Using LLM client: {client_name}")
                    return client
                    
        logger.warning("No LLM clients available")
        return None
    
    def get_multi_client(self, 
                        primary: str, 
                        fallbacks: Optional[List[str]] = None) -> "MultiLLMClient":
        """기본 + 폴백 클라이언트들을 관리하는 멀티 클라이언트 반환"""
        return MultiLLMClient(self, primary, fallbacks or [])

class MultiLLMClient:
    """다중 LLM 클라이언트 - 자동 폴백 지원"""
    
    def __init__(self, registry: LLMRegistry, primary: str, fallbacks: List[str]):
        self.registry = registry
        self.primary = primary
        self.fallbacks = fallbacks
        self._current_client = None
        
    def _get_current_client(self) -> Optional[LLMClient]:
        """현재 사용할 클라이언트 반환"""
        if self._current_client:
            return self._current_client
            
        # 기본 클라이언트 시도
        client = self.registry.get_client(self.primary)
        if client:
            self._current_client = client
            return client
            
        # 폴백 클라이언트들 시도
        for fallback in self.fallbacks:
            client = self.registry.get_client(fallback)
            if client:
                logger.info(f"Using fallback LLM: {fallback}")
                self._current_client = client
                return client
                
        return None
    
    async def ainvoke(self, prompt: str, **kwargs) -> str:
        """폴백 지원 LLM 호출"""
        # 기본 클라이언트 시도
        try:
            client = self.registry.get_client(self.primary)
            if client:
                return await client.ainvoke(prompt, **kwargs)
        except Exception as e:
            logger.warning(f"Primary LLM ({self.primary}) failed: {e}")
        
        # 폴백 클라이언트들 시도
        for fallback_name in self.fallbacks:
            try:
                client = self.registry.get_client(fallback_name)
                if client:
                    logger.info(f"Trying fallback LLM: {fallback_name}")
                    return await client.ainvoke(prompt, **kwargs)
            except Exception as e:
                logger.warning(f"Fallback LLM ({fallback_name}) failed: {e}")
                
        raise Exception("All LLM clients failed")
    
    async def astream(self, prompt: str, **kwargs):
        """폴백 지원 스트리밍 호출"""
        client = self._get_current_client()
        if not client:
            raise Exception("No LLM client available")
            
        async for chunk in client.astream(prompt, **kwargs):
            yield chunk

# 전역 레지스트리 인스턴스
registry = LLMRegistry()

# 클라이언트 등록
def setup_registry():
    """레지스트리 초기 설정"""
    from .openai_client import OpenAIClient
    from .claude_client import ClaudeClient  
    from .gemini_client import GeminiClient
    
    registry.register("openai", OpenAIClient)
    registry.register("claude", ClaudeClient)
    registry.register("gemini", GeminiClient)
    
    logger.info("LLM Registry setup completed")

# 초기화
setup_registry()
