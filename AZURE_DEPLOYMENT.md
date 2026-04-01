# Deployment Guide: FastAPI on Azure

This guide shows how to deploy your FastAPI application to Azure using Docker.

## Prerequisites

- Azure subscription (free account available)
- Azure CLI installed (`az` command)
- Docker installed locally
- Git installed
- Your Dockerfile is ready

## Architecture Options

### Option 1: Azure Container Instances (ACI) ⭐ Recommended for Simple Apps
- **Serverless containers**
- **Pay per second**
- **Simple to deploy**
- **Good for**: Dev/test, low traffic apps

### Option 2: Azure App Service
- **Fully managed**
- **Auto-scaling**
- **CI/CD integration**
- **Good for**: Production apps with scaling needs

### Option 3: Azure VM (EC2 Equivalent)
- **Full control**
- **Manual Docker management**
- **More complex**
- **Good for**: Complex requirements

---

## Option 1: Deploy with Azure Container Instances (ACI)

### Step 1: Create Azure Container Registry (ACR)

```bash
# Login to Azure
az login

# Create a resource group
az group create --name fastapi-ml-rg --location eastus

# Create container registry
az acr create --resource-group fastapi-ml-rg \
  --name fastapimlacrYOURNAME \
  --sku Basic

# Get login credentials
az acr credential show --name fastapimlacrYOURNAME
```

### Step 2: Build and Push Docker Image

```bash
# Build Docker image locally
docker build -t fastapi-ml:latest .

# Tag image for ACR
docker tag fastapi-ml:latest fastapimlacrYOURNAME.azurecr.io/fastapi-ml:latest

# Login to ACR
az acr login --name fastapimlacrYOURNAME

# Push image to ACR
docker push fastapimlacrYOURNAME.azurecr.io/fastapi-ml:latest

# View pushed images
az acr repository list --name fastapimlacrYOURNAME
```

### Step 3: Deploy to Azure Container Instances

```bash
# Create Azure Container Instance
az container create \
  --resource-group fastapi-ml-rg \
  --name fastapi-ml-container \
  --image fastapimlacrYOURNAME.azurecr.io/fastapi-ml:latest \
  --registry-login-server fastapimlacrYOURNAME.azurecr.io \
  --registry-username USERNAME \
  --registry-password PASSWORD \
  --dns-name-label fastapi-ml \
  --ports 80 \
  --environment-variables \
    MODEL_PATH=/app/model.pkl \
  --cpu 1 --memory 1

# Get public IP
az container show \
  --resource-group fastapi-ml-rg \
  --name fastapi-ml-container \
  --query ipAddress.fqdn
```

### Access Your App

```
https://fastapi-ml.eastus.azurecontainers.io:8000
API Docs: https://fastapi-ml.eastus.azurecontainers.io:8000/docs
```

---

## Option 2: Deploy with Azure App Service

### Step 1: Create App Service Plan

```bash
# Create app service plan
az appservice plan create \
  --name fastapi-ml-plan \
  --resource-group fastapi-ml-rg \
  --sku B1 \
  --is-linux

# Create web app for containers
az webapp create \
  --resource-group fastapi-ml-rg \
  --plan fastapi-ml-plan \
  --name fastapi-ml-app \
  --deployment-container-image-name fastapimlacrYOURNAME.azurecr.io/fastapi-ml:latest

# Configure container settings
az webapp config container set \
  --name fastapi-ml-app \
  --resource-group fastapi-ml-rg \
  --docker-custom-image-name fastapimlacrYOURNAME.azurecr.io/fastapi-ml:latest \
  --docker-registry-server-url https://fastapimlacrYOURNAME.azurecr.io \
  --docker-registry-server-user USERNAME \
  --docker-registry-server-password PASSWORD
```

### Step 2: Configure Environment Variables

```bash
# Set environment variables
az webapp config appsettings set \
  --resource-group fastapi-ml-rg \
  --name fastapi-ml-app \
  --settings \
    WEBSITES_PORT=8000 \
    WEBSITES_ENABLE_APP_SERVICE_STORAGE=false
```

### Step 3: Enable Continuous Deployment (Optional)

```bash
# Configure GitHub integration
az webapp deployment source config-zip \
  --resource-group fastapi-ml-rg \
  --name fastapi-ml-app \
  --src-path ./fastapi-ml.zip
```

### Access Your App

```
https://fastapi-ml-app.azurewebsites.net
API Docs: https://fastapi-ml-app.azurewebsites.net/docs
```

---

## Option 3: Deploy on Azure VM (EC2 Equivalent)

### Step 1: Create Azure VM

```bash
# Create VM
az vm create \
  --resource-group fastapi-ml-rg \
  --name fastapi-ml-vm \
  --image UbuntuLTS \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys

# Get public IP
az vm show \
  --resource-group fastapi-ml-rg \
  --name fastapi-ml-vm \
  --show-details \
  --query publicIps
```

### Step 2: SSH into VM and Install Docker

```bash
# SSH into VM
ssh azureuser@YOUR_PUBLIC_IP

# Update package manager
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose (optional)
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 3: Deploy Container on VM

```bash
# Login to ACR
az acr login --name fastapimlacrYOURNAME

# Pull image
docker pull fastapimlacrYOURNAME.azurecr.io/fastapi-ml:latest

# Run container
docker run -d \
  --name fastapi-ml \
  -p 80:8000 \
  -e MODEL_PATH=/app/model.pkl \
  fastapimlacrYOURNAME.azurecr.io/fastapi-ml:latest

