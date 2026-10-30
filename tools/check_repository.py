#!/usr/bin/env python3
"""Check staged/tracked source only; never print matched secret or diary content.

Run after git add. This is a guardrail, not an exhaustive secret scanner.
Reading the index also catches force-added files ignored by .gitignore.
"""
from pathlib import Path, PurePosixPath
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


TOKEN_PATTERNS = [
    rb'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----',
    rb'\bgh[pousr]_[A-Za-z0-9]{20,}\b',
    rb'\bgithub_pat_[A-Za-z0-9_]{20,}\b',
    rb'\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}\b',
    rb'\bAKIA[A-Z0-9]{16}\b',
    rb'\bxox[baprs]-[A-Za-z0-9-]{20,}\b',
    rb'''(?i)(?:api[_-]?key|access[_-]?token|password|client[_-]?secret)\s*[=:]\s*["'][A-Za-z0-9_+/.=-]{16,}["']''',
]
PRIVATE_PARTS = {'private', 'data', 'backups', 'exports', 'captures', '.gradle', '.idea', 'node_modules', 'build'}
PRIVATE_NAMES = {'local.properties', 'key.properties', 'keystore.properties', 'secrets.properties', 'credentials.json', 'google-services.json', '.envrc'}
PRIVATE_SUFFIXES = {'.db', '.sqlite', '.sqlite3', '.keystore', '.jks', '.p12', '.pfx', '.pem', '.key', '.der', '.cer', '.log', '.apk', '.aab', '.zip', '.bundle', '.hprof'}


def problems(path, mode, data):
    p = PurePosixPath(path)
    lower = p.name.lower()
    failures = []
    if mode != '100644' and mode != '100755':
        failures.append('symlink/submodule requires separate review')
    if (set(part.lower() for part in p.parts) & PRIVATE_PARTS or lower in PRIVATE_NAMES
            or (lower.startswith('.env') and lower != '.env.example')
            or p.suffix.lower() in PRIVATE_SUFFIXES
            or re.search(r'\.(?:db|sqlite|sqlite3)-(?:wal|shm|journal)$', lower)
            or '未言备份' in lower or ('weiyan' in lower and 'backup' in lower)):
        failures.append('private data, credential or generated-file path')
    if len(data) > 2 * 1024 * 1024:
        failures.append('file above 2 MiB requires separate review')
    if b'\0' in data:
        failures.append('binary content requires separate review')
    for pattern in TOKEN_PATTERNS:
        if re.search(pattern, data):
            failures.append('possible secret')
            break
    text = data.decode('utf-8', errors='replace')
    if re.search(r'data:image/[^;\s]+;base64,[A-Za-z0-9+/=]{40,}', text):
        failures.append('embedded image payload requires separate review')
    if p.suffix.lower() == '.json':
        try:
            obj = json.loads(text)
            if isinstance(obj, dict) and (obj.get('format') == 'WEIYAN_LOCAL_BACKUP' or isinstance(obj.get('notes'), list)):
                failures.append('possible diary export')
        except ValueError:
            pass
    if path == 'prototypes/mobile-m1/index.html':
        if re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon)\s*\(', text):
            failures.append('prototype network capability requires explicit authorization review')
        if re.search(r'''(?:src|href|action)\s*=\s*["']\s*(?:https?:)?//''', text, re.I):
            failures.append('remote resource in offline prototype')
    return failures


def main():
    entries = git('ls-files', '--stage', '-z').split(b'\0')
    failures = 0
    checked = 0
    for entry in entries:
        if not entry:
            continue
        metadata, raw_path = entry.split(b'\t', 1)
        mode, oid, stage = metadata.decode().split()
        path = raw_path.decode('utf-8')
        if stage != '0':
            found = ['unresolved merge conflict']
        else:
            found = problems(path, mode, git('cat-file', 'blob', oid))
        checked += 1
        for reason in found:
            # Only the path and reason are shown, never matching source content.
            print(f'BLOCK: {path}: {reason}', file=sys.stderr)
            failures += 1
    print(f'Checked {checked} index entries; {failures} finding(s).')
    return int(failures != 0)


if __name__ == '__main__':
    sys.exit(main())
