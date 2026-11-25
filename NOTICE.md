# NOTICE

## Report content

The corpus indexes **publicly disclosed reports from HackerOne**. Each row carries the
canonical URL `https://hackerone.com/reports/<id>`. The write-up text, titles and
metadata are not relicensed by this repository; they remain the work of the reporters
and the programs that disclosed them, under HackerOne's disclosure terms.

This repository is a retrieval index over that public material, produced for security
research. Attribution is preserved in every search result (program, reporter, date,
URL). Removal requests: open an issue naming the report id.

## Redaction

Credentials, tokens, keys and email addresses found in the source material were replaced
with `[REDACTED_*]` markers before publication. FTS indexes were rebuilt and affected
chunks re-embedded. Reporter handles were kept as public attribution. See README.md
("Redaction") for the rule set and its limits.

## Code

`scripts/`, `tools/`, `setup.sh` — MIT, see LICENSE.
