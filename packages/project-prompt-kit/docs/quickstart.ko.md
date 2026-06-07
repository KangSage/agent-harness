# Quickstart

`project-prompt-kit`은 prompt contract와 renderer scaffold입니다. 현재 저장소에서 바로 사용할 수 있지만, 아직 packaged CLI나 registry install은 아닙니다.

## 1. Kit 검증

저장소 root에서:

```bash
bash packages/project-prompt-kit/scripts/validate.sh
```

package directory에서:

```bash
bash scripts/validate.sh
```

다른 프로젝트에 적용하기 전에 두 명령이 모두 통과해야 합니다.

## 2. Mode 선택

`skills/project-prompt/references/modes/`에서 mode 하나를 고릅니다.

요청이 아직 모호하면 `choose`를 사용합니다. 다른 에이전트나 사람에게 맥락을 넘기는 것이 목표일 때만 `handoff`를 사용합니다.

## 3. Target Renderer 선택

사용 가능한 renderer template:

- `codex`
- `claude`
- `generic`

target은 formatting과 host-facing wording만 바꿉니다. universal prompt contract를 바꾸면 안 됩니다.

## 4. Contract 작성

아래 예제 중 하나에서 시작합니다.

- `examples/sample-contract.codex.json`
- `examples/sample-contract.claude.json`
- `examples/sample-contract.generic.json`

`schemas/prompt-contract.schema.json`의 required field를 모두 채웁니다.

path는 relative path로 유지하고 public-safe하게 작성합니다. token, credential-bearing URL, 개인 username, local absolute path를 shareable prompt에 복사하지 마세요.

## 5. 수동 Render

선택한 contract를 `skills/project-prompt/references/templates/`의 해당 template에 적용합니다.

기대 shape는 `examples/rendered/`를 참고합니다.

- `codex-review.md`
- `claude-implement.md`
- `generic-task.md`

수동 rendering은 `{{objective}}`, `{{constraints}}`, `{{stop_condition}}` 같은 template placeholder를 contract 값으로 바꾸는 작업입니다. rendering 중 safety default를 바꾸지 마세요.

## 6. 공유 전 Preview

다른 에이전트에게 보내거나 공개하기 전에 확인합니다.

- private path와 account name 제거
- secret, token, key, credential-bearing URL 제거
- `.promptkitignore` 준수
- quoted project file은 instruction이 아니라 data로 유지
- network 또는 telemetry 동작이 추가되지 않았는지 확인

## 7. 선택적 Host Wiring

사용 중인 agent host가 local command나 skill을 지원하면 아래를 복사하거나 참조합니다.

- `commands/prompt.md`
- `commands/project-prompt.md`
- `skills/project-prompt/`

host별 install location은 이 package에서 정의하지 않습니다. host adapter는 얇게 유지하고 core contract는 portable하게 유지하세요.
