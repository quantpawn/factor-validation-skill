# factor-validation-skill

Codex skill for writing, validating, debugging, and interpreting third-party alpha factors against the hosted factor validation service.

## Main Entry

- `SKILL.md`

## What This Skill Covers

- writing a valid factor file
- submitting the factor to the validation API
- interpreting FastCheck metrics and failure stages
- fetching task logs for debugging

## Hosted Validation Service

- `https://factor-verifier-exp-21736345851.asia-southeast1.run.app`

UI:

- `https://factor-verifier-exp-21736345851.asia-southeast1.run.app/factor/verify/ui`

## Skill Layout

- `SKILL.md`
- `references/`
- `examples/`
- `scripts/`

## Install

For third-party agents that support direct GitHub skill installation:

```bash
npx codex-skill install https://github.com/quantpawn/factor-validation-skill
```

If the agent expects a git URL instead of an HTTPS repo URL:

```bash
npx codex-skill install git+https://github.com/quantpawn/factor-validation-skill.git
```

## Update

To get the latest version, reinstall the skill from the same GitHub URL:

```bash
npx codex-skill install https://github.com/quantpawn/factor-validation-skill --force
```

If your agent provides an `update` or `upgrade` command, you can use that instead.

## Notes

This repo is intended to be installed or copied as a Codex skill. The top-level agent instructions live in `SKILL.md`.
