# 🚀 Multi-Language RAG System - Deployment Guide

This guide will help you deploy your Multi-Language RAG System to make it live and accessible from anywhere.

## 📋 Prerequisites

1. **Groq API Key**: Make sure you have your Groq API key ready
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)

## 🌐 Deployment Options

### Option 1: Railway (Recommended - Easiest)

**Railway** is the easiest option with a generous free tier.

#### Steps:
1. **Sign up** at [railway.app](https://railway.app)
2. **Connect your GitHub** repository
3. **Create a new project** and select your repository
4. **Add environment variable**:
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key
5. **Deploy** - Railway will automatically detect and deploy your app

#### Benefits:
- ✅ Free tier available
- ✅ Automatic deployments
- ✅ Easy environment variable management
- ✅ Built-in monitoring

---

### Option 2: Render (Free Tier Available)

**Render** offers a free tier and is very reliable.

#### Steps:
1. **Sign up** at [render.com](https://render.com)
2. **Connect your GitHub** repository
3. **Create a new Web Service**
4. **Configure**:
   - **Name**: `multilingual-rag-system`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. **Add environment variable**:
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key
6. **Deploy**

#### Benefits:
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy scaling
- ✅ Good performance

---

### Option 3: Heroku

**Heroku** is a classic choice for Python apps.

#### Steps:
1. **Install Heroku CLI** and login
2. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```
3. **Set environment variable**:
   ```bash
   heroku config:set GROQ_API_KEY=your_api_key_here
   ```
4. **Deploy**:
   ```bash
   git push heroku main
   ```

#### Benefits:
- ✅ Well-established platform
- ✅ Good documentation
- ✅ Multiple add-ons available

---

### Option 4: Docker + Cloud Platforms

#### Using Docker with any cloud platform:

1. **Build Docker image**:
   ```bash
   docker build -t multilingual-rag .
   ```

2. **Run locally**:
   ```bash
   docker run -p 8001:8001 -e GROQ_API_KEY=your_key multilingual-rag
   ```

3. **Deploy to cloud platforms**:
   - **Google Cloud Run**
   - **AWS ECS/Fargate**
   - **Azure Container Instances**
   - **DigitalOcean App Platform**

---

### Option 5: VPS (Virtual Private Server)

#### Steps:
1. **Rent a VPS** (DigitalOcean, Linode, Vultr, etc.)
2. **SSH into your server**
3. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```
4. **Clone your repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
5. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
6. **Set environment variable**:
   ```bash
   export GROQ_API_KEY=your_api_key_here
   ```
7. **Run with systemd** (create `/etc/systemd/system/rag-system.service`):
   ```ini
   [Unit]
   Description=Multi-Language RAG System
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/path/to/your/app
   Environment=GROQ_API_KEY=your_api_key_here
   ExecStart=/usr/bin/python3 main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
8. **Start the service**:
   ```bash
   sudo systemctl enable rag-system
   sudo systemctl start rag-system
   ```

---

## 🔧 Environment Variables

Make sure to set these environment variables in your deployment platform:

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes |
| `HOST` | Host to bind to (default: 127.0.0.1) | ❌ No |
| `PORT` | Port to run on (default: 8001) | ❌ No |

## 🌍 Domain & SSL

### Custom Domain Setup:
1. **Purchase a domain** (Namecheap, GoDaddy, etc.)
2. **Point DNS** to your deployment platform
3. **Configure SSL** (most platforms do this automatically)

### SSL Certificates:
- **Railway**: Automatic SSL
- **Render**: Automatic SSL
- **Heroku**: Automatic SSL
- **VPS**: Use Let's Encrypt with Certbot

## 📊 Monitoring & Logs

### Built-in Health Check:
Your app includes a health check endpoint at `/health`

### Logging:
- Application logs are automatically captured by most platforms
- Check your platform's dashboard for logs

## 🔒 Security Considerations

1. **API Key Security**: Never commit your API key to Git
2. **Environment Variables**: Use platform-specific secret management
3. **HTTPS**: Always use HTTPS in production
4. **Rate Limiting**: Consider adding rate limiting for production use

## 🚀 Quick Deploy Commands

### Railway:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Render:
```bash
# Connect via Git
git push origin main
# Then configure in Render dashboard
```

### Heroku:
```bash
heroku create your-app-name
heroku config:set GROQ_API_KEY=your_key
git push heroku main
```

## 🎯 Recommended Deployment Flow

1. **Start with Railway** (easiest)
2. **Test thoroughly** with your API key
3. **Monitor performance** and usage
4. **Scale up** if needed

## 📞 Support

If you encounter issues:
1. Check the platform's documentation
2. Verify environment variables are set correctly
3. Check application logs
4. Ensure your Groq API key is valid and has sufficient credits

---

**🎉 Congratulations!** Your Multi-Language RAG System will be live and accessible from anywhere in the world! 