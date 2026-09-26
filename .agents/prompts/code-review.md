# Code Review Agent Prompt Template

When reviewing code:
1. Ensure no hardcoded credentials, mock placeholders, or fake backend responses exist.
2. Check that inventory modifications use transactions and row-level locks.
3. Verify that all components meet UI wireframe guidelines and have loading/error states.
4. Verify tests exist and pass for new functionality.
5. Check type safety in Python (type hints) and TypeScript (strict types).
