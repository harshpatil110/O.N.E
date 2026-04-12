---
title: "Coding Standards and Style Guidelines"
category: "engineering"
applicable_roles: ["all"]
applicable_stacks: ["python", "node"]
applicable_levels: ["intern", "junior", "mid", "senior"]
last_updated: "2026-04-13"
---

# Coding Standards and Style Guidelines

Maintaining a uniform, highly readable codebase is essential for long-term velocity and developer happiness. Code is read infinitely more times than it is written. Therefore, we prioritize readability, predictability, and automated formatting over cleverness. This document outlines the stylistic dogmas for both our Python backends and robust JavaScript/TypeScript frontends.

## Automated Formatting Tooling

To completely eliminate bikeshedding over indentation and line spacing during code reviews, we enforce strict, automated formatters pre-commit.

### Python Environments
- **PEP 8 Compliance:** All standard PEP 8 guidelines apply. We rely on automation over human memory to enforce this.
- **Black:** The uncompromising code formatter. We use Black with a line length of 88 characters. If Black formats your code, leave it exactly as is—do not fight the tool.
- **isort:** We utilize `isort` configured with the Black profile (`--profile black`) to automatically sort and alphabetically group your imports at the top of every file.

### JavaScript and TypeScript Environments
- **Prettier:** Handles all spacing, quoting, and stylistic formatting.
- **ESLint:** Catches logical flaws, unused variables, and enforces best practices. 
Your IDE should be configured to run `eslint --fix` and `prettier` automatically upon saving any file.

## Naming Conventions
Variable names must be descriptive and unabbreviated. Avoid letters like `x`, `n`, or `data` unless used strictly as a brief loop index. 
- **Python:** Use `snake_case` for variables, modules, and functions. Use `PascalCase` strictly for Classes. Constant variables should be `UPPER_SNAKE_CASE`.
- **JavaScript/TypeScript:** Use `camelCase` for variables, methods, and functions. Use `PascalCase` for React components, interface definitions, and Classes.

## Documentation and Comments
Do not tell the reader *what* the code is doing; well-written code should be expressive enough to explain that. Write comments exclusively to explain *why* the code was written in a non-obvious way (e.g., addressing edge cases, API quirks, or obscure business logic constraints).
- **Python Docstrings:** Use the Google docstring format for all public functions, classes, and methods. Clearly define `Args:` and `Returns:` where complex structures are passed.
- **JS Docs:** Use JSDoc style comments directly above exported functions, React components, or complex hooks. 

## Cognitive Load and Function Length
We mandate modular, single-responsibility functions. 
- **Maximum Function Length:** Aim for under 30 lines of active logic per function. If a function or method exceeds 50 lines, it is almost certainly handling too many responsibilities and must be aggressively refactored into smaller, testable sub-routines.
- **Cyclomatic Complexity:** Avoid overly nested `if/else` ladders. Extract conditions to named variables or utilize early `return` / guard clauses at the top of the function.

Adherence to these standards is automatically evaluated by CI pipelines. PRs violating these conventions will be automatically blocked from merging.
