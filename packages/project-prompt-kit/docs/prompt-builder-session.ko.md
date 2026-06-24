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
6. 내가 communication policy를 제공하면 rendered prompt에 반영한다.
7. 역할별 검토가 worker prompt 품질을 높인다면 review panel을 고른다.
8. 필수 정보가 부족할 때만 짧은 질문 하나를 한다.

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

communication policy:
worker는 사용자에게 질문하거나 진행 상황을 보고하거나 최종 요약을 작성할 때 사용자의 언어를 사용한다.
agent-to-agent handoff, 내부 조율 메모, 압축된 기술 brief는 simple English를 사용한다.
agent-to-agent English는 짧고 직접적이며 불필요한 표현을 줄인다.
code, command, SQL, log, error, identifier, file path는 번역하지 않는다.
SQL의 목적과 해석은 사용자의 언어로 설명하되 SQL 본문은 그대로 유지한다.
운영 query 결과가 필요하면 사용자에게 한 번에 하나씩 사용자의 언어로 질문한다.

review panel:
이 작업에 필요한 역할만 고른다.
구현 작업이면 CTO Reviewer, Software Architect, QA Engineer, Security / Privacy Reviewer를 포함한다.
운영 장애나 운영 조사면 CTO Reviewer, Software Architect, QA Engineer, Operations / CS Lead, Security / Privacy Reviewer를 포함한다.
정책, 약관, 고객 공지면 Legal / Compliance Risk Screener, Operations / CS Lead, Product / Information Architecture Reviewer, Growth / Marketing Reviewer를 포함한다.
신규 기능 기획이면 CTO Reviewer, Product / Information Architecture Reviewer, UX / Product Designer, Growth / Marketing Reviewer, QA Engineer를 포함한다.
문서나 handoff면 Product / Information Architecture Reviewer, Operations / CS Lead, QA Engineer, CTO Reviewer를 포함한다.
Legal / Compliance Risk Screener는 법률/컴플라이언스 리스크 식별과 변호사 검토 필요 지점 표시로만 한정하며, 확정 법률 자문이나 컴플라이언스 승인은 하지 않는다.

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

## 커뮤니케이션 정책 (Communication Policy)

rendered prompt는 한 언어로 작성되지만 worker가 사용자에게는 다른 언어로 말해야 할 수 있다면 communication policy를 사용합니다. Prompt Builder는 사용자-facing 언어와 agent-to-agent 조율 언어를 분리해서 명확히 적어야 합니다.

v0.1에서는 이 내용을 optional contract schema field로 둡니다. 모든 prompt에 필수로 만들지는 않습니다. 어떤 prompt는 이미 하나의 명확한 커뮤니케이션 언어를 갖고 있기 때문입니다.

권장 worker 정책:

```text
사용자에게 하는 질문, 진행 상황 보고, 최종 요약은 사용자의 언어로 작성한다.
agent-to-agent handoff와 압축된 기술 조율 메모는 simple English를 사용한다.
agent-to-agent English는 짧고 직접적이며 불필요한 표현을 줄인다.
code, command, SQL, log, error, identifier, file path는 번역하지 않는다.
SQL의 목적과 해석은 사용자의 언어로 설명하되 SQL 본문은 그대로 유지한다.
운영 결과가 필요하면 사용자-facing 질문을 한 번에 하나씩 한다.
```

## 거버넌스 선택 (Governance Selection)

worker prompt가 작업을 시작하기 전에 계획 검토, 리스크 gate, 상황별 checklist를 먼저 정리해야 한다면 governance selection을 사용합니다.

v0.2에서는 이 내용을 optional contract guidance로 둡니다. 가볍게 유지하세요. 미해결 리스크가 보이도록 만드는 최소한의 governance layer만 고릅니다.

세부 확장 규칙의 기준은 `governance-presets.md`입니다. 이 세션 가이드는 어떤 governance layer를 고를지만 돕습니다.

### 거버넌스 선택 질문

