# APF TODAY INSIGHT Plugin — setup and acceptance checklist

## Purpose
Prepare a review-only APF TODAY INSIGHT newsletter from the GitHub V2 candidate feed. This repository contains a starter plugin manifest, editor instructions, and a read-only OpenAPI feed action. These files do not by themselves prove that a plugin is installed, published, or executable in ChatGPT.

## Current implementation limits
- `plugin/openapi.yaml` reads only the public `main/data/latest.json` feed. It does not fetch publisher article bodies, verify image bytes, generate/crop images, run local Python scripts, render HTML, or send Outlook email.
- Editorial verification, image handling, HTML editing, and audit steps require capabilities/tools that are actually available in the active ChatGPT plugin runtime.
- Never describe an unavailable tool or untested feature as working.
- Never send an email or merge/publish changes without the user's explicit approval.

## Current design authority
- Use `assets/master-current.html` as the current approved design baseline.
- Use `references/design-current.md` for the current design rules.
- Do not revert to the historical VOL.019 design. Any legacy VOL.019 file is compatibility material only.
- If either current design file is missing from the branch or unavailable to the runtime, stop short of claiming design-compliant HTML has been generated; use only the supplied files and explicitly flag the missing dependency.

## Setup
1. Open the ChatGPT Plugins page and choose **Add → Create plugin**.
2. Follow the plugin creator's prompts. Provide the repository URL: https://github.com/jyttang94-max/apf-today-insight-v2
3. Ask it to inspect and reuse:
   - `plugin/plugin.json`
   - `plugin/APF_INSIGHT_EDITOR_INSTRUCTIONS.md`
   - `plugin/openapi.yaml`
   - `references/design-current.md`
   - `assets/master-current.html`
   - verification and image-audit scripts, when present and executable
4. Keep the plugin private while testing.
5. Confirm which repository files were actually imported and which tools the plugin can actually call. Do not assume a GitHub repository is automatically loaded as knowledge.

## Acceptance tests
- [ ] Latest feed fetch succeeds and shows `edition_date`, `generated_at`, `articles`, and `errors`.
- [ ] Stale feed is flagged, never silently treated as current.
- [ ] Google News RSS is not treated as an original publisher article.
- [ ] Only articles whose actual body facts were checked are included.
- [ ] Event-level duplicates are checked against available published/excluded ledgers and previous issues; missing history is disclosed.
- [ ] Image source, file bytes, decoded format, dimensions, article match, rights status, and embedding are recorded.
- [ ] HTML follows the current master, contains no stale article links/images, and preserves Outlook table layout.
- [ ] Available audit scripts actually run and outputs are retained.
- [ ] Desktop/mobile rendering is checked where tools permit.
- [ ] Outlook delivery remains unverified until a real received message and EML/MIME are inspected.

## Do not claim without evidence
Plugin installation, publication, tool connectivity, web article verification, image processing, audit execution, browser rendering, and Outlook delivery must each be marked verified only after the corresponding test passes.
