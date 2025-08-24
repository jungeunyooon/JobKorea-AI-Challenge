"""
프롬프트 로더 유틸리티
YAML 기반 프롬프트 파일을 로드하고 템플릿을 렌더링
"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class PromptLoader:
    """YAML 기반 프롬프트 로더"""
    
    def __init__(self, prompts_dir: str):
        """
        Args:
            prompts_dir: 프롬프트 파일들이 위치한 디렉토리 경로
        """
        self.prompts_dir = Path(prompts_dir)
        self._cache = {}  # 로드된 프롬프트 캐시
    
    def load_prompt_config(self, prompt_file: str) -> Dict[str, Any]:
        """
        YAML 프롬프트 파일 로드
        
        Args:
            prompt_file: 프롬프트 파일명 (예: 'interview_questions.yaml')
            
        Returns:
            Dict: 프롬프트 설정 데이터
        """
        if prompt_file in self._cache:
            logger.error(f"Using cached config for {prompt_file}")
            return self._cache[prompt_file]
            
        file_path = self.prompts_dir / prompt_file
        logger.error(f"Loading prompt file from: {file_path}")
        
        if not file_path.exists():
            logger.error(f"Prompt file does not exist: {file_path}")
            raise FileNotFoundError(f"프롬프트 파일을 찾을 수 없습니다: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            logger.error(f"YAML config loaded: {type(config)}, keys: {list(config.keys()) if config else 'None'}")
            self._cache[prompt_file] = config
            logger.error(f"프롬프트 파일 로드 성공: {prompt_file}")
            return config
            
        except yaml.YAMLError as e:
            logger.error(f"YAML 파싱 오류 ({prompt_file}): {e}")
            raise
        except Exception as e:
            logger.error(f"프롬프트 파일 로드 실패 ({prompt_file}): {e}")
            raise
    
    def render_system_prompt(self, config: Dict[str, Any], context: Dict[str, Any] = None) -> str:
        """
        시스템 프롬프트 렌더링
        
        Args:
            config: 프롬프트 설정
            context: 추가 컨텍스트 변수
            
        Returns:
            str: 렌더링된 시스템 프롬프트
        """
        template = config.get('system_prompt_template', '')
        
        # 간단한 템플릿이므로 그대로 반환
        return template
    
    def render_human_prompt(self, config: Dict[str, Any], resume_data: Dict[str, Any]) -> str:
        """
        휴먼 프롬프트 렌더링
        
        Args:
            config: 프롬프트 설정
            resume_data: 이력서 데이터
            
        Returns:
            str: 렌더링된 휴먼 프롬프트
        """
        template = config.get('human_prompt_template', '')
        logger.error(f"Human prompt template: {template}")
        logger.error(f"Resume data for formatting: {resume_data}")
        logger.error(f"Resume data type: {type(resume_data)}")
        
        try:
            result = template.format(**resume_data)
            logger.error(f"Human prompt formatted successfully")
            return result
        except KeyError as e:
            logger.error(f"휴먼 프롬프트 렌더링 실패 - 누락된 변수: {e}")
            raise
        except Exception as e:
            logger.error(f"휴먼 프롬프트 렌더링 실패: {e}")
            raise
    
    def get_experience_level(self, years: int) -> str:
        """
        경력 연수에 따른 레벨 결정
        
        Args:
            years: 경력 연수
            
        Returns:
            str: 경력 레벨 ('junior', 'mid', 'senior')
        """
        if years <= 2:
            return 'junior'
        elif years <= 5:
            return 'mid'
        else:
            return 'senior'
    


# 전역 로더 인스턴스들
_loaders = {}

def get_prompt_loader(service_name: str) -> PromptLoader:
    """
    서비스별 프롬프트 로더 반환
    
    Args:
        service_name: 서비스명 ('interview', 'learning' 등)
        
    Returns:
        PromptLoader: 해당 서비스의 프롬프트 로더
    """
    if service_name not in _loaders:
        # Docker 컨테이너 내에서의 경로 설정
        # /app/shared/prompts/loader.py에서 /app/{service_name}-service/prompts로
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # /app
        prompts_dir = os.path.join(base_dir, f'{service_name}-service', 'prompts')
        
        logger.info(f"프롬프트 디렉토리 경로: {prompts_dir}")
        _loaders[service_name] = PromptLoader(prompts_dir)
    
    return _loaders[service_name]
