"""
Celery 앱 설정
"""

import os
import importlib
from celery import Celery
from shared.config.base import BaseAppSettings

# 설정 로드
settings = BaseAppSettings()

# 현재 working directory 확인
current_dir = os.getcwd()
print(f"🔍 Current working directory: {current_dir}")

# Celery 앱 생성 (include 없이)
celery_app = Celery(
    "interview_coach",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)

# Working directory에 따라 tasks 강제 import
if 'interview-service' in current_dir:
    print("📍 Interview Service environment detected")
    if os.path.exists('tasks.py'):
        try:
            print("✅ Interview tasks.py found - importing directly")
            # Celery 앱 설정 완료 후 tasks 모듈 강제 import
            import sys
            sys.path.insert(0, os.getcwd())  # 현재 디렉토리를 path에 추가
            import tasks  # interview-service/tasks.py import
            print(f"🎯 Successfully imported interview tasks module")
            
            # 등록된 tasks 확인
            task_names = [name for name in celery_app.tasks.keys() if 'tasks.' in name]
            print(f"📋 Registered interview tasks: {task_names}")
        except Exception as e:
            print(f"❌ Failed to import interview tasks: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ tasks.py not found in interview-service")
        
elif 'learning-service' in current_dir:
    print("📍 Learning Service environment detected")
    if os.path.exists('tasks.py'):
        try:
            print("✅ Learning tasks.py found - importing directly")
            # Celery 앱 설정 완료 후 tasks 모듈 강제 import
            import sys
            sys.path.insert(0, os.getcwd())  # 현재 디렉토리를 path에 추가
            import tasks  # learning-service/tasks.py import
            print(f"🎯 Successfully imported learning tasks module")
            
            # 등록된 tasks 확인
            task_names = [name for name in celery_app.tasks.keys() if 'learning_service.tasks.' in name or 'tasks.' in name]
            print(f"📋 Registered learning tasks: {task_names}")
        except Exception as e:
            print(f"❌ Failed to import learning tasks: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ tasks.py not found in learning-service")
        
else:
    print("🔄 General environment - tasks loaded individually by workers")
    print("📋 Each worker handles its own task loading")

# Celery 설정
celery_app.conf.update(
    task_serializer=settings.celery_task_serializer,
    accept_content=[settings.celery_accept_content],
    result_serializer=settings.celery_result_serializer,
    timezone=settings.celery_timezone,
    enable_utc=True,
    
    # 작업 라우팅
    task_routes={
        'tasks.*': {'queue': 'interview_queue'},
        'learning_service.tasks.*': {'queue': 'learning_queue'},
    },
    
    # 성능 최적화
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=False,
    
    # 재시도 설정
    task_default_retry_delay=60,
    task_max_retries=3,
    
    # 결과 만료 시간 (1시간)
    result_expires=3600,
    
    # 작업 추적 활성화
    task_track_started=True,
    task_send_sent_event=True,
    
    # 결과 확장 정보 포함 (serialization 문제 해결)
    result_extended=True,
    
    # 보다 안전한 serialization 설정
    task_ignore_result=False,
    task_store_errors_even_if_ignored=True,
)

# 큐 설정
celery_app.conf.task_default_queue = 'default'
celery_app.conf.task_queues = {
    'default': {
        'exchange': 'default',
        'routing_key': 'default',
    },
    'interview_queue': {
        'exchange': 'interview',
        'routing_key': 'interview',
    },
    'learning_queue': {
        'exchange': 'learning', 
        'routing_key': 'learning',
    }
}

if __name__ == '__main__':
    celery_app.start()
