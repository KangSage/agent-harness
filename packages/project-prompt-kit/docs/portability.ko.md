# Portability

Project Prompt Kit은 private workspace, local-only framework, single agent host와 독립적이어야 합니다.

portable artifact:

- mode spec
- universal prompt contract
- renderer template
- sample output
- validation rule

host-specific adapter는 존재할 수 있지만 core contract를 바꾸면 안 됩니다.

public example은 relative path와 sanitized project name을 사용해야 합니다. private username, local absolute path, access token, framework-specific runtime state를 포함하지 마세요.
