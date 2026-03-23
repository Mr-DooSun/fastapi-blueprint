# 013. 상속 대신 IoC Container를 선택한 이유

- 상태: Accepted
- 날짜: 2026-03-23
- 관련 이슈: #21
- 관련 ADR: 007-di-container-and-app-separation.md (보완)

## 배경

Python에서 의존성을 관리하는 가장 간단한 방법은 상속이다:

```python
class UserService:
    def __init__(self):
        self.repository = UserRepository()  # 직접 생성
```

또는 상속으로 Repository를 내장하는 방식:

```python
class BaseService(UserRepository):  # 상속으로 Repository 기능 포함
    pass
```

FastAPI에도 `Depends()`가 내장되어 있어 간단한 DI가 가능하다.
그런데 왜 별도의 IoC Container 라이브러리(`dependency-injector`)를 도입했는가?

## 문제: 상속과 직접 생성의 한계

### 1. 상속은 결합이다

```python
class UserService(UserRepository):
    pass
```

Service가 Repository를 **상속**하면:
- Service가 Repository의 **모든 메서드**를 갖게 됨 (의도하지 않은 DB 접근 노출)
- Repository 구현이 바뀌면 Service가 깨짐 (상속 체인 전파)
- Service가 여러 Repository를 사용해야 하면? Python은 다중상속이 가능하지만 MRO 충돌 위험

**상속은 "is-a" 관계**다. Service는 Repository가 아니라 Repository를 **사용**한다 ("has-a").

### 2. 직접 생성은 교체가 안 된다

```python
class UserService:
    def __init__(self):
        self.repository = UserRepository(database=Database())  # 하드코딩
```

- 테스트에서 MockRepository로 교체 불가 (DB 없이 테스트 불가)
- Database 인스턴스를 매번 새로 생성 (커넥션 풀 재사용 불가)
- Repository 구현체를 바꾸려면 Service 코드를 수정해야 함

### 3. FastAPI Depends()만으로는 부족한 경우

```python
@router.post("/user")
async def create_user(
    service: UserService = Depends(get_user_service)
):
    ...
```

FastAPI의 `Depends()`는 **Router 레벨에서만 작동**한다:
- Worker 태스크에서는 `Depends()` 사용 불가
- Service 간 의존성 (Service A가 Service B를 사용)을 표현하기 어려움
- 싱글톤 보장이 안 됨 (매 요청마다 새 인스턴스 가능)

## 결정

**dependency-injector 라이브러리로 IoC Container 도입**

### 생성자 주입 (Constructor Injection)

```python
# Service는 Protocol(인터페이스)에만 의존
class UserService(BaseService[UserDTO]):
    def __init__(self, user_repository: UserRepositoryProtocol):
        super().__init__(repository=user_repository)
```

- Service는 `UserRepositoryProtocol`만 알고, 구현체를 모름
- 실제 구현체 연결은 Container가 담당

### Container가 조립

```python
class UserContainer(containers.DeclarativeContainer):
    core_container = providers.DependenciesContainer()

    user_repository = providers.Singleton(
        UserRepository,
        database=core_container.database,  # DB는 싱글톤으로 공유
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,  # 여기서 구현체 연결
    )
```

### Server와 Worker가 같은 Container 재사용

```python
# Server Router — @inject로 Container에서 주입
@inject
async def create_user(
    user_service: UserService = Depends(Provide[UserContainer.user_service]),
): ...

# Worker Task — 동일한 패턴
@inject
async def consume_task(
    user_service: UserService = Provide[UserContainer.user_service],
): ...
```

## 근거

| 기준 | 상속 | 직접 생성 | FastAPI Depends | IoC Container |
|------|------|----------|----------------|---------------|
| 결합도 | 높음 (is-a) | 높음 (하드코딩) | 중간 | **낮음** (인터페이스만) |
| 테스트 | Mock 어려움 | Mock 불가 | Mock 가능 | **Mock 용이** |
| Worker 지원 | - | - | 불가 | **가능** |
| 싱글톤 보장 | - | 불가 | 불가 | **Singleton provider** |
| 레이어 분리 | 위반 | 위반 | Router만 | **전 계층** |

