````md
# Local Validation

## Date

March 20, 2026

## Goal

Validate that the application and container work correctly in a local Docker environment before deploying to AWS.

---

## Environment Notes

Docker Desktop was installed and running, but the `docker` CLI was not initially available in the shell PATH.

Verified the Docker CLI directly:

```bash
/Applications/Docker.app/Contents/Resources/bin/docker --version
```

Added Docker to the PATH for the current session and all future sessions:

```bash
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Docker version confirmed:** `29.2.1, build a5c7197`

---

## App Files

```bash
cd ~/documents/aws-hosted-app
ls app
```

Files present in `./app`:

- `Dockerfile`
- `server.py`

---

## Steps

### 1. Build the image

```bash
docker build -t aws-hosted-app-local ./app
```

Build completed successfully. Image tagged as `aws-hosted-app-local` using base image `python:3.12-slim`.

### 2. Run the container

```bash
docker run --name aws-hosted-app-test -p 8080:8080 -d aws-hosted-app-local
```

### 3. Confirm the container is running

```bash
docker ps
```

```
CONTAINER ID   IMAGE                  COMMAND                CREATED          STATUS          PORTS                    NAMES
1d4bc4622aa3   aws-hosted-app-local   "python /app/server.…" 10 seconds ago   Up 10 seconds   0.0.0.0:8080->8080/tcp   aws-hosted-app-test
```

---

## Endpoint Validation

### `GET /`

```bash
curl -i http://localhost:8080/
```

```
HTTP/1.0 200 OK
Content-Type: text/plain

hello
```

✅ Pass

### `GET /health`

```bash
curl -i http://localhost:8080/health
```

```
HTTP/1.0 200 OK
Content-Type: text/plain

ok
```

✅ Pass

### `GET /notreal`

```bash
curl -i http://localhost:8080/notreal
```

```
HTTP/1.0 404 Not Found
```

✅ Pass

---

## Duplicate Container Name Behavior

A second `docker run` using the same container name (`aws-hosted-app-test`) failed as expected while the original container was still running:

```
docker: Error response from daemon: Conflict. The container name "/aws-hosted-app-test"
is already in use by container "1d4bc4622aa3...". You have to remove (or rename) that
container to be able to reuse that name.
```

To rerun, stop and remove the existing container first:

```bash
docker stop aws-hosted-app-test
docker rm aws-hosted-app-test
```

---

## What This Proves

- Docker is installed and usable after fixing the shell PATH.
- The image builds successfully from the current `Dockerfile`.
- The container starts and binds correctly to local port `8080`.
- `GET /` returns `200 hello` as expected.
- `GET /health` returns `200 ok` — ready for use as an ALB target group health check path.
- Invalid paths return `404` correctly.
- Local validation is complete, reducing the chance of conflating application-level issues with AWS networking, ECS, ALB, or target group configuration issues during deployment.
````