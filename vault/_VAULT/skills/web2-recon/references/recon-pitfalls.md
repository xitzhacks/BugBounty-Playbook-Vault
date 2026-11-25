# Recon Pitfalls — Session-Derived

## nuclei Timeout on Large Host Lists
- If you have 50+ live hosts, nuclei may take 10+ minutes and timeout
- Run nuclei in background: `terminal(background=true, notify_on_complete=true)`
- Or split host list into smaller chunks
- Or skip nuclei during initial recon, run later on curated list

## Parallel Shell Commands
- `gau` + `waybackurls` in parallel with `&` can cause terminal to refuse: "Foreground command uses '&' backgrounding"
- Use Python `concurrent.futures.ThreadPoolExecutor` instead

## Marionette Screenshot Capture
- `m.save_screenshot(path)` fails — needs file object:
  ```python
  with open(path, 'wb') as f:
      m.save_screenshot(f)
  ```
- Use `m.delete_session()` not `m.close_session()`
- JS `fetch()` in Marionette may return None (promise resolution issues in headless) — use curl for HTTP verification
