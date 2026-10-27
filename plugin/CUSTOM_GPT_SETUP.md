# APF TODAY INSIGHT Editor — Custom GPT setup and acceptance checklist

## Current implementation stage
This repository branch contains the instruction pack and a read-only OpenAPI action for the public V2 feed. It is not a published ChatGPT plugin and does not itself provide image processing, web browsing, file execution, or Outlook send/receive verification.

## Configure the private Custom GPT
1. In ChatGPT, open Explore GPTs / Create (or the GPT editor available to your account) and create a private GPT named **APF TODAY INSIGHT Editor**.
2. Copy `plugin/APF_INSIGHT_EDITOR_INSTRUCTIONS.md` into the GPT Instructions field.
3. Add `plugin/openapi.yaml` as an Action schema if Actions are available in your workspace. The action is read-only and public; no API key is needed for this raw GitHub feed endpoint.
4. Upload these Knowledge files manually; repository files are not automatically attached to GPT Knowledge:
   - `references/operating-manual.md`
   - `references/v2-pilot.md`
   - `assets/master-vol019.html`
   - `references/original-verification.md`
   - `references/image-pipeline.md`
   - `references/source-image-separation.md`
   - `references/photo-book-policy.md`
   - `references/workflow.md`
   - `scripts/audit_html.py`
   - `scripts/audit_image_delivery.py`
   - selected prior issues / published and excluded ID ledgers
5. Enable web search/browsing and code/data-analysis capabilities if available. Test actual article-page opening and actual image-byte processing separately.
6. Keep the GPT private until every acceptance test below passes.

## Repository prerequisite gap
At the time this checklist was created, the default branch did not contain `references/` (the GitHub API returned 404 for that directory), so the two required documents and other references need to be committed or uploaded before the GPT can be fully configured. Never claim the GPT has read files that were not provided.

## Acceptance tests
- [ ] The action fetches current `data/latest.json` and displays both `edition_date` and `generated_at`.
- [ ] A stale feed is flagged, not treated as today's feed.
- [ ] Google News RSS links are not treated as publisher originals.
- [ ] Headline-only matches are excluded unless article body facts were checked.
- [ ] Duplicate-event checks use published/excluded ledgers and available issues; incomplete history is disclosed.
- [ ] Only `body_verified=true` stories appear in HTML cards.
- [ ] Article images are downloaded as bytes, decoded with Pillow, visually matched, and cropped/resized to master dimensions.
- [ ] Prior issue images and stale article URLs are absent from the candidate.
- [ ] The 美리보기 title, author, edition, cover, description, official link, and topical connection are freshly verified.
- [ ] Both audit scripts run and their actual outputs are retained.
- [ ] Desktop/mobile render checks are completed.
- [ ] Outlook delivery is marked unverified until a real test email and received EML/MIME are checked.

## Do not automate these without explicit approval
- Sending a newsletter email.
- Merging the feature branch into main.
- Publishing the GPT publicly.
