# Prompt Builder 세션

Prompt Builder 세션은 한 에이전트 세션이 project prompt만 만들고, 실제 작업은 다른 에이전트 세션이 수행하게 할 때 사용합니다.

이 패턴은 기존 프로젝트, 위험도가 높은 작업, 운영 조사, 장기 handoff에 유용합니다. Prompt Builder 세션은 아직 정리되지 않은 의도를 contract JSON과 rendered prompt로 바꿉니다. 코드 수정, 운영 시스템 접속, 실제 작업 수행은 하지 않아야 합니다.

## 세션 시작 프롬프트

대상 프로젝트 안에서 새 에이전트 세션을 열고 아래 프롬프트를 붙여넣습니다.

```text
너는 이 프로젝트의 Prompt Builder다.

.tools/project-prompt-kit를 사용해서 project prompt만 작성해라.
직접 코드 수정, git commit, DB 접속, 운영 작업, 요청된 실제 작업 수행은 하지 마라.

내가 제공하는 목표, 범위, 배경, 제약을 바탕으로:
1. mode와 target renderer를 선택하거나 확인한다.
2. contract JSON을 작성한다.
3. rendered prompt markdown을 작성한다.
4. 내가 workspace strategy를 제공하면 rendered prompt에 반영한다.
5. 내가 infrastructure boundaries를 제공하면 rendered prompt에 반영한다.
6. 필수 정보가 부족할 때만 짧은 질문 하나를 한다.

프로젝트 규칙:
- AGENTS.md와 하위 AGENTS.md를 지켜라.
- .promptkitignore를 지켜라.
- secret, environment 값, credential-bearing URL, local absolute path를 출력하지 마라.
- 운영 시스템에 접속하지 마라.
```

## 요청 형태

세션 시작 프롬프트 뒤에는 아래 형태로 요청합니다.

```text
mode: debug

target renderer:
codex, claude, generic 중 하나

workspace strategy:
현재 체크아웃은 다른 세션과 공유 중일 수 있고, 관련 없는 로컬 변경이 있을 수 있다.
worker는 현재 체크아웃을 read-only로 취급한다.
수정 작업 전에 remote를 fetch하고 요청된 remote base ref 기준의 새 worktree를 만든다.
codex/<task-slug> 같은 작업별 branch를 사용한다.
예: git worktree add ../<repo>-<task-slug> -b codex/<task-slug> origin/<base-branch>
worker는 새 worktree 안에서만 수정, 테스트, 커밋, 푸시한다.
worker는 현재 체크아웃에서 reset, clean, checkout, revert를 수행하지 않는다.

infrastructure boundaries:
worker는 운영 DB, 운영 API, cloud console, secret store, admin dashboard에 직접 접속하지 않는다.
운영 데이터가 필요하면 worker는 read-only SQL을 단계별로 작성한다.
내가 운영 DB에서 각 SQL을 실행하고 결과를 전달한다.
허용 SQL: read-only SELECT/WITH query.
금지 SQL: UPDATE, DELETE, INSERT, ALTER, DROP, LOCK, transaction control statement.
worker는 secret, credential, token, environment 값을 요청하거나 출력하거나 추론하지 않는다.
worker는 전달받은 운영 결과를 민감한 정보로 취급하고 필요한 최소 근거만 인용한다.

목표:
운영 환경 포인트 전송 트랜잭션 데이터 정합성을 조사한다.

진행 방식:
worker는 결과를 해석하고 다음 read-only SQL을 제안한다.

범위:
포인트 도메인만.

제약:
- AGENTS.md를 지켜라.
- .promptkitignore를 지켜라.
- secret, env 값, local absolute path를 출력하지 마라.
- 원인 분석만 하고 보정은 수행하지 않는다.

출력:
contract JSON과 rendered prompt markdown.
```

## 작업공간 전략 (Workspace Strategy)

현재 체크아웃이 공유 중이거나, dirty 상태이거나, 다른 에이전트 세션이 이미 사용 중이라면 workspace strategy를 사용합니다. Prompt Builder는 이 정책을 rendered worker prompt에 넣어 worker가 어디에서 write 작업을 해도 되는지 명확히 해야 합니다.

v0.1에서는 이 내용을 optional contract schema field로 둡니다. 모든 prompt에 필수로 만들지는 않습니다. read-only 작업이나 문서 작업은 worktree 격리가 필요하지 않을 수 있기 때문입니다.

권장 worker 정책:

```text
현재 체크아웃은 read-only context다.
worktree 생성 전에 git fetch origin을 실행한다.
요청된 remote base ref에서 작업별 worktree를 만든다.
요청된 branch prefix로 작업별 branch를 만든다.
새 worktree 안에서 AGENTS.md를 다시 읽고 수정한다.
수정, 테스트, 커밋, 푸시는 새 worktree 안에서만 한다.
기존 체크아웃의 관련 없는 파일을 reset, clean, checkout, revert하지 않는다.
```

## 인프라 경계 (Infrastructure Boundaries)

작업이 DB, 운영 API, cloud console, secret store, admin dashboard 같은 외부 시스템을 건드릴 수 있다면 infrastructure boundaries를 사용합니다. Prompt Builder는 접근 규칙을 일반 제약 목록에 묻어두지 말고 rendered worker prompt에 별도 경계로 명확히 적어야 합니다.

v0.1에서는 이 내용을 optional contract schema field로 둡니다. 모든 prompt에 필수로 만들지는 않습니다. local-only prompt는 외부 인프라를 건드리지 않을 수 있기 때문입니다.

권장 worker 정책:

```text
worker는 운영 인프라에 직접 접속하지 않는다.
worker는 사람 운영자에게 승인된 read-only command나 query 실행을 요청할 수 있다.
운영 SQL은 prompt가 명시적으로 더 허용하지 않는 한 read-only SELECT/WITH만 사용한다.
worker는 각 query의 목적을 먼저 설명한 뒤 query를 제시한다.
worker는 사람이 반환한 결과를 받은 뒤 다음 운영 query를 제안한다.
worker는 secret, token, credential, environment 값을 요청하거나 노출하거나 추론하지 않는다.
반환된 운영 데이터는 민감 정보로 취급하고 필요한 최소 근거만 인용한다.
```

## 로컬 산출물

로컬 전용으로 사용할 때는 생성된 prompt 산출물을 vendored kit 아래에 둡니다.

```text
.tools/project-prompt-kit/local/contracts/
.tools/project-prompt-kit/local/rendered/
```

프로젝트가 kit를 의도적으로 vendor로 포함하지 않는다면 `.tools/`는 git에서 제외하세요.

## 역할 분리

- Prompt Builder 세션: prompt contract와 rendered prompt만 작성합니다.
- Worker 세션: rendered prompt를 실행합니다.
- 사람 운영자: 위험한 작업을 승인하고, 운영 전용 read-only query가 필요할 때 직접 실행합니다.

이 방식은 prompt 작성은 portable하게 유지하면서 운영 데이터와 프로젝트 secret의 safety boundary를 지킵니다.
