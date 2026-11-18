# Repository instructions

- Treat this clone as one independent Git mutation boundary.
- Preserve unrelated branches, worktrees, submodules, and dirty changes.
- Follow the repository's local documentation and source-owned contracts.
- Keep secrets, credentials, runtime state, caches, logs, and generated evidence
  out of version control.

## Verification

- Source checks: `just check`.
- Full source and retained-history check: `just verify`.
- The public contract validator can also run directly: `python3 cli-tools/validate_public_contracts.py`.
