# 🧰 CaseForge

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](VERSION)
[![Python](https://img.shields.io/badge/python-3.9%2B-yellow)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Linux-informational)](#-scope)
[![CI](https://github.com/Tinytim695/case-forge/actions/workflows/quality.yml/badge.svg)](https://github.com/Tinytim695/case-forge/actions/workflows/quality.yml)
[![License](https://img.shields.io/badge/license-MIT-informational)](LICENSE)

**A local-first Linux incident-response and forensic case builder.**

CaseForge turns controlled host observations into a portable, hashed evidence bundle. It is designed to sit above small focused tools such as ShellSieve, TraceLock and DNAProcess.

## 🧭 Workflow

~~~text
caseforge new incident-001
        │
        ▼
caseforge collect incident-001
        │
        ├── system
        ├── process
        ├── network
        ├── users
        └── persistence
        │
        ▼
caseforge timeline incident-001
caseforge ioc incident-001 iocs.txt
caseforge report incident-001
caseforge verify incident-001
caseforge export incident-001 -o incident-001.zip
~~~

## 🔍 Collectors

| Module | Collects |
|---|---|
| 'system' | OS release, kernel, architecture, uptime estimate |
| 'process' | PID/PPID, state, IDs, threads, command line, executable hash, namespaces |
| 'network' | local TCP/UDP sockets and listening endpoints from '/proc/net/' |
| 'users' | passwd/group metadata without password hashes |
| 'persistence' | selected cron, systemd, init, shell-profile and SSH key-file metadata |
| 'filesystem' | metadata for recently modified files under paths you explicitly supply |
| 'logs' | last N lines from paths you explicitly supply or common Linux log paths |

Collection is explicit. Filesystem collection does **not** recursively scan the whole disk unless you supply a path, and no collector makes network requests.

## 🔐 Evidence integrity

Every evidence artifact gets:

- UTC collection timestamp
- schema and module context
- byte size
- SHA-256

'verify' recalculates hashes and never reruns collection.

'export' creates a ZIP containing the case, evidence and 'SHA256SUMS'.

## 🕰️ Timeline

Collectors emit timestamped events where available. 'timeline' combines them with artifact-collection events and sorts them chronologically.

## 🎯 IOC triage

Create a plain-text IOC file with one value per line:

~~~text
203.0.113.10
example.test
https://example.test/path
person@example.test
0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
~~~

Run:

~~~bash
caseforge ioc incident-001 iocs.txt
~~~

IOC scanning is against the **local evidence already collected**. There is no automatic reverse lookup, DNS lookup, URL fetch or cloud enrichment.

## 📝 Reports

'caseforge report' generates a Markdown report with case metadata, collection summary, listening sockets, evidence hashes and IOC matches.

## 🧩 Relationship to the other tools

CaseForge is intended to be the case/evidence layer. It can consume or sit alongside outputs from:

- **ShellSieve** for shell-history analysis
- **TraceLock** for command execution records
- **DNAProcess** for process snapshots

The current release keeps those integrations file-based and optional.

## Installation

~~~bash
git clone https://github.com/Tinytim695/case-forge.git
cd case-forge
chmod +x caseforge
sudo install -m 0755 caseforge /usr/local/bin/caseforge
~~~

Then:

~~~bash
caseforge --version
caseforge new incident-001
~~~

## Scope

Linux '/proc' is required for process/network collection. Some host fields depend on permissions.

Use only on systems, processes, files and logs you are authorised to inspect and retain.

## License

MIT
