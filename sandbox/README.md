# PyClimb Sandbox

This directory contains the Docker-based sandbox for executing untrusted code.

## Building the Sandbox Image

```bash
cd sandbox
docker build -t pyclimb-sandbox .
```

## How It Works

When sandbox mode is enabled (`PYCLIMB_USE_SANDBOX=true`), the judge:

1. Creates a temporary directory with the user's code
2. Runs a Docker container with strict security constraints
3. Mounts the code directory as read-only
4. Captures stdout/stderr
5. Destroys the container after execution

## Security Features

| Feature | Implementation |
|---------|----------------|
| **No network** | `--network none` |
| **Memory limit** | `--memory 128m` |
| **CPU limit** | `--cpus 0.5` |
| **Read-only filesystem** | `--read-only` |
| **Non-root user** | Container runs as `runner` user |
| **Dropped capabilities** | `--cap-drop ALL` |
| **No privilege escalation** | `--security-opt no-new-privileges` |
| **Timeout** | External `timeout` command |

## Testing the Sandbox

```bash
# Test basic execution
echo 'print("hello")' > /tmp/test.py
docker run --rm \
  --network none \
  --memory 128m \
  --cpus 0.5 \
  --read-only \
  --tmpfs /tmp:size=10m \
  --security-opt no-new-privileges \
  --cap-drop ALL \
  -v /tmp/test.py:/sandbox/code.py:ro \
  pyclimb-sandbox \
  timeout 5 python3 /sandbox/code.py

# Test network is blocked
echo 'import urllib.request; urllib.request.urlopen("https://example.com")' > /tmp/net.py
docker run --rm --network none -v /tmp/net.py:/sandbox/code.py:ro pyclimb-sandbox timeout 5 python3 /sandbox/code.py
# Should fail with network error

# Test filesystem is read-only
echo 'open("/evil.txt", "w").write("pwned")' > /tmp/write.py
docker run --rm --read-only -v /tmp/write.py:/sandbox/code.py:ro pyclimb-sandbox timeout 5 python3 /sandbox/code.py
# Should fail with read-only filesystem error
```

## Configuration

Set these environment variables in your `.env` or Django settings:

```
PYCLIMB_USE_SANDBOX=true          # Enable Docker sandbox
PYCLIMB_SANDBOX_IMAGE=pyclimb-sandbox  # Docker image name
PYCLIMB_SANDBOX_TIMEOUT=5         # Timeout in seconds
PYCLIMB_SANDBOX_MEMORY=128m       # Memory limit
PYCLIMB_SANDBOX_CPUS=0.5          # CPU limit
```

## Known Limitations

1. **Docker required**: The host must have Docker installed and running
2. **Docker socket access**: Django process needs access to Docker socket
3. **Overhead**: ~100-200ms overhead per container startup
4. **No GPU support**: GPU problems would need additional configuration

## Fallback Behavior

If Docker is not available or sandbox mode is disabled, the runner falls back to
the original subprocess-based execution. This is fine for development but
**not safe for production with untrusted users**.
