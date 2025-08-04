# 🔧 Setup Guide

## Environment Variables

Create a `.env` file in the root directory with your API keys:

```bash
# .env file
GROQ_API_KEY=your_groq_api_key_here
```

## Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   - Copy the example above to `.env`
   - Replace `your_groq_api_key_here` with your actual Groq API key

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Access the application**:
   - Open your browser to `http://localhost:8001`

## Security Notes

- ✅ Never commit your `.env` file to Git
- ✅ The `.env` file is already in `.gitignore`
- ✅ API keys are now loaded from environment variables
- ✅ Your API key is secure and won't be exposed in code

## Deployment

For deployment, set the `GROQ_API_KEY` environment variable in your deployment platform:

- **Railway**: Add in the Variables tab
- **Render**: Add in the Environment section
- **Heroku**: Use `heroku config:set GROQ_API_KEY=your_key`
- **VPS**: Export the variable in your shell 