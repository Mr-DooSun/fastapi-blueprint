# FastAPI Layered Architecture

FastAPI를 기반으로 한 **Clean Architecture + Layered Architecture** 패턴을 구현한 프로젝트입니다.
도메인 중심의 설계와 의존성 주입을 통해 확장 가능하고 유지보수가 용이한 백엔드 시스템을 제공합니다.

## 🏗️ 아키텍처 개요

### 전체 구조
```
src/
├── core/           # 공통 인프라 및 베이스 클래스
└── server/         # 서버별 구현
    ├── application/ # 애플리케이션 계층
    ├── domain/     # 도메인 계층
    └── infrastructure/ # 인프라 계층
```

### 데이터 흐름
```
Router → UseCase → Service → Repository → Database
   ↓        ↓        ↓         ↓
  DTO    Entity   Entity    Entity
```

## 📁 프로젝트 구조 상세

### 🎯 Core 모듈 (`src/core/`)

공통 인프라와 베이스 클래스들을 제공하는 핵심 모듈입니다.

#### `application/` - 애플리케이션 계층
- **`dtos/`**: 데이터 전송 객체 (DTO)
  - `common/`: 공통 DTO (BaseRequest, BaseResponse, PaginationInfo)
  - `user/`: 사용자 관련 DTO
- **`use_cases/`**: 유스케이스 베이스 클래스
  - `base_use_case.py`: CRUD 작업을 위한 제네릭 베이스 클래스
- **`messaging/`**: 메시징 시스템
  - `rabbitmq_publisher.py`: RabbitMQ 메시지 발행

#### `domain/` - 도메인 계층
- **`entities/`**: 도메인 엔티티
  - `entity.py`: 모든 엔티티의 베이스 클래스
  - `user/`: 사용자 관련 엔티티
- **`services/`**: 도메인 서비스
  - `base_service.py`: 서비스 베이스 클래스
  - `minio_service.py`: MinIO 스토리지 서비스
  - `s3_service.py`: AWS S3 스토리지 서비스
- **`enums/`**: 도메인 열거형

#### `infrastructure/` - 인프라 계층
- **`database/`**: 데이터베이스 관련
  - `database.py`: MySQL 연결 및 세션 관리
  - `models/`: SQLAlchemy 모델
    - `user/`: 사용자 모델
- **`repositories/`**: 리포지토리
  - `base_repository.py`: 제네릭 베이스 리포지토리
- **`messaging/`**: 메시징 인프라
  - `rabbitmq_manager.py`: RabbitMQ 연결 관리
- **`di/`**: 의존성 주입
  - `core_container.py`: 공통 컨테이너 (DB, MinIO, RabbitMQ)

#### `middleware/` - 미들웨어
- **`exception_middleware.py**: 전역 예외 처리 미들웨어

#### `exceptions/` - 예외 처리
- **`base_exception.py`: 커스텀 예외 베이스 클래스

#### `common/` - 공통 유틸리티
- **`dto_utils.py`: DTO 변환 유틸리티
- **`pagination.py`: 페이지네이션 유틸리티

### 🚀 Server 모듈 (`src/server/`)

실제 서버 구현을 담당하는 모듈입니다.

#### `application/` - 애플리케이션 계층
- **`routers/`**: FastAPI 라우터
  - `api/`: REST API 라우터
    - `health_check_router.py`: 헬스 체크 엔드포인트
    - `user/`: 사용자 관련 API
  - `websocket/`: WebSocket 라우터
    - `chat/`: 채팅 관련 WebSocket
- **`use_cases/`**: 서버별 유스케이스
  - `user/`: 사용자 관련 유스케이스

#### `domain/` - 도메인 계층
- **`services/`**: 서버별 도메인 서비스
  - `user/`: 사용자 서비스
- **`entities/`**: 서버별 엔티티
- **`enums/`**: 서버별 열거형

#### `infrastructure/` - 인프라 계층
- **`repositories/`**: 서버별 리포지토리
  - `user/`: 사용자 리포지토리
- **`di/`**: 의존성 주입
  - `server_container.py`: 서버 컨테이너
  - `containers/`: 도메인별 컨테이너
    - `user_container.py`: 사용자 도메인 컨테이너
    - `storage_container.py`: 스토리지 컨테이너
- **`bootstrap/`**: 애플리케이션 부트스트랩
  - `api_route_registry.py`: API 라우터 등록
  - `websocket_route_registry.py`: WebSocket 라우터 등록
  - `admin_registry.py`: 관리자 페이지 등록

#### `admin/` - 관리자 페이지
- **`views/`**: SQLAdmin 뷰
  - `user/`: 사용자 관리 뷰

#### `exceptions/` - 서버별 예외 처리

### 📦 기타 파일들

- **`config.yml`**: 애플리케이션 설정
- **`docker-compose.yml`**: Docker Compose 설정
- **`pyproject.toml`**: 프로젝트 의존성 및 메타데이터
- **`alembic.ini`**: 데이터베이스 마이그레이션 설정
- **`run_server_local.py`**: 로컬 서버 실행 스크립트

## 🚀 시작하기

### 1. 프로젝트 설치
```bash
git clone https://github.com/Mr-DooSun/fastapi_layered_architecture.git
cd fastapi_layered_architecture
```

### 2. 의존성 설치
```bash
uv venv --python 3.12.9
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .
```

### 3. 환경 설정
```bash
# 환경 변수 파일 생성
cp _env/dev.env.example _env/dev.env
# 필요한 환경 변수 설정
```

### 4. 데이터베이스 설정
```bash
# 데이터베이스 마이그레이션
alembic upgrade head
```

### 5. 프로젝트 실행
```bash
python run_server_local.py --env dev
```

## 🔧 주요 기능

### ✅ Clean Architecture
- **계층별 명확한 책임 분리**
- **의존성 역전 원칙 적용**
- **테스트 용이성**

### ✅ 의존성 주입
- **Dependency Injector 사용**
- **도메인별 컨테이너 분리**
- **느슨한 결합**

### ✅ 제네릭 베이스 클래스
- **CRUD 작업 표준화**
- **코드 중복 최소화**
- **일관된 API 응답**

### ✅ 데이터베이스
- **MySQL + SQLAlchemy**
- **비동기 세션 관리**
- **Alembic 마이그레이션**

### ✅ 메시징 시스템
- **RabbitMQ 지원**
- **비동기 메시지 처리**

### ✅ 스토리지
- **MinIO 지원**
- **AWS S3 지원**

### ✅ 관리자 페이지
- **SQLAdmin 기반**
- **데이터베이스 관리 UI**

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **관리자 페이지**: http://localhost:8000/admin

## 🧪 테스트

```bash
# 테스트 실행
pytest

# 커버리지 확인
pytest --cov=src
```

## 🐳 Docker 배포

```bash
# Docker 이미지 빌드
docker build -f _docker/docker.Dockerfile -t fastapi-layered .

# Docker Compose 실행
docker-compose up -d
```

## 📈 확장 가이드

### 새로운 도메인 추가
1. `src/server/application/routers/api/` 에 새 라우터 생성
2. `src/server/application/use_cases/` 에 새 유스케이스 생성
3. `src/server/domain/services/` 에 새 서비스 생성
4. `src/server/infrastructure/repositories/` 에 새 리포지토리 생성
5. `src/server/infrastructure/di/containers/` 에 새 컨테이너 생성

### 새로운 기능 추가
1. 기존 베이스 클래스 상속
2. 제네릭 타입 활용
3. 의존성 주입 컨테이너에 등록

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.