# Check logs
docker logs fastapi-ml
```

### Step 4: Open Firewall Port

```bash
# Create network security group rule
az vm open-port \
  --resource-group fastapi-ml-rg \
  --name fastapi-ml-vm \
  --port 80 \
  --priority 1001
```

---

## Comparison Table: Which Option?

| Feature | ACI | App Service | VM |
|---------|-----|-------------|-----|
| **Ease of Setup** | ⭐⭐⭐⭐ Easy | ⭐⭐⭐ Medium | ⭐⭐ Hard |
| **Cost** | Pay per second | Pay per hour | Pay per hour |
| **Auto-scaling** | ❌ No | ✅ Yes | ❌ No |
| **CI/CD Integration** | ⭐⭐ Basic | ✅ Excellent | ⭐ Manual |
| **Control** | Limited | Medium | Full |
| **Best For** | Dev/Test | Production | Complex apps |
| **Startup Time** | Seconds | Minutes | Minutes |

---

## Useful Azure CLI Commands

```bash
# View all container instances
az container list --output table

# View logs
az container logs --resource-group fastapi-ml-rg --name fastapi-ml-container

# Stop container
az container stop --resource-group fastapi-ml-rg --name fastapi-ml-container

# Delete container
az container delete --resource-group fastapi-ml-rg --name fastapi-ml-container

# View app service logs
az webapp log tail --name fastapi-ml-app --resource-group fastapi-ml-rg

# Scale app service (auto-scale)
az appservice plan update --name fastapi-ml-plan --sku P1V2
```

---

## GitHub Actions CI/CD for Azure

Create `.github/workflows/deploy-azure.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Log in to Azure Container Registry
      uses: azure/docker-login@v1
      with:
        login-server: ${{ secrets.ACR_LOGIN_SERVER }}
        username: ${{ secrets.ACR_USERNAME }}
        password: ${{ secrets.ACR_PASSWORD }}
    
    - name: Build and push Docker image
      run: |
        docker build -t ${{ secrets.ACR_LOGIN_SERVER }}/fastapi-ml:latest .
        docker push ${{ secrets.ACR_LOGIN_SERVER }}/fastapi-ml:latest
    
    - name: Deploy to Azure Container Instances
      uses: azure/aci-deploy-action@v1
      with:
        resource-group: ${{ secrets.AZURE_RESOURCE_GROUP }}
        name: fastapi-ml-container
        image: ${{ secrets.ACR_LOGIN_SERVER }}/fastapi-ml:latest
        registry-login-server: ${{ secrets.ACR_LOGIN_SERVER }}
        registry-username: ${{ secrets.ACR_USERNAME }}
        registry-password: ${{ secrets.ACR_PASSWORD }}
        dns-name-label: fastapi-ml
        ports: 80
```

---

## Environment Variables & Secrets

```bash
# Set environment variables in Azure
az container create ... \
  --environment-variables \
    LOG_LEVEL=INFO \
    MODEL_PATH=/app/model.pkl

# Or in App Service
az webapp config appsettings set \
  --resource-group fastapi-ml-rg \
  --name fastapi-ml-app \
  --settings VARIABLE_NAME=value
```

---

## Monitoring & Logging

### View Logs

```bash
# ACI logs
az container logs --resource-group fastapi-ml-rg --name fastapi-ml-container

# App Service logs
az webapp log tail --name fastapi-ml-app --resource-group fastapi-ml-rg
```

### Enable Application Insights (Optional)

```bash
# Create Application Insights
az monitor app-insights component create \
  --app fastapi-ml-insights \
  --location eastus \
  --resource-group fastapi-ml-rg \
  --application-type web

# Link to App Service
az webapp config appsettings set \
  --resource-group fastapi-ml-rg \
  --name fastapi-ml-app \
  --settings APPINSIGHTS_INSTRUMENTATION_KEY=YOUR_KEY
```

---

## Cost Estimation

### Azure Container Instances (ACI)
- vCPU: ~$0.0135/hour
- Memory: ~$0.0015/GB/hour
- **Estimate**: ~$1-2/month for small app

### Azure App Service (B1 Plan)
- **Cost**: ~$12/month
- Includes 60 compute minutes

### Azure VM (Standard_B2s)
- **Cost**: ~$30-50/month

---

## Cleanup

```bash
# Delete all resources
az group delete --name fastapi-ml-rg
```

---

## Troubleshooting

### Container won't start
```bash
# Check logs
az container logs --resource-group fastapi-ml-rg --name fastapi-ml-container

# Get detailed info
az container show --resource-group fastapi-ml-rg --name fastapi-ml-container
```

### Authentication issues
```bash
# Verify ACR credentials
az acr credential show --name fastapimlacrYOURNAME

# Re-login to ACR
az acr login --name fastapimlacrYOURNAME
```

### Port issues
```bash
# Check open ports (VM)
az vm open-port --resource-group fastapi-ml-rg --name fastapi-ml-vm --port 8000
```

---

## Resources

- [Azure Container Instances Docs](https://learn.microsoft.com/en-us/azure/container-instances/)
- [Azure App Service Docs](https://learn.microsoft.com/en-us/azure/app-service/)
- [Azure CLI Reference](https://learn.microsoft.com/en-us/cli/azure/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/concepts/)

---

**Last Updated**: April 2024
