# 🐳 Installing Docker and Running Redis on Docker

## 1. Install Docker

### **On macOS**

1. Go to [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/).
2. Download and install the `.dmg` file.
3. Open Docker Desktop and wait for it to start (you’ll see the whale icon in the menu bar).
4. Verify installation:

   ```bash
   docker --version
   ```

### **On Windows**

1. Download **Docker Desktop for Windows** from [docker.com](https://www.docker.com/products/docker-desktop/).
2. Run the installer and follow the setup wizard (enable WSL2 integration if prompted).
3. After installation, open Docker Desktop.
4. Verify:

   ```bash
   docker --version
   ```

### **On Linux (Ubuntu example)**

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo systemctl enable --now docker
docker --version
```

---

## 2. Install and Run Redis in Docker

### **Step 1: Pull the Redis Image**

```bash
docker pull redis
```

### **Step 2: Run Redis Container**

Run Redis in the background and expose the default port (6379):

```bash
docker run -d --name redis-server -p 6379:6379 redis
```

### **Step 3: Verify It’s Running**

```bash
docker ps
```

You should see a container named **redis-server**.

### **Step 4: Connect to Redis CLI**

```bash
docker exec -it redis-server redis-cli
```

Then try:

```bash
ping
```

You should get:

```
PONG
```

---

## 3. Optional: Persistent Redis Data

If you want data to persist even when the container stops:

```bash
docker run -d --name redis-server -p 6379:6379 -v redis-data:/data redis redis-server --save 60 1
```

> This mounts a Docker volume `redis-data` to store Redis data files.

---

## 4. Stop and Remove the Container

```bash
docker stop redis-server
docker rm redis-server
```