사용자가 governance 선택을 명확히 주지 않았다면 아래 질문을 순서대로 확인합니다. Prompt Builder는 preset과 scenario template을 추천할 수 있지만, 필요한 근거가 부족한 상태에서 자동 결정하지 않습니다.

1. 이 작업이 인증, 권한, 개인정보, 결제, 정산, 운영 데이터, 고객 영향, rollout, rollback, 지원 운영에 영향을 주는가?
2. 운영 장애, 데이터 정합성 문제, 고객에게 보여줄 설명, 운영 영향 후속 조치가 관련되는가?
3. 보관, 삭제, 동의, 고지, 정책, 규제 데이터 처리, 변호사 검토 트리거가 관련되는가?
4. rollback, fallback, support path, 고객 커뮤니케이션 owner, runbook 준비 상태가 불명확한가?
5. 외부 인프라, 고객 영향, 사람 승인 경계가 없는 낮은 위험의 local-only 작업인가?

high-risk trigger가 하나라도 명확하면 preset을 `standard`나 `light`로 낮춰 선택하지 않습니다. 답이 불명확하면 추측하지 말고 사용자-facing 질문 하나를 짧게 묻습니다. 이 흐름은 prompt 작성 가이드이며 automatic risk classifier가 아닙니다.

`governance.preset`은 검토 강도를 고를 때 사용합니다.

- `light`: 낮은 위험의 작업에서 scope, acceptance, validation만 빠르게 확인할 때.
- `standard`: 일반 구현 계획에서 제품, 아키텍처, QA 검토가 필요할 때.
- `high_risk`: 인증, 권한, 개인정보, 운영 데이터, 결제, 고객 영향, 법무/컴플라이언스 검토 트리거, 지원 운영, rollout, rollback에 영향을 줄 수 있을 때.

`governance.scenario_template`은 상황별 체크리스트를 추가할 때 사용합니다.

- `auth_migration`: session, token, permission, account recovery, audit log, authentication data flow가 바뀔 수 있을 때.
- `production_incident`: 장애나 운영 데이터 정합성 문제를 조사, 완화, 설명, 후속 조치할 때.
- `regulated_data_or_domain`: 보관, 삭제, 동의, 고지, 정책, 규제 데이터 처리, 변호사 검토 트리거가 관련될 수 있을 때.

governance layer가 필요 없다면 `governance` block을 생략합니다.
`none` preset은 추가하지 않습니다.
`governance.review_panel_preset`은 만들지 않습니다.

governance를 선택했다면 reviewer 지시는 기존 `review_panel` 구조로 풀어 씁니다. Legal / Compliance 역할은 자격 있는 사람이 검토해야 할 리스크 트리거를 식별하는 용도이며, 법률 자문이나 컴플라이언스 승인을 제공하지 않습니다.

### 과잉 적용 / 과소 적용 예시

| 상황 | 권장 선택 | 이유 |
| --- | --- | --- |
| 정책, 릴리즈, 고객 영향이 없는 단순 문서 오타 수정 | `governance` 생략 또는 빠른 acceptance check가 필요할 때만 `light` | high-risk 검토는 새 리스크를 드러내지 못하고 절차만 늘립니다 |
| 민감 데이터나 운영 경계는 없지만 제품, 아키텍처, QA 불확실성이 있는 일반 기능 기획 | `standard` | 계획 검토는 필요하지만 high-risk trigger는 없습니다 |
| 인증 모듈 교체, 권한 변경, 운영 데이터 조사, 결제/정산 경로, 고객 영향 장애 | `high_risk`, 필요하면 맞는 scenario template 추가 | 명확한 high-risk trigger는 낮춰 선택하면 안 됩니다 |
| worker가 직접 DB 접속은 하지 않고 사람이 실행할 SQL을 작성하는 운영 데이터 정합성 조사 | `high_risk` + `production_incident` | 직접 접속이 없어도 운영 근거와 지원 영향에는 gate가 필요합니다 |
| 정책, 고지, 보관, 삭제, 동의, 규제 데이터 기획 | `high_risk` + `regulated_data_or_domain` | 법률 자문을 제공하지 않으면서 법무/컴플라이언스 검토 트리거를 드러내야 합니다 |

