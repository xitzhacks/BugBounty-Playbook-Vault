---
title: "Container & kernel escape — worker escapes, ingress injection, runner policy, runc"
type: playbook
category: container-kernel-escape
cwe: "CWE-732"
source_count: 9
full_bodies_available: 9
corpus: "h1-brain disclosed_reports.db (3,673 rows), priv-esc bucket + module_map_all.json merges"
list_accessed: "2026-11-07"
note: "Anchors: PRIV-1382919 (ingress-nginx SA token, $2,500), PRIV-694181/697055 (LGTM symlinks, $2,000 each), PRIV-692603 (prepare-step root, $1,500). All 9 bodies read."
---

# Container & Kernel Escape — the boundary is the finding

## 1. Overview

Nine rows, **$10,600/6 paid** (3/9 carry no figure: the runc disclosure row, the EndpointSlice row, and the ingress-snippets row). The module is bimodal: three **worker/job escapes** (semmle LGTM ×3, $1,500–$2,000 each) where a worker container writes to the host through a symlink or package-install step, and six **orchestration rows** (kubernetes ×4, gitlab-runner ×1, ibb runc ×1) where the escape is a policy or configuration decision (an ingress annotation, a Docker socket, an EndpointSlice validator) rather than a memory bug. The DB weakness is uniform (9/9 `Privilege Escalation`). The module's price anchor is $2,500 (two kubernetes rows) — the corpus prices orchestration-layer privilege hops at cluster-admin reach, and worker-layer symlink reads at host-file-read reach ($2,000).

