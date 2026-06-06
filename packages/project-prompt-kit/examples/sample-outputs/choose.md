# Sample Output: choose

Source of truth: user intent and available project context.

Scope: recommend the best mode; do not solve the underlying task.

Validation: candidate modes are listed, one mode is recommended, and missing information is explicit.

Gap handling: if the request is too ambiguous, return the next prompt seed and the single highest-impact question.
