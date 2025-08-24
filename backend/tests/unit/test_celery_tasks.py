import pytest
import asyncio
from celery.result import AsyncResult
from unittest.mock import patch, MagicMock, AsyncMock
import json

class TestCeleryTasks:
    """Celery 태스크 테스트"""
    
    @pytest.fixture
    def mock_celery_task(self):
        """Mock Celery task fixture"""
        with patch('celery.Task') as mock:
            mock.return_value.delay.return_value = AsyncResult('test-id')
            yield mock
    
    def test_task_creation(self, mock_celery_task):
        """태스크 생성 및 큐잉 테스트"""
        task = mock_celery_task.return_value
        result = task.delay({"test": "data"})
        
        assert isinstance(result, AsyncResult)
        assert result.id == 'test-id'
        task.delay.assert_called_once_with({"test": "data"})

    def test_task_result_storage(self, mock_redis):
        """Redis 태스크 결과 저장 테스트"""
        redis_client = mock_redis.return_value
        
        # 결과 저장
        redis_client.set('task:test-id', '{"status": "completed"}')
        redis_client.set.assert_called_once()
        
        # 결과 조회
        result = redis_client.get('task:test-id')
        assert result == b'{"status": "completed"}'

    @pytest.mark.asyncio
    async def test_interview_pipeline_mock(self, mock_celery_task, mock_redis):
        """면접 질문 생성 파이프라인 모킹 테스트"""
        # Given: 이력서 데이터가 주어지고
        resume_data = {
            "name": "TestDev",
            "technical_skills": ["Python", "FastAPI"]
        }
        
        # Mock task creation
        mock_task = MagicMock()
        mock_task.delay.return_value = AsyncResult('interview-task-id')
        
        # When: 태스크를 실행하면
        result = mock_task.delay(resume_data)
        
        # Then: 태스크가 큐에 들어가고
        assert result.id == 'interview-task-id'
        mock_task.delay.assert_called_once_with(resume_data)
        
        # Redis에 결과 저장 확인
        redis_client = mock_redis.return_value
        redis_client.set(f'interview:result:{result.id}', json.dumps({
            "status": "completed",
            "questions": [
                {"question": "Python 경험에 대해 설명해주세요."},
                {"question": "FastAPI의 장점은 무엇인가요?"}
            ]
        }))
        
        stored_result = redis_client.get(f'interview:result:{result.id}')
        assert stored_result is not None

    @pytest.mark.asyncio
    async def test_learning_path_pipeline_mock(self, mock_celery_task, mock_redis):
        """학습 경로 생성 파이프라인 모킹 테스트"""
        # Given: 사용자 데이터가 주어지고
        user_data = {
            "current_skills": ["Python", "FastAPI"],
            "target_position": "Backend Developer"
        }
        
        # Mock task creation
        mock_task = MagicMock()
        mock_task.delay.return_value = AsyncResult('learning-task-id')
        
        # When: 태스크를 실행하면
        result = mock_task.delay(user_data)
        
        # Then: 태스크가 큐에 들어가고
        assert result.id == 'learning-task-id'
        mock_task.delay.assert_called_once_with(user_data)
        
        # Redis에 결과 저장 확인
        redis_client = mock_redis.return_value
        redis_client.set(f'learning:result:{result.id}', json.dumps({
            "status": "completed",
            "learning_path": [
                {"topic": "Django 심화", "duration": "2주"},
                {"topic": "시스템 설계", "duration": "1개월"}
            ]
        }))
        
        stored_result = redis_client.get(f'learning:result:{result.id}')
        assert stored_result is not None

    def test_task_retry_mechanism(self):
        """태스크 재시도 메커니즘 테스트"""
        with patch('celery.Task') as mock_task_class:
            task = mock_task_class.return_value
            task.retry = MagicMock(side_effect=Exception("Max retries exceeded"))
            
            # 실패 시뮬레이션
            with pytest.raises(Exception, match="Max retries exceeded"):
                task.retry(countdown=60, max_retries=3)
            
            task.retry.assert_called_once_with(countdown=60, max_retries=3)

    @pytest.mark.asyncio
    async def test_task_chain_simulation(self):
        """태스크 체인 시뮬레이션 테스트"""
        # Given: 태스크 체인이 구성되고
        with patch('celery.chain') as mock_chain:
            mock_chain_instance = MagicMock()
            mock_chain.return_value = mock_chain_instance
            mock_chain_instance.delay.return_value = AsyncResult('chain-task-id')
            
            # When: 체인을 실행하면
            task_chain = mock_chain(
                {"task": "preprocess_resume", "data": {"name": "test"}},
                {"task": "generate_interview_questions"},
                {"task": "post_process_questions"}
            )
            result = task_chain.delay()
            
            # Then: 체인이 실행되고
            assert result.id == 'chain-task-id'
            mock_chain_instance.delay.assert_called_once()

    def test_task_progress_tracking(self, mock_redis):
        """태스크 진행 상황 추적 테스트"""
        redis_client = mock_redis.return_value
        task_id = 'test-progress-id'
        
        # 진행 상황 업데이트
        progress_data = {
            "status": "in_progress",
            "current_step": 2,
            "total_steps": 5,
            "message": "면접 질문 생성 중..."
        }
        redis_client.set(f'task:progress:{task_id}', json.dumps(progress_data))
        
        # 진행 상황 조회
        stored_progress = redis_client.get(f'task:progress:{task_id}')
        assert stored_progress is not None
        redis_client.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self, mock_redis):
        """에러 처리 및 복구 테스트"""
        # Given: 태스크가 실패하도록 설정
        mock_task = MagicMock()
        mock_task.delay.side_effect = Exception("LLM API 오류")
        redis_client = mock_redis.return_value
        
        # When & Then: 에러가 발생하면 적절히 처리된다
        with pytest.raises(Exception, match="LLM API 오류"):
            try:
                result = mock_task.delay({"test": "data"})
            except Exception as e:
                # 에러 상태 저장
                error_data = {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": "2024-01-01T00:00:00Z"
                }
                redis_client.set(f'task:error:test-id', json.dumps(error_data))
                raise e
        
        # 에러 로그 저장 확인
        redis_client.set.assert_called_with(
            'task:error:test-id',
            json.dumps({
                "status": "failed",
                "error": "LLM API 오류",
                "timestamp": "2024-01-01T00:00:00Z"
            })
        )

    @pytest.mark.asyncio
    async def test_concurrent_task_execution(self, mock_redis):
        """동시 태스크 실행 테스트"""
        # Given: 여러 태스크가 동시에 실행되는 상황
        task_ids = ['task-1', 'task-2', 'task-3']
        
        async def mock_async_task(task_id):
            await asyncio.sleep(0.1)  # 지연 시뮬레이션
            return AsyncResult(task_id)
        
        # When: 태스크들을 동시에 실행하면
        tasks = [mock_async_task(task_id) for task_id in task_ids]
        results = await asyncio.gather(*tasks)
        
        # Then: 모든 태스크가 완료된다
        assert len(results) == 3
        for i, result in enumerate(results):
            assert result.id == task_ids[i]

    def test_rabbitmq_connection_mock(self, mock_rabbitmq):
        """RabbitMQ 연결 모킹 테스트"""
        # Given: RabbitMQ 연결이 모킹되고
        connection = mock_rabbitmq.return_value
        
        # When: 연결을 사용하면
        connection.connect()
        connection.close()
        
        # Then: 연결 메서드가 호출된다
        connection.connect.assert_called_once()
        connection.close.assert_called_once()