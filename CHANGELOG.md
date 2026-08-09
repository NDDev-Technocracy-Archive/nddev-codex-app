# Changelog

All notable changes to `nddev-codex-app` are documented here.

## [0.2.0] - 2026-08-09

- Add the capability-negotiated public provider protocol v3 with exact
  HarnessBundle validation, pure plans, post-lock target revalidation,
  target-bound backups, rollback, and durable component/bundle/plan provenance.
- Separate the canonical `nddev` content setup identity from `safe` and
  `full-auto` permission profiles while retaining the previous `--setup`
  spellings as bounded compatibility aliases and reading schema-v1 stamps.
- Correct the README manager version and preserve the public repository's
  local-validation-only boundary.
- Add durable prepared/committed recovery, exact projection-kind negotiation,
  and pre-plan TOML/skill-tree validation without reapplying uncertain effects.

## [0.1.3] - 2026-08-08

- Update the pinned stable Codex CLI from `0.146.1` to `0.147.0` and refresh
  the official package checksum manifest plus all four supported archives.
- Revalidate the unchanged top-level config schema, native plugin lifecycle,
  and permission profiles. The removed `codex exec --full-auto` compatibility
  flag is not used by this manager; full-auto remains a native config posture.

## [0.1.2] - 2026-08-06

- Update the pinned stable Codex CLI from `0.146.0` to `0.146.1`.
- Re-verify the unchanged official standalone installer identity and current
  configuration/checker surfaces; upstream reports one safer automatic-review
  defaults bug fix and no format migration.

## [0.1.1] - 2026-07-30

- Included the repository instruction and Claude compatibility bridge closure
  in both source and runtime release archives so extracted validation remains
  self-contained.

## [0.1.0] - 2026-07-24

Pre-release baseline. Version scheme realigned across the nddev setup modules:
`0.1.0` reflects that the `nddev-builder` tooling — the setup system for
building setups — is ready, while the working setups themselves are not yet
shipped. `1.0.0` is reserved for the first working setups.

- Codex setup manager (`cli-tools/nddev_codex.py`) with target-explicit
  lifecycle and the co-owned `config.toml` ownership model.
- Native `nddev-builder` marketplace and plugin, including the config,
  requirements, and artifact checkers.
- Checkers and runtime pinned to the official Codex CLI `0.145.0`
  (`rust-v0.145.0`); the standalone `install.sh` installer and the
  per-platform package archives are verified against the official
  `codex-package_SHA256SUMS` manifest.