1. **Protocol + Container = DIP 실현**: Domain 레이어가 Infrastructure를 모르는 상태에서, Container가 런타임에 구현체를 연결한다. 이것이 "Domain에서 Infrastructure import 금지" 규칙을 가능하게 하는 핵심 메커니즘이다.

2. **Singleton으로 리소스 관리**: Database 커넥션 풀, HTTP 클라이언트, SQS 브로커 등 비싼 리소스를 `providers.Singleton`으로 한 번만 생성하고 전체 앱에서 공유한다.

3. **Server/Worker 코드 공유**: 같은 Service/Repository를 Server Router와 Worker Task에서 동일한 패턴(`@inject` + `Provide[]`)으로 사용한다. FastAPI `Depends()`만으로는 Worker에서 재사용이 불가능하다.

4. **테스트 격리**: Container를 override하면 실제 DB 없이 MockRepository로 테스트할 수 있다. 현재 단위 테스트에서 이 패턴을 적극 활용하고 있다.

## 레이어드 아키텍처의 확장성 한계를 IoC Container로 보완

레이어드 아키텍처의 대표적 단점은 **확장성**이다:
- 새 도메인 추가 시 각 레이어에 파일을 만들고 수동으로 등록해야 함
- 도메인 간 의존성이 생기면 레이어를 넘나드는 import가 발생
- 레이어가 고정적이라 유연한 조합이 어려움

IoC Container가 이 문제를 해결한다:

### 1. 도메인 자동 발견

```python
# src/_core/infrastructure/discovery.py
def discover_domains():
    # src/{name}/infrastructure/di/{name}_container.py를 자동 탐지
    # → DynamicContainer에 동적 등록
```

새 도메인 추가 시 `_apps/server/container.py`나 `bootstrap.py`를 **수정할 필요가 없다**.
Container만 규칙에 맞게 만들면 자동으로 등록된다.

### 2. 도메인 간 의존성을 Container 레벨에서 해결

```python
# quiz_container가 chat_service를 사용해야 할 때
class QuizContainer(containers.DeclarativeContainer):
    core_container = providers.DependenciesContainer()

    # 다른 도메인의 Repository를 Protocol로 주입
    chat_repository = providers.Singleton(
        ChatRepository,
        database=core_container.database,
    )

    quiz_service = providers.Factory(
        QuizService,
        quiz_repository=quiz_repository,
        chat_repository=chat_repository,  # Container가 연결
    )
```

Domain 코드는 Protocol에만 의존하고, **실제 연결은 Container가 담당**한다.
레이어를 넘나드는 import 없이 도메인 간 의존성을 해결할 수 있다.

### 3. Interface별 유연한 조합

같은 도메인 Container를 Server/Worker/Admin에서 **필요한 것만 골라서** 조합할 수 있다:

```
Server: CoreContainer + UserContainer + QuizContainer (전체)
Worker: CoreContainer + QuizContainer (퀴즈 비동기 처리만)
Admin:  CoreContainer + UserContainer (사용자 관리만)
```

레이어드 아키텍처의 "고정적 구조" 한계를 Container의 **선언적 조합**으로 극복한다.

## 트레이드오프

| 이점 | 비용 |
|------|------|
| 레이어 간 완전한 분리 | dependency-injector 학습 필요 |
| 테스트 용이성 | Container 선언 boilerplate |
| 리소스 수명 관리 | 디버깅 시 Container 경유 추적 |
| Server/Worker 코드 공유 | `@inject` 데코레이터 패턴 숙지 필요 |

단순 CRUD만 있는 소규모 프로젝트라면 FastAPI `Depends()`로 충분하다.
이 프로젝트가 IoC Container를 도입한 것은 **엔터프라이즈급 확장성**(도메인 10개+, 팀원 5명+)과
**Server/Worker 비즈니스 로직 공유**를 전제로 설계했기 때문이다.
