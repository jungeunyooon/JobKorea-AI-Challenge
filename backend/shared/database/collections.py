"""
MongoDB 컬렉션 이름 상수 및 스키마 정의
"""

class Collections:
    """컬렉션 이름 상수"""
    RESUMES = "resumes"
    INTERVIEW_QUESTIONS = "interview_questions"
    LEARNING_PATHS = "learning_paths"


class CollectionSchemas:
    """MongoDB 컬렉션 스키마 정의"""
    
    @staticmethod
    def get_resumes_schema():
        """이력서 컬렉션 스키마"""
        return {
            "_id": "ObjectId",  # MongoDB 자동 생성 ID
            "name": "str",      # 이름 (1-50자)
            "contact": {        # 연락처 정보
                "phone": "str (optional)",
                "email": "str (optional)", 
                "github": "str (optional, URL)",
                "linkedin": "str (optional, URL)",
                "portfolio": "str (optional, URL)"
            },
            "summary": "str",   # 한 줄 요약/소개 (10-500자)
            "work_experiences": [  # 경력 사항 배열
                {
                    "company": "str",              # 회사명
                    "position": "str",             # 직책
                    "duration": "str",             # 근무 기간
                    "project_name": "str (optional)",      # 주요 프로젝트명
                    "project_description": "str (optional)", # 프로젝트 설명
                    "tech_stack": ["str"],         # 사용 기술 스택
                    "achievements": ["str"],       # 주요 성과
                    "team_size": "int (optional, >= 1)"    # 팀 규모
                }
            ],
            "total_experience_months": "int (>= 0)",  # 총 경력 (개월)
            "personal_projects": [  # 개인/팀 프로젝트 배열
                {
                    "name": "str",                 # 프로젝트명
                    "duration": "str (optional)",          # 개발 기간
                    "description": "str",          # 프로젝트 설명
                    "tech_stack": ["str"],         # 사용 기술 스택
                    "github_url": "str (optional, URL)",   # GitHub URL
                    "demo_url": "str (optional, URL)",     # 데모 URL
                    "key_achievements": ["str"],   # 주요 성과
                    "architecture_highlights": ["str"]  # 아키텍처 특이사항
                }
            ],
            "technical_skills": {  # 기술 스킬 (세분화)
                "programming_languages": ["str"],    # 프로그래밍 언어
                "frameworks": ["str"],               # 프레임워크
                "databases": ["str"],                # 데이터베이스
                "message_queue_caching": ["str"],    # 메시지 큐 및 캐싱
                "cloud_platforms": ["str"],          # 클라우드 플랫폼
                "devops_tools": ["str"],             # DevOps 도구
                "monitoring_tools": ["str"],         # 모니터링 도구
                "others": ["str"]                    # 기타 도구/기술
            },
            "certifications": [  # 자격증 및 인증 배열
                {
                    "name": "str",                   # 자격증명
                    "issuer": "str",                 # 발급기관
                    "issue_date": "str",             # 취득일 (YYYY.MM.DD)
                    "expiry_date": "str (optional)",        # 만료일
                    "credential_url": "str (optional, URL)" # 자격증 확인 URL
                }
            ],
            "activities": [  # 관련 활동 배열
                {
                    "type": "str",                   # 활동 유형
                    "name": "str",                   # 활동명/단체명
                    "description": "str",            # 활동 설명 및 역할
                    "period": "str (optional)",             # 활동 기간
                    "achievements": ["str"],         # 주요 성과
                    "url": "str (optional, URL)"            # 관련 URL
                }
            ],
            "education": [  # 교육 배경 배열
                {
                    "institution": "str",            # 학교명
                    "degree": "str",                 # 학위/과정명
                    "major": "str",                  # 전공
                    "period": "str",                 # 재학 기간
                    "status": "str"                  # 상태 (졸업, 재학, 수료 등)
                }
            ],
            "unique_key": "str",        # 이름 기반 고유 키 (이름_1, 이름_2 등)
            "created_at": "datetime",   # 생성 시간
            "updated_at": "datetime"    # 수정 시간
        }
    
    @staticmethod
    def get_interview_questions_schema():
        """면접 질문 컬렉션 스키마"""
        return {
            "_id": "ObjectId",          # MongoDB 자동 생성 ID
            "interview_id": "str",      # 면접 질문 세션 ID
            "resume_id": "str",         # 이력서 ID 참조
            "unique_key": "str",        # 이력서 고유 키
            "provider": "str",          # LLM 제공자 (openai, claude, gemini)
            "model": "str",             # 사용된 LLM 모델명
            "questions": [              # 면접 질문 배열 (1-5개)
                {
                    "difficulty": "str",     # 난이도 (easy|medium|hard)
                    "topic": "str",          # 주요 기술 키워드
                    "question": "str",       # 실제 질문 본문
                    "what_good_answers_cover": ["str"]  # 좋은 답변 포함 요소
                }
            ],
            "generated_at": "datetime"  # 생성 시간
        }
    
    @staticmethod
    def get_learning_paths_schema():
        """학습 경로 컬렉션 스키마"""
        return {
            "_id": "ObjectId",          # MongoDB 자동 생성 ID
            "resume_id": "str",         # 이력서 ID 참조
            "unique_key": "str",        # 이력서 고유 키
            "provider": "str",          # LLM 제공자 (openai, claude, gemini)
            "model": "str",             # 사용된 LLM 모델명
            "analysis": {               # 이력서 분석 결과
                "strengths": ["str"],   # 식별된 장점들
                "weaknesses": ["str"]   # 식별된 단점들
            },
            "summary": "str",           # 학습 경로 전체 요약
            "learning_paths": [         # 학습 경로 배열 (3-8개)
                {
                    "type": "str",           # 학습 유형 (strength|weakness)
                    "title": "str",          # 학습 제목
                    "description": "str",    # 학습 설명 및 목표
                    "reason": "str",         # 학습 제시 이유
                    "resources": ["str"],    # 추천 학습 리소스/방법
                    "link": "str"            # 관련 학습 링크
                }
            ],
            "generated_at": "datetime"  # 생성 시간
        }