**Case-stock (9 rows / $10,600):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [PRIV-1382919](https://hackerone.com/reports/1382919) | kubernetes — https://github.com/kubernetes/ingress-nginx | ingress path injects nginx alias → service-account token | $2,500 |
| [PRIV-1842829](https://hackerone.com/reports/1842829) | kubernetes — https://github.com/kubernetes/kops | kOps GCE/GCP → cluster-admin + cloud instance create | $2,500 |
| [PRIV-694181](https://hackerone.com/reports/694181) | semmle — lgtm-com.pentesting.semmle.net | build.log symlink → host copy reads /etc/passwd | $2,000 |
| [PRIV-697055](https://hackerone.com/reports/697055) | semmle — lgtm-com.pentesting.semmle.net | lgtm.yml/.lgtm.yml symlink → host file read | $2,000 |
| [PRIV-692603](https://hackerone.com/reports/692603) | semmle — lgtm-com.pentesting.semmle.net | prepare-step package install → container root | $1,500 |
| [PRIV-1417211](https://hackerone.com/reports/1417211) | gitlab — https://gitlab.com/gitlab-org/gitlab-runner | docker-socket runner → host root (/etc/shadow) | $100 |
| [PRIV-495495](https://hackerone.com/reports/495495) | ibb — IBB (Legacy) | runc escape → host root (CVE-2019-5736) | - |
| [PRIV-1145044](https://hackerone.com/reports/1145044) | kubernetes — https://github.com/kubernetes/kubernetes | EndpointSlice holes → host-network hijack (CVE-2021-25737) | - |
| [PRIV-1249583](https://hackerone.com/reports/1249583) | kubernetes — https://github.com/kubernetes/ingress-nginx | ingress snippets (lua) → service-account token + proxy | - |

## 2. PRIV-1382919 and PRIV-1249583: the ingress-nginx token theft

The module's two kubernetes ingress rows are the same architectural flaw through two injection dialects, and the $2,500 paid row states the impact without shading:

> A user with the permissions to create an ingress resource can obtain the ingress-nginx service account token which can list secrets is all namespaces (cluster wide).

PRIV-1382919 reaches it by injecting an nginx `alias` into the controller's `nginx.conf` through an ingress `path` (`/gaf{alias /var/run/secrets/kubernetes.io/serviceaccount/;}location ~* ^/aaa`) — the path string is concatenated into the rendered config with no quoting. PRIV-1249583 (no figure) reaches the identical token through the *sanctioned* feature: the `configuration-snippet` / `server-snippet` annotations accept arbitrary Lua, and the body ships a `set_by_lua` snippet that reads `/run/secrets/kubernetes.io/serviceaccount/token` and serves it on a `/token` location. The same row adds the kube-apiserver proxy variant (`ExternalName` → `kubernetes.default`). The Doctrine: **the ingress controller's config-rendering path is a root shell over the cluster** — any string that lands in `nginx.conf` or in a Lua block is code, and the service-account token mounted in the pod is the first host file worth reading. The corpus prices the path-injection dialect at $2,500 and records the snippet dialect without a figure; the vault teaches them as one lane.

## 3. The LGTM worker escapes: symlinks across the container/host copy

PRIV-694181 (**$2,000**) is the worker-escape genome. The build worker runs in a container; after the job the host copies a log file out of the container; the copy follows symlinks *on the host*:

> Because lack of security, attacker will be able to remove original log file and replace it will a symlink to other file,

The body then shows the one-line attack: `rm -rf /opt/out/snapshot/log/build.log && ln -s /etc/passwd /opt/out/snapshot/log/build.log` — the host's copy reads the host's `/etc/passwd`. PRIV-697055 (**$2,000**, "[again]") is the same primitive through the config-file copy path: the worker processes `lgtm.yml` but keeps both `lgtm.yml` and `.lgtm.yml` in the output directory, so a symlink named `.lgtm.yml` pointing at a host file is copied with host content. PRIV-692603 (**$1,500**) is the container-root variant: the `prepare` step installs packages from source paths, so a malicious `.deb` planted in the source tree is installed as root inside the container, with a `postinst` backdoor (`setpasswd`) persisting it. The three rows teach the worker doctrine: **any file the worker writes that the orchestrator later reads as the host is an escape primitive**, and any step that installs worker-supplied packages is a container-root primitive. The $2,000 price is for host-file-read; the $1,500 price is for in-container root (no host reach demonstrated).

## 4. The remaining rows

PRIV-1842829 (kOps, **$2,500**) shows the cloud-credential endgame: a compromised kOps-managed GCE cluster yields cluster-admin, then the master-node service account's GCP role ("Kubernetes Engine Service Agent") yields arbitrary compute-instance creation — the body walks through shell-in-pod → metadata-token → `gcloud` instance creation with the token exfiltrated. PRIV-1417211 (GitLab runner, **$100**) is the Docker-socket policy row: the official Docker-in-Docker runner setup mounts `/var/run/docker.sock`, and any CI job can `docker run --privileged --volume /:/host ... cat /host/etc/shadow`. PRIV-495495 (runc, no figure) is the disclosure row: CVE-2019-5736 escapes Docker and Kubernetes containers to host root. Its body is a link card (blog post, PoC, Red Hat/AWS/GCP bulletins), not a technique — ranked as the module's most famous, least instructive row. PRIV-1145044 (EndpointSlice validation, no figure) closes the module with a validator hole: malformed EndpointSlice objects let a pod hijack host-network reach.

## 5. Cross-module notes

This module is the remote half of module 03. Module 03 is "the service runs as root and loads my file"; this module is "the orchestrator runs as root and copies my file" — same trust inversion, different scheduler. PRIV-1092859 (module 05) is the DNS-delegation cousin of the kOps row here.

## 6. What pays/what doesn't

- **Cluster reach prices at $2,500.** Both $2,500 rows reach cluster secrets or cloud compute beyond the cluster (ingress SA token → all-namespace secrets; kOps → GCP instances). The corpus prices reach, not elegance.
- **Host-file-read prices at $2,000.** The LGTM symlink rows demonstrate `/etc/passwd` from the host with a one-line `ln -s`. Same primitive, twice, same price.
- **In-container root without host reach prices lower ($1,500)** (692603), and **documented-by-design Docker-socket access prices at $100** (1417211) — the corpus distinguishes "the platform lets you" (cheap) from "the platform's copy path leaks" ($2,000) from "the platform hands cluster admin" ($2,500).
- **No-figure rows (3):** 495495 (link-only runc disclosure), 1145044 (EndpointSlice), 1249583 (snippets + token + proxy). The vault records them as figure-less, not unpaid; 1249583's full token-theft walkthrough at no figure is the module's sharpest reminder that figure-less ≠ low impact.

## 7. Cross-references

- Module 03 owns the local writable-path doctrine; this module owns the orchestration copy path. The playbook (PRIV-Testing-Agent-Playbook.md) P1 inventories job outputs, snippet annotations, and socket mounts together.
- PRIV-495495 is the Memory-Corruption vault's runc row; PRIV-1145044 (CVE-2021-25737) is its Kubernetes-validator sibling.
