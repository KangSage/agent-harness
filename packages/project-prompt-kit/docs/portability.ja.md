# Portability

Project Prompt Kit は private workspace, local-only framework, single agent host から独立している必要があります。

portable artifact:

- mode spec
- universal prompt contract
- renderer template
- sample output
- validation rule

host-specific adapter は存在してもよいですが、core contract を変えてはいけません。

public example では relative path と sanitized project name を使います。private username, local absolute path, access token, framework-specific runtime state を含めないでください。
