# APF TODAY INSIGHT Editor — setup

This folder contains the workflow specification for a ChatGPT-based APF TODAY INSIGHT editorial assistant.

## What this is
- A version-controlled instruction pack for a Custom GPT or equivalent agent workflow.
- It defines live-feed retrieval, source-body verification, duplicate checks, image acquisition/validation, approved HTML template handling, and pre-delivery audits.
- It is **not** a published or installed ChatGPT plugin, and does not itself create a runnable web service.

## Configure a Custom GPT
1. In ChatGPT, open the GPT builder and create a private GPT named **APF TODAY INSIGHT Editor**.
2. Paste the contents of `APF_INSIGHT_EDITOR_INSTRUCTIONS.md` into its Instructions field.
3. Upload the operating manual, pilot guide, approved `assets/master-vol019.html`, relevant reference files, audit scripts, and example prior issues as Knowledge/files. Do not assume a GitHub branch makes these files available to the GPT's Knowledge automatically.
4. To fetch `data/latest.json` live, enable an available GitHub connector/action with read access to this repository, or configure an authenticated Action/API endpoint. Verify each run actually fetches the current file.
5. For public web article verification and image inspection, ensure browsing and any required file/image processing tools are enabled. If those tools are unavailable, the assistant must report the gap and not mark the task verified.
6. Keep the GPT private until the source-verification, image, and audit workflow has been tested end-to-end.

## Required acceptance tests before operational use
- The assistant reads the manual and pilot guide at the start; missing files are reported.
- It fetches live `data/latest.json` and reports `generated_at` and fetch time.
- A Google News RSS URL alone never counts as an original source.
- A headline match without article-body verification is excluded.
- Same-event reprints are detected where historical data is available.
- No stale master article URLs or Base64 images survive in generated HTML.
- Verified image bytes are downloaded, decoded, visually matched, cropped/resized to the correct slot, and audited.
- The 美리보기 book metadata, cover, description, official link, and topical connection are refreshed and verified.
- Output includes the review HTML, article verification log, image log, and audit report.
- The assistant never claims Outlook delivery without an actual send/receive test and EML/MIME verification.

## Repository state and limitations
The specification was added on branch `feature/apf-insight-chatgpt-plugin`. This does not publish a plugin or change the default branch. Before using this as an operational workflow, reconcile the instructions with the repository's actual reference files and test the full process.
