# Google ADK Basics

🚀 **Welcome to the comprehensive journey through Google Agent Development Kit (ADK)!**

This repository contains a complete collection of AI agent implementations using Google's ADK framework, designed to learn the fundamentals of building sophisticated AI agents with fine-grained control.

## Project Structure

```
GoogleADKDevwork/
├── 📁 openai_agent/              # Using OpenAI models via LiteLLM
├── 📁 sequential_agent/          # Chain-based workflow agents
├── 📁 parallel_agent/            # Concurrent execution agents
├── 📁 session_agent/             # Session management with persistent state
├── 📁 structured_agent/          # Structured input/output schemas
├── 📁 tool_agent/                # Custom tools and function calling
├── 📁 persistent_session_agent/  # Database-backed persistenta gents
├── 📄 requirements.txt           # Python dependencies
├── 📄 Readmemation.md            # Detailed setup instructions
```

## 🚀 Getting Started

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Google Cloud Account** (free tier available)
3. **OpenAI API Key** (optional, for openai_agent)

### Setup Instructions

#### 1. Google Cloud Setup

1. **Create a Google Cloud Project**:

   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Access Google AI Studio**:

   - Navigate to [Google AI Studio](https://aistudio.google.com/)
   - Create an API Key (free tier - no credit card needed!)

3. **Environment Configuration**:
   - Copy your API key
   - Create a `.env` file :
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

#### 2. OpenAI API
1. **Create a new API**:
   - Go to [OpenAI API Key](https://platform.openai.com/api-keys)
   - Create a new project or select an existing one
   - Add a new key

3. **Environment Configuration**:
   - Copy your API key
   - Create a `.env` file :
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

#### 2. Project Setup

```bash
# Clone the repository
git clone <repository-url>
cd google-adk-devwork

# Install dependwencies
pip install -r requirements.txt
```

## 🔧 Development Best Practices

### Folder Structure

```
agent_name/
├── __init__.py      # Python package marker
├── agent.py         # Main agent logic
```

### Code Organization

- Always define `root_agent` in `agent.py` to work with `adk run` and `adk web`
- Use descriptive agent names and descriptions
- Implement proper error handling
- Document tool functions with clear descriptions

## 📖 Additional Resources
- [Google ADK Documentation](https://google.github.io/adk-docs/)




