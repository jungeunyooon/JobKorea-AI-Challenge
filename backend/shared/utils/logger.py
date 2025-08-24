"""
공통 로거 설정
"""

import logging
import sys

def setup_logger(service_name: str, log_level: str = "INFO") -> logging.Logger:
    """서비스별 표준화된 로거 설정"""
    
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 중복 핸들러 방지
    if not logger.handlers:
        # 콘솔 핸들러
        handler = logging.StreamHandler(sys.stdout)
        
        # 포맷터 설정
        formatter = logging.Formatter(
            f'%(asctime)s - {service_name} - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # 루트 로거와 분리
        logger.propagate = False
    
    return logger
