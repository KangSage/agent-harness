# agent-harness

[English](./README.md) | [한국어](./README.ko.md) | [日本語](./README.ja.md)

`agent-harness`는 코딩 에이전트/프로젝트 에이전트용 재사용 가능한 구성요소를 모아두는 공개 모노레포입니다.

## 목표
- 프롬프트 킷, 슬래시 커맨드, 워크플로 템플릿, 검증 도구, 예제, 안전 패턴을 재사용 가능하게 정리합니다.
- Codex, Claude, 일반 렌더러에서 공통으로 쓸 수 있도록 호스트 중립 계약을 유지합니다.
- 기본값은 안전 우선입니다: 로컬 우선 동작, 텔레메트리 비활성, 민감정보 레다크션, 프롬프트 경계 명시.

## 모노레포 구조
- `docs/` — 원칙, 아키텍처, 로드맵
- `packages/project-prompt-kit/` — 첫 패키지 스캐폴드(`v0.1`)
- `.github/workflows/validate.yml` — 스캐폴드 검증 CI

## 첫 패키지: `project-prompt-kit`
첫 패키지는 가볍고 호스트 중립적인 프롬프트 킷의 시작점을 제공합니다.

명령 계약:
- 기본 명령: `/prompt`
- 정식 별칭: `/project-prompt`

참고: [`packages/project-prompt-kit/README.md`](./packages/project-prompt-kit/README.md)

## 빠른 검증
```bash
bash packages/project-prompt-kit/scripts/validate.sh
```

## 라이선스
MIT — [`LICENSE`](./LICENSE) 참고.
