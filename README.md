# 🎭 Nexus AI - Personal Assistant

**AI-powered multi-agent assistant with intelligent routing and seamless integrations**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-FF6B6B?style=for-the-badge)](https://python.langchain.com/docs/langgraph)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

---

## 🚀 **What is Nexus AI?**

Nexus AI is an intelligent personal assistant powered by **Google Gemini 2.0 Flash** that uses a sophisticated multi-agent architecture to handle various tasks. Instead of having one AI try to do everything, Nexus AI has **three specialized agents** (Slack, Weather, Calendar) that are experts in their domains, coordinated by an intelligent orchestrator.

### **🎯 Key Features**

- **🤖 Multi-Agent Architecture**: Specialized AI agents for different tasks
- **🎭 Intelligent Orchestration**: Smart routing to the right agent based on user intent
- **🔐 Secure Authentication**: JWT-based user authentication with Supabase
- **💬 Natural Language Processing**: Chat with your assistant in plain English
- **📱 Modern Web Interface**: Responsive React/Next.js frontend
- **⚡ Real-time Communication**: Instant responses and seamless user experience
- **🔗 External Integrations**: Connect to Slack, weather services, Google Calendar, and more

---

## 🤖 **Available Agents**

### **1. 🎭 Orchestrator Agent**

- **Role**: Central coordinator and decision maker
- **Capabilities**: Analyzes user requests and routes to appropriate specialized agents
- **Intelligence**: Uses LLM to understand context and user intent

### **2. 📱 Slack Agent**

- **Role**: Team communication specialist
- **Capabilities**:
  - Send messages to Slack channels (team, development)
  - Handle team communication requests
  - Slack webhook integration
- **Examples**: _"Send hello to team channel"_, _"Tell development I'll be late"_

### **3. 🌤️ Weather Agent**

- **Role**: Weather and climate expert
- **Capabilities**:
  - Current weather information for any city
  - Multi-day weather forecasts (up to 7 days)
  - Climate data and historical information
  - Weather comparisons between cities
- **Examples**: _"Weather in Tokyo?"_, _"5-day forecast for London"_, _"Compare weather NYC vs LA"_

### **4. 📅 Google Calendar Agent**

- **Role**: Calendar and scheduling specialist
- **Capabilities**:
  - Create calendar events through natural language
  - Google OAuth2 integration for secure access
  - Parse event details (date, time, description) from prompts
  - Store encrypted calendar credentials securely
- **Examples**: _"Schedule meeting tomorrow at 2pm"_, _"Plan dentist appointment Friday 10am"_, _"Book lunch with client Thursday"_

---

## 🏗️ **System Architecture**

```mermaid
graph TB
    subgraph "Frontend (Next.js)"
        UI["🖥️ React UI"]
        AUTH["🔐 Authentication"]
        CHAT["💬 Chat Interface"]
    end

    subgraph "Backend (FastAPI)"
        API["⚡ REST API"]
        ORCH["🎭 Orchestrator Agent"]

        subgraph "Specialized Agents"
            SLACK["📱 Slack Agent"]
            WEATHER["🌤️ Weather Agent"]
            CALENDAR["📅 Calendar Agent"]
        end
    end

    subgraph "External Services"
        SUPABASE["🗄️ Supabase Database"]
        GEMINI["🧠 Google Gemini AI"]
        SLACK_API["📱 Slack Webhooks"]
        WEATHER_API["🌐 Weather APIs"]
        CALENDAR_API["📅 Google Calendar API"]
    end

    UI --> API
    AUTH --> SUPABASE
    CHAT --> ORCH
    ORCH --> SLACK
    ORCH --> WEATHER
    ORCH --> CALENDAR
    ORCH --> GEMINI
    SLACK --> SLACK_API
    WEATHER --> WEATHER_API
    CALENDAR --> CALENDAR_API
```

### **🔄 How It Works**

1. **User Input**: You type a message in natural language
2. **Authentication**: System verifies your identity via JWT tokens
3. **Orchestration**: The orchestrator analyzes your request using Gemini AI
4. **Agent Selection**: Routes to the appropriate specialized agent
5. **Task Execution**: Agent performs the specific task (weather, Slack, etc.)
6. **Response**: Formatted, personalized response returned to you

---

## 🛠️ **Technologies Used**

### **Backend**

- **FastAPI** - High-performance Python web framework
- **LangGraph** - Agent workflow orchestration
- **LangChain** - LLM integration and tooling
- **Google Gemini 2.0 Flash** - Advanced AI language model
- **Supabase** - PostgreSQL database with real-time features
- **JWT** - Secure authentication tokens
- **bcrypt** - Password hashing
- **Pydantic** - Data validation and settings management

### **Frontend**

- **Next.js 15** - React framework with App Router
- **React 19** - UI library with latest features
- **TypeScript** - Type-safe JavaScript
- **TailwindCSS** - Utility-first CSS framework
- **Axios** - HTTP client for API communication
- **React Hook Form** - Form state management
- **Lucide React** - Beautiful icon library
- **React Hot Toast** - Elegant notifications

### **Database & Auth**

- **Supabase** - PostgreSQL with Row Level Security
- **JWT Authentication** - Secure token-based auth
- **Encrypted Storage** - Secure credential management

---

## 📋 **Prerequisites**

Before you begin, ensure you have the following installed:

- **Python 3.11+** ([Download Python](https://python.org/downloads/))
- **Node.js 18+** ([Download Node.js](https://nodejs.org/))
- **npm or yarn** (comes with Node.js)
- **Git** ([Download Git](https://git-scm.com/downloads))

### **Required API Keys & Services**

1. **Google Gemini API Key**

   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new API key
   - Keep it secure - you'll need it for setup

2. **Supabase Project**

   - Sign up at [Supabase](https://supabase.com/)
   - Create a new project
   - Note your project URL and API keys

3. **Slack Webhooks** (Optional)

   - Create Slack webhook URLs for your channels
   - Required for Slack messaging functionality

4. **Google Calendar API** (Optional)
   - Set up Google Cloud Console project
   - Enable Google Calendar API
   - Create OAuth2 credentials
   - Required for calendar event creation

---

## 🚀 **Quick Start Guide**

### **1. Clone the Repository**

```bash
git clone <your-repository-url>
cd langgraph
```

### **2. Backend Setup**

#### **Install Dependencies**

```bash
cd backend
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

#### **Environment Configuration**

Create a `.env` file in the `backend/` directory:

```bash
# Copy the example and fill in your values
cp .env.example .env
```

**Required Environment Variables:**

```bash
# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key-here

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database URL
DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres

# Slack Webhooks (Optional)
SLACK_TEAM_WEBHOOK=https://hooks.slack.com/services/YOUR/TEAM/WEBHOOK
SLACK_DEV_WEBHOOK=https://hooks.slack.com/services/YOUR/DEV/WEBHOOK

# Google Calendar Configuration (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
GOOGLE_CALENDAR_SCOPES=https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/calendar.readonly
CALENDAR_TOKEN_ENCRYPTION_KEY=your-32-character-encryption-key
```

#### **Database Setup**

1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Run the SQL script from `backend/database_schema.sql`

#### **Start Backend Server**

```bash
# Make sure you're in the backend directory and virtual environment is activated
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: **http://localhost:8000**

### **3. Frontend Setup**

#### **Install Dependencies**

```bash
cd frontend
npm install
# or
yarn install
```

#### **Environment Configuration**

Create a `.env.local` file in the `frontend/` directory:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### **Start Frontend Development Server**

```bash
npm run dev
# or
yarn dev
```

The frontend will be available at: **http://localhost:3000**

---

## 🎯 **How to Use Nexus AI**

### **1. Sign Up & Sign In**

1. Visit **http://localhost:3000**
2. Click **"Get Started"** to create a new account
3. Fill in your details and create a password
4. Sign in with your credentials

### **2. Connect Your Services (Optional)**

Before using specific features, you may need to connect external services:

- **Google Calendar**: Visit your profile settings to connect your Google Calendar for event creation
- **Slack**: Webhooks are pre-configured for team communication

### **3. Chat with Your Assistant**

Once logged in, you can chat naturally with your AI assistant:

#### **Slack Commands:**

- _"Send hello to team channel"_
- _"Tell the development team I'll be late"_
- _"Send a message to team saying meeting is cancelled"_

#### **Weather Queries:**

- _"What's the weather in Tokyo?"_
- _"Give me a 5-day forecast for London"_
- _"Compare weather between New York and Paris"_
- _"What's the climate like in Mumbai during July?"_

#### **Calendar Commands:**

- _"Schedule meeting tomorrow at 2pm"_
- _"Plan dentist appointment next Friday 10am"_
- _"Add team standup Monday 9am"_
- _"Book lunch with client Thursday 12:30pm"_

#### **General Conversation:**

- _"What can you help me with?"_
- _"Tell me about the weather and then send a message to the team"_
- _"Schedule a meeting and notify the team on Slack"_

### **4. Intelligent Routing**

The orchestrator automatically determines which agent to use based on your request:

- **Weather words** → Weather Agent
- **Slack/messaging words** → Slack Agent
- **Calendar/scheduling words** → Calendar Agent
- **Conversational queries** → Direct orchestrator response

---

## 📚 **API Documentation**

When the backend is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **System Status**: http://localhost:8000/

### **Key Endpoints**

| Endpoint               | Method | Description                  |
| ---------------------- | ------ | ---------------------------- |
| `/auth/signup`         | POST   | User registration            |
| `/auth/signin`         | POST   | User login                   |
| `/auth/me`             | GET    | Get current user             |
| `/chat`                | POST   | Send message to AI assistant |
| `/calendar/connect`    | GET    | Connect Google Calendar      |
| `/calendar/status`     | GET    | Check calendar integration   |
| `/calendar/disconnect` | DELETE | Disconnect calendar          |
| `/health`              | GET    | System health check          |

---

## 📁 **Project Structure**

```
langgraph/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── agents/            # AI agent implementations
│   │   ├── states/            # Agent state definitions
│   │   ├── nodes/             # Agent node logic
│   │   ├── edges/             # Workflow edge definitions
│   │   ├── tools/             # Agent tools and capabilities
│   │   ├── services/          # Business logic services
│   │   ├── database/          # Database operations
│   │   ├── routes/            # API route definitions
│   │   ├── models/            # Data models
│   │   └── main.py           # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── database_schema.sql    # Database schema
│   └── .env                  # Environment variables
├── frontend/                  # Next.js frontend
│   ├── src/
│   │   ├── app/              # App Router pages
│   │   ├── components/       # React components
│   │   ├── contexts/         # React contexts
│   │   └── lib/             # Utility libraries
│   ├── package.json         # Node.js dependencies
│   └── .env.local          # Frontend environment
├── tasks/                    # Implementation task documents
└── README.md                # This file
```

---

## 🧪 **Development & Testing**

### **Backend Development**

```bash
# Run with auto-reload
python -m uvicorn src.main:app --reload

# Run tests (when available)
pytest

# Check code formatting
black src/
flake8 src/
```

### **Frontend Development**

```bash
# Development server
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Lint code
npm run lint
```

---

## 🚀 **Production Deployment**

### **Backend (FastAPI)**

1. Set up a production server (AWS, Google Cloud, DigitalOcean, etc.)
2. Install dependencies and set environment variables
3. Use a production WSGI server like Gunicorn:
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### **Frontend (Next.js)**

1. Build the application: `npm run build`
2. Deploy to Vercel, Netlify, or your preferred hosting platform
3. Update environment variables for production APIs

### **Database**

- Supabase handles production database automatically
- Ensure proper RLS policies are in place
- Monitor usage and performance

---

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **Backend won't start**

- ✅ Check Python version (3.11+ required)
- ✅ Verify virtual environment is activated
- ✅ Ensure all environment variables are set
- ✅ Check Gemini API key is valid

#### **Frontend won't connect to backend**

- ✅ Verify backend is running on port 8000
- ✅ Check CORS settings in backend
- ✅ Confirm API URL in frontend environment

#### **Database connection issues**

- ✅ Verify Supabase credentials
- ✅ Check database URL format
- ✅ Ensure database schema is created

#### **AI responses not working**

- ✅ Confirm Gemini API key is valid and has quota
- ✅ Check agent imports and initialization
- ✅ Verify LangGraph workflow configuration

### **Getting Help**

If you encounter issues:

1. Check the logs in both backend and frontend consoles
2. Verify all environment variables are correctly set
3. Ensure all services (Supabase, Gemini) are accessible
4. Check API documentation at `/docs` for debugging

---

## 🎯 **What's Next?**

### **Planned Features**

- 📧 **Email Agent** - Send and manage emails
- 📄 **Document Processing** - Handle PDFs and documents
- 🔍 **Web Search Agent** - Search the internet for information
- 🗂️ **File Management** - Organize and manage files
- 🎵 **Media Controls** - Control music and media playback

### **Contributing**

This is a personal project, but contributions and suggestions are welcome! Feel free to:

- Report bugs or issues
- Suggest new features
- Improve documentation
- Enhance existing agents

---

## 📄 **License**

This project is for educational and personal use. Please respect the terms of service for all integrated APIs and services.

---

## 🙏 **Acknowledgments**

- **LangChain & LangGraph** - For the amazing agent orchestration framework
- **Google Gemini** - For the powerful AI capabilities
- **Supabase** - For the excellent database and auth platform
- **FastAPI** - For the high-performance web framework
- **Next.js** - For the amazing React framework

---

**🎭 Nexus AI - Your Intelligent Personal Assistant**

_Built with ❤️ using cutting-edge AI and web technologies_
