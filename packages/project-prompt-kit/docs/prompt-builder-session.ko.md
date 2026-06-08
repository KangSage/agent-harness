# Prompt Builder 세션

Prompt Builder 세션은 한 에이전트 세션이 project prompt만 만들고, 실제 작업은 다른 에이전트 세션이 수행하게 할 때 사용합니다.

이 패턴은 이미 진행 중인 프로젝트, 위험도가 높은 작업, 운영 조사, 긴 handoff에 유용합니다. Prompt Builder 세션은 느슨한 의도를 contract JSON과 rendered prompt로 바꿉니다. 코드 수정, 운영 시스템 접속, 실제 작업 수행은 하지 않아야 합니다.

## 세션 시작 프롬프트

대상 프로젝트 안에서 새 에이전트 세션을 열고 아래 프롬프트를 붙여넣습니다.

```text
너는 이 프로젝트의 Prompt Builder다.

.tools/project-prompt-kit를 사용해서 Codex 작업 프롬프트만 작성해라.
직접 코드 수정, git commit, DB 접속, 운영 작업, 요청된 실제 작업 수행은 하지 마라.

내가 제공하는 목표, 범위, 배경, 제약을 바탕으로:
1. mode를 선택하거나 확인한다.
2. contract JSON을 작성한다.
3. rendered Codex prompt markdown을 작성한다.
4. 필수 정보가 부족할 때만 짧은 질문 하나를 한다.

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

목표:
운영 환경 포인트 전송 트랜잭션 데이터 정합성을 조사한다.

진행 방식:
worker는 운영 DB에 직접 접속하지 않는다.
worker는 read-only SQL을 단계별로 작성한다.
내가 운영 DB에서 각 SQL을 실행하고 결과를 전달한다.
worker는 결과를 해석하고 다음 read-only SQL을 제안한다.

범위:
포인트 도메인만.

제약:
- AGENTS.md를 지켜라.
- .promptkitignore를 지켜라.
- secret, env 값, local absolute path를 출력하지 마라.
- read-only SELECT/WITH SQL만 허용한다.
- UPDATE, DELETE, INSERT, ALTER, DROP, LOCK은 금지한다.
- 원인 분석만 하고 보정은 수행하지 않는다.

출력:
contract JSON과 rendered Codex prompt markdown.
```

## 로컬 산출물

로컬 전용으로 사용할 때는 생성된 prompt 산출물을 vendored kit 아래에 둡니다.

```text
.tools/project-prompt-kit/local/contracts/
.tools/project-prompt-kit/local/rendered/
```

프로젝트가 kit를 의도적으로 vendoring하지 않는다면 `.tools/`는 git에서 제외하세요.

## 역할 분리

- Prompt Builder 세션: prompt contract와 rendered prompt만 작성합니다.
- Worker 세션: rendered prompt를 실행합니다.
- 사람 운영자: 위험한 작업을 승인하고, 운영 전용 read-only query가 필요할 때 직접 실행합니다.

이 방식은 prompt 작성은 portable하게 유지하면서 운영 데이터와 프로젝트 secret의 safety boundary를 지킵니다.