예시:

```json
{
  "mode": "plan",
  "governance": {
    "preset": "high_risk",
    "scenario_template": "auth_migration"
  }
}
```

## 리뷰 패널 (Review Panel)

작업을 구현, 릴리즈, 정책 공개, 고객-facing 커뮤니케이션으로 넘기기 전에 역할별 관점 검토가 필요하다면 review panel을 사용합니다. Prompt Builder는 모든 reviewer를 항상 켜지 말고 작업에 맞는 역할만 골라야 합니다.

v0.1에서는 이 내용을 optional contract schema field로 둡니다. 역할은 host-specific subagent 이름이 아니라 portable text로 유지합니다.

권장 역할:

- CTO Reviewer: 제품/기술 의사결정의 일관성, 구현 준비도, 복잡도 통제.
- Software Architect: 도메인 경계, 데이터 흐름, 상태 전이, 시스템 책임 분리, 설계 입력 누락.
- QA Engineer: 예외 케이스, acceptance criteria, 테스트 가능성, 운영 전 검증.
- Security / Privacy Reviewer: 인증, 권한, 개인정보, 로그, 마스킹, secret, abuse risk.
- Legal / Compliance Risk Screener: 약관, 고지, 책임 범위, 운영 리스크, 법률/컴플라이언스 리스크, 변호사 검토 필요 지점. 확정 법률 자문이나 컴플라이언스 승인은 하지 않음.
- Operations / CS Lead: 고객 응대, 장애 대응, 운영자 관점 명확성, 정책 설명 일관성.
- Product / Information Architecture Reviewer: 주제 구조, 결정 사항, 범위, 다음 액션, 문서 scanability.
- UX / Product Designer: 사용자 흐름, 문구, 접근성, 실수 방지, UI 결정 품질.
- Growth / Marketing Reviewer: 타깃 고객, 포지셔닝, 전환, 런칭 메시지, 가격/패키징 리스크.
- Data / Analytics Reviewer: 이벤트 설계, 지표, funnel, 실험 준비도.
- Finance / Unit Economics Reviewer: 비용, 마진, 가격, 환불, 보상 리스크.

권장 preset:

```text
implementation_review:
CTO Reviewer, Software Architect, QA Engineer, Security / Privacy Reviewer

production_incident:
CTO Reviewer, Software Architect, QA Engineer, Operations / CS Lead, Security / Privacy Reviewer

policy_or_customer_notice:
Legal / Compliance Risk Screener, Operations / CS Lead, Product / Information Architecture Reviewer, Growth / Marketing Reviewer

new_feature_planning:
CTO Reviewer, Product / Information Architecture Reviewer, UX / Product Designer, Growth / Marketing Reviewer, QA Engineer

docs_or_handoff:
Product / Information Architecture Reviewer, Operations / CS Lead, QA Engineer, CTO Reviewer
```

### 리뷰 행동 패턴

review panel을 worker prompt로 렌더링할 때는 각 reviewer 지시를 고정된 형식으로 짧고 반복 가능하게 작성합니다. 아래 항목은 새 contract field가 아니라 prompt 작성 가이드입니다. 대상과 허용/금지 행동은 task context, constraints, workspace strategy, infrastructure boundaries에서 가져옵니다.

```text
역할:
대상:
허용 행동:
금지 행동:
검토 관점:
산출물:
fact / inference 구분:
```

worker에게 reviewer 결과를 아래 표로 통합하게 합니다.

```text
역할 | 판정 | 핵심 근거 | 판정 반영 | 남은 리스크
```

`TIMELINE.md`는 같은 review pattern을 여러 작업에서 반복했을 때 남기는 optional local artifact로만 사용합니다. `.tools/project-prompt-kit/local/` 또는 git에서 제외된 로컬 작업 경로 아래에 두고, 필수 prompt contract field로 만들지 않습니다.

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
