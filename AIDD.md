# AIDD.md — AI 개발 가이드

> 이 프로젝트는 Claude + Serena MCP를 중심으로 한 **AIDD (AI-Driven Development)** 방법론으로 관리됩니다.
> 새 세션 시작 시 이 파일과 CLAUDE.md를 먼저 읽으세요.

---

## 1. 아키텍처 한 줄 요약

**DDD 기반 모듈형 레이어드 아키텍처** — 도메인별로 4계층(Interface / Application / Domain / Infrastructure)을 완전히 분리한 구조.

```
의존성 방향: Interface → Application → Domain ← Infrastructure
```

---

## 2. 데이터 흐름 (유일한 정답)

```
[Request]          CreateUserRequest(BaseRequest)
                   ↓ CreateUserDTO(**item.model_dump())
[UseCase]          CreateUserDTO
                   ↓
[Service]          CreateUserDTO
                   ↓
[Repository]       UserModel(**dto.model_dump())  →  DB
                   DB  →  UserDTO.model_validate(model, from_attributes=True)
                   ↑
[Service/UseCase]  UserDTO
                   ↓ UserResponse(**dto.model_dump(exclude={'password'}))
[Response]         UserResponse(BaseResponse)
```

---

## 3. 객체 역할

| 타입 | 위치 | 역할 |
|---|---|---|
| `NameDTO` | `domain/dtos/` | 모든 레이어를 흐르는 내부 데이터. 민감 필드 포함 가능 |
| `NameResponse/Request` | `interface/server/dtos/` | API 경계 전용. 명시적 필드, 다중상속 금지 |
| `NameModel` | `infrastructure/database/models/` | DB 테이블 매핑. Repository 밖으로 절대 나가지 않음 |

---

## 4. 새 도메인 추가 (체크리스트)

```
src/{name}/
├── domain/
│   ├── dtos/{name}_dto.py          ← NameDTO, CreateNameDTO, UpdateNameDTO
│   ├── protocols/{name}_repository_protocol.py
│   ├── exceptions/{name}_exceptions.py
│   ├── events/{name}_events.py
│   └── services/{name}_service.py
├── application/
│   └── use_cases/{name}_use_case.py
├── infrastructure/
│   ├── database/models/{name}_model.py
│   ├── repositories/{name}_repository.py
│   └── di/{name}_container.py
└── interface/
    ├── server/
    │   ├── dtos/{name}_dto.py      ← NameResponse, CreateNameRequest, UpdateNameRequest
    │   └── routers/{name}_router.py
    └── worker/tasks/{name}_task.py (필요 시)
```

user 도메인을 참조 패턴으로 사용하세요.

---

## 5. 절대 금지 규칙

```python
# ❌ 다중상속
class UserResponse(BaseResponse, UserEntity): pass

# ❌ entity 변환 메서드
item.to_entity(CreateUserEntity)
UserResponse.from_entity(data)

# ❌ Domain에서 Infrastructure import
from src._core.infrastructure.database.base_repository import BaseRepository  # domain/에서

# ❌ Model을 Repository 밖으로 노출
return UserModel(...)  # service에서
```

---

## 6. AI 세션 시작 가이드

새 Claude 세션에서 작업을 이어갈 때:

```
1. "refactoring_status 메모리 확인해줘" — 현재 Phase 파악
2. 작업 요청 — Claude가 Serena로 자동 탐색 + context7으로 라이브러리 문서 확인
3. 커밋 전 — pre-commit hook 자동 실행 (아키텍처 위반 차단)
```

다른 디바이스에서 작업을 이어갈 때는 `AIDD_PLAN.md`를 먼저 읽으세요.

---

## 7. 검증 커맨드

```bash
# 서버 실행
uvicorn src._apps.server.app:app --reload --host 127.0.0.1 --port 8001

# 아키텍처 위반 검사
grep -r "from src._core.domain.entities" src/ --include="*.py"    # → 없어야 함
grep -r "from src._core.infrastructure" src/_core/domain/ --include="*.py"  # → 없어야 함
grep -r "\.to_entity\|\.from_entity" src/ --include="*.py"         # → 없어야 함

# 테스트
pytest tests/ -v
pytest tests/unit/ -v              # 단위 테스트만
pytest tests/integration/ -v      # 통합 테스트만
pytest tests/ -v --cov=src         # 커버리지 포함
```
