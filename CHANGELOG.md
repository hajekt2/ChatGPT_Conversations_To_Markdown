# Changelog

## 2026-02-26

### Added
- New config option: `extract_assets` (default `true`).
  - When `false`, converter skips copying image/audio assets.
  - Markdown output also removes asset embeds/links/references.

### Changed
- Conversation title handling now normalizes underscores to spaces for display.
- Markdown filename and first `#` header now stay in sync using the normalized `title`.
- YAML frontmatter no longer writes the `title` property.
- Setup wizard now writes `extract_assets: true` by default.
- `config.json.example` includes `extract_assets`.
