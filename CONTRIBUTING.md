# Contributing to Gonesis

Thanks for helping improve this skill. The repository is a set of instructions, so most changes are edits to Markdown.

## Ground rules

- Keep each operational rule in **one** owning reference file. Do not duplicate a rule across files; link to it instead. [`references/sources.md`](references/sources.md) lists which file owns which topic.
- When you change a rule, update the affected completion criteria and any navigation tables (`SKILL.md`, `references/README.md`).
- Keep `SKILL.md` short (well under 500 lines) and push detail into `references/`.
- Keep `references/requirement.txt` and `references/requirement.example.txt` aligned: same sections, same field names, and no unresolved `<answer>` in the example.
- Mark illustrative values as examples. Do not turn a sample answer into a default.
- Dependency evidence (versions, commits, symbols) must come from inspected source. Record it in `references/libraries.md` and `references/sources.md`, and do not claim runtime proof you did not run.
- Write command-line examples on a single line so they can be copied and pasted as-is.

## Before opening a pull request

Run the repository check:

```sh
python3 -I scripts/check_skill.py
```

It verifies the `SKILL.md` frontmatter and that every local Markdown link resolves inside the repository. CI runs the same check.

If you changed generated-service behavior (for example the Task rules), also try the skill on a real target and note the result in the pull request.

## Branches and commits

- Branch names: `<type>/<short-description>` in kebab-case. Types: `feat`, `fix`, `test`, `refactor`, `chore`, `ci`, `docs`.
- Commit messages: `<type>: <description>`, lowercase imperative, no trailing period, one logical change per commit.

## Reporting problems

Open an issue with the request you gave the agent, the `requirement.txt` (secrets removed), what the agent did, and what you expected instead.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
