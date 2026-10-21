# DeepSeek Search / Fetch

Official documentation checked 2026-10-21:

- [Guide, syntax, errors and billing](https://api-docs.deepseek.com/zh-cn/guides/search/)
- [Search schema](https://api-docs.deepseek.com/zh-cn/api/search)
- [Fetch schema](https://api-docs.deepseek.com/zh-cn/api/fetch)

These are standalone JSON tools; no model name, chat completion, Responses request, or model-provider switch is required. If these contracts stop working, reread the official documentation before changing the helper.

## Requests

Send `Content-Type: application/json` and `Authorization: Bearer <process DEEPSEEK_API_KEY>` over HTTPS, only to `api.deepseek.com`. Never forward this header to a page being fetched.

`POST https://api.deepseek.com/v1/tools/search`

```json
{"query":"Unity shader compilation site:github.com","count":5,"need_content":false}
```

- `query`: 1–128 Unicode characters, not all whitespace.
- `count`: 1–50, API default 10; helper default 5.
- `need_content`: boolean, API default false. True requests body text but does not guarantee it exists.
- Optional `ori_question`: original question, 1–128 characters, or null; helper supports `--ori-question`.
- Optional `localization`: IP address for localized prioritization; omitted by this helper.
- Query syntax: `site:`, `-site:`, `-keyword`, `-"phrase"`, `"exact phrase"`, `lang:zh,en`, `after:YYYY-MM-DD`, `before:YYYY-MM-DD`; multiple sites can use `site:github.com OR site:reddit.com`.

Success is `{"results":[...]}`. Each result includes `title`, `url`, `snippet`, `summary`, `content`, `date`, `site_name`, `site_icon`, `rerank_score`, `authority`. An empty array means no matches. `content` is empty if not requested or unavailable. `date` may be null; do not invent a publication date. Summary text is not a verbatim page body. Ranking and authority scores are provider metadata, not independent verification.

`POST https://api.deepseek.com/v1/tools/fetch`

```json
{"url":"https://api-docs.deepseek.com/zh-cn/guides/search/"}
```

URL must be HTTP/HTTPS with a host, no username/password, at most 8192 characters. Success is `{"title":"...","content":"Markdown body"}`. Target availability and site policy still apply; the API does not promise all comments, media, scripts, or private content.

## Failures and cost

Errors have an `error` object. Distinguish 400 invalid requests, 401 invalid/missing key, 402 insufficient balance, 403 Fetch safety rejection, 404 Fetch unavailable/unextractable content, 408 timeout, 413 oversized request, 429 rate limit, and 5xx upstream/server errors. Correct requests before retrying non-transient 4xx responses. Fetch 403 is not automatically an authentication failure.

The helper does at most two retries for 408/429/5xx and network timeouts. It reports `Retry-After` when waiting would exceed 60 seconds. A failed/empty request must not be described as successful research.

Search and Fetch use per-successful-request billing; count is not a per-result fee. Consult the current guide for rates and effective dates rather than assuming free access or copying a stale price. No recursive crawl or automatic fetching of every search result is included.

## Local validation, 2026-10-21

- Search `site:github.com/mrdoob/three.js Timer`, count 3: PASS; returned a relevant Timer migration PR, FixedTimer commit, and Timer issue. Body text was not requested.
- Search `Unity shader compilation site:reddit.com` and refinement `DeepSeek site:reddit.com`, count 3, body requested: both EMPTY. This does not prove Reddit is universally unavailable; it does mean this test did not validate Reddit coverage.
- Fetch `https://api-docs.deepseek.com/zh-cn/guides/search/`: PASS; returned the expected title and substantive Markdown documenting both endpoints.

These small probes verify the configured endpoints, not complete discussion coverage or guaranteed future availability.
