// MongoDB 초기 설정 스크립트
db = db.getSiblingDB('interview_coach');

// 사용자 생성
db.createUser({
    user: 'app_user',
    pwd: 'app_password',
    roles: [
        {
            role: 'readWrite',
            db: 'interview_coach'
        }
    ]
});
print('Database initialized successfully');
