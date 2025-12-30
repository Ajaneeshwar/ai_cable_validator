<div align="center">

# 🔌 AI-Driven Cable Design Validation System

### Intelligent IEC Standards Compliance Validation Powered by Google Gemini AI

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Google Gemini](https://img.shields.io/badge/Gemini_AI-Powered-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)

<p align="center">
  <strong>A production-ready full-stack application that validates low-voltage cable designs against IEC 60502-1 and IEC 60228 international standards using advanced AI reasoning.</strong>
</p>

[Features](#-features) •
[Tech Stack](#-tech-stack) •
[Quick Start](#-quick-start) •
[API Reference](#-api-reference) •
[Architecture](#-architecture) •
[Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Quick Start](#-quick-start)
- [Environment Configuration](#-environment-configuration)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Key Design Decisions](#-key-design-decisions)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **AI-Driven Cable Design Validation System** is a sophisticated full-stack application designed for electrical cable manufacturers and engineers. It leverages Google's Gemini AI to intelligently validate cable specifications against international IEC standards, providing detailed compliance reports with confidence scores and transparent reasoning.

### 🎬 Demo

> **Live Demo**: Coming Soon  
> **API Documentation**: Available at `/docs` when running locally

### 🔑 Key Highlights

- **AI-First Approach**: No hardcoded validation rules - AI interprets IEC standards dynamically
- **Production-Ready**: Complete with security middleware, error handling, and logging
- **Type-Safe**: Full TypeScript frontend with Pydantic-validated backend
- **Developer Experience**: Comprehensive API documentation with Swagger/OpenAPI

---

## ✨ Features

### Core Functionality

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered Validation** | Uses Google Gemini to validate cable designs against IEC 60502-1 and IEC 60228 standards |
| 📝 **Multiple Input Modes** | Supports structured JSON, free-text natural language, and database record selection |
| 📊 **Detailed Results** | Provides PASS/WARN/FAIL status with granular explanations for each parameter |
| 📈 **Confidence Scoring** | AI-generated confidence levels (0-100%) with transparent reasoning |
| 🔍 **AI Reasoning Transparency** | View detailed AI thought process for each validation decision |

### Technical Features

| Feature | Description |
|---------|-------------|
| 🔐 **Security First** | CORS protection, trusted host middleware, and secure error handling |
| 📚 **Interactive API Docs** | Auto-generated Swagger UI and ReDoc documentation |
| 💾 **Data Persistence** | SQLite database with SQLAlchemy ORM for cable design storage |
| 🎨 **Premium UI** | Dark theme with Material UI components and smooth animations |
| 📱 **Responsive Design** | Fully responsive layout for desktop and mobile devices |

---

## 🛠 Tech Stack

### Backend

| Technology | Purpose |
|------------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python 3.10+** | Core programming language |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) **FastAPI** | High-performance async web framework |
| ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white) **SQLAlchemy 2.0** | ORM for database operations |
| ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white) **Pydantic** | Data validation and serialization |
| ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white) **SQLite** | Lightweight relational database |
| ![Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=flat&logo=google&logoColor=white) **Google Gemini** | AI-powered validation engine |

### Frontend

| Technology | Purpose |
|------------|---------|
| ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js&logoColor=white) **Next.js 14** | React framework with App Router |
| ![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black) **React 18** | UI component library |
| ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white) **TypeScript 5** | Type-safe JavaScript |
| ![MUI](https://img.shields.io/badge/Material_UI-007FFF?style=flat&logo=mui&logoColor=white) **Material UI 5** | React UI component library |
| ![Axios](https://img.shields.io/badge/Axios-5A29E4?style=flat&logo=axios&logoColor=white) **Axios** | HTTP client for API requests |

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js 14 + MUI)                        │
│  ┌────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │  Input Panel   │  │  Results Grid   │  │   AI Reasoning Drawer       │  │
│  │  • Form Mode   │  │  • Data Table   │  │   • Confidence Scores       │  │
│  │  • Free Text   │  │  • Status Chips │  │   • Detailed Explanations   │  │
│  │  • DB Select   │  │  • Filtering    │  │   • Parameter Breakdown     │  │
│  └────────────────┘  └─────────────────┘  └─────────────────────────────┘  │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │ HTTPS/REST
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       BACKEND (FastAPI + Python)                            │
│  ┌────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │    Routers     │  │   Validation    │  │      AI Gateway             │  │
│  │  • /design/*   │─▶│    Service      │─▶│  • Google Gemini Client     │  │
│  │  • /health     │  │  • Orchestrator │  │  • Prompt Engineering       │  │
│  └────────────────┘  └─────────────────┘  └─────────────────────────────┘  │
│           │                                                                  │
│           ▼                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    SQLite Database (SQLAlchemy ORM)                  │   │
│  │                    • Cable Design Records                            │   │
│  │                    • Validation History                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- **Python** 3.10 or higher ([Download](https://python.org/downloads))
- **Node.js** 18 or higher ([Download](https://nodejs.org))
- **Git** ([Download](https://git-scm.com))
- **Google Gemini API Key** ([Get Free API Key](https://aistudio.google.com/app/apikey))

### Installation

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/ai_cable_validator.git
cd ai_cable_validator
```

#### 2️⃣ Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start the development server
uvicorn app.main:app --reload --port 8000
```

✅ **Backend running at**: http://localhost:8000  
📚 **API Documentation**: http://localhost:8000/docs

#### 3️⃣ Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.local.example .env.local

# Start the development server
npm run dev
```

✅ **Frontend running at**: http://localhost:3000

---

## ⚙️ Environment Configuration

### Backend (`backend/.env`)

```env
# Environment (development, staging, production)
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite:///./cable_designs.db

# Google Gemini API Configuration
# Get your API key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Model Options:
# - gemini-2.0-flash (fast, good for demos)
# - gemini-1.5-pro (slower, better reasoning)
GEMINI_MODEL=gemini-2.0-flash

# CORS Configuration (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend (`frontend/.env.local`)

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📖 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/design/validate` | Validate a cable design |
| `GET` | `/design/list` | List all saved cable designs |
| `GET` | `/design/{id}` | Get a specific cable design |
| `GET` | `/health` | Health check endpoint |
| `GET` | `/docs` | Interactive API documentation |

### Request Examples

#### Structured Input Validation

```bash
curl -X POST "http://localhost:8000/design/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "design": {
      "standard": "IEC 60502-1",
      "voltage": "0.6/1 kV",
      "conductor_material": "Cu",
      "conductor_class": "Class 2",
      "csa": 10,
      "insulation_material": "PVC",
      "insulation_thickness": 1.0
    }
  }'
```

#### Free-Text Natural Language Validation

```bash
curl -X POST "http://localhost:8000/design/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "free_text": "IEC 60502-1 cable, 10 sqmm Cu Class 2, PVC insulation 1.0 mm, LV 0.6/1 kV"
  }'
```

#### Database Record Validation

```bash
curl -X POST "http://localhost:8000/design/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "design_id": 1
  }'
```

### Response Format

```json
{
  "success": true,
  "data": {
    "overall_status": "PASS",
    "overall_confidence": 92,
    "parameters": [
      {
        "name": "Conductor Cross-Section",
        "status": "PASS",
        "confidence": 95,
        "reasoning": "10 mm² meets IEC 60228 Class 2 requirements..."
      }
    ],
    "ai_reasoning": "Based on IEC 60502-1 standards..."
  }
}
```

---

## 📁 Project Structure

```
cable-design-validator/
│
├── 📂 backend/
│   ├── 📂 app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── config.py            # Environment configuration
│   │   ├── database.py          # SQLite database setup
│   │   ├── seed.py              # Sample data seeding
│   │   ├── 📂 models/           # SQLAlchemy ORM models
│   │   ├── 📂 schemas/          # Pydantic request/response schemas
│   │   ├── 📂 services/
│   │   │   ├── ai_gateway.py    # Google Gemini integration
│   │   │   └── validation.py    # Validation business logic
│   │   └── 📂 routers/          # API route handlers
│   ├── .env.example             # Environment template
│   ├── requirements.txt         # Python dependencies
│   └── README.md
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 app/              # Next.js App Router pages
│   │   ├── 📂 components/       # React UI components
│   │   ├── 📂 services/         # API client services
│   │   ├── 📂 theme/            # Material UI theme config
│   │   └── 📂 types/            # TypeScript type definitions
│   ├── .env.local.example       # Environment template
│   ├── package.json             # Node.js dependencies
│   └── tsconfig.json            # TypeScript configuration
│
└── README.md                    # This file
```

---

## 🧪 Testing

### Test Cases

| # | Test Case | Input | Expected Result |
|---|-----------|-------|-----------------|
| 1 | Valid Compliant Design | 10mm² Cu, PVC 1.0mm | All PASS, confidence ≥85% |
| 2 | Borderline Insulation | 16mm² Cu, PVC 0.9mm | Insulation → WARN |
| 3 | Non-Compliant Design | 10mm² Cu, PVC 0.5mm | Insulation → FAIL |
| 4 | Incomplete Free Text | "10 sqmm copper cable" | Missing fields → WARN |

### Running Tests

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests (if configured)
cd frontend
npm run test
```

---

## 💡 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **AI-First Validation** | No hardcoded IEC rules - AI interprets standards dynamically, allowing adaptation to standard updates |
| **Transparent Reasoning** | Every validation decision includes confidence scores and detailed explanations for auditability |
| **Clean Architecture** | Separated concerns (Routers → Services → AI Gateway) for maintainability and testability |
| **Type Safety** | Full TypeScript frontend + Pydantic backend prevents runtime errors and improves DX |
| **Premium UX** | Dark theme, smooth animations, and responsive design for professional appearance |


---

## 🔮 Future Enhancements

- [ ] **PDF Report Generation** - Export validation results as PDF reports
- [ ] **Multiple Standard Support** - Add support for additional IEC standards
- [ ] **Batch Validation** - Validate multiple cable designs simultaneously
- [ ] **User Authentication** - Add JWT-based authentication
- [ ] **Validation History** - Track and compare historical validations
- [ ] **Cloud Deployment** - Deploy to AWS/GCP with production database

---

## 👨‍💻 Author

**Your Name**  
- GitHub: [@Ajaneeshwar](https://github.com/Ajaneeshwar)
- LinkedIn: [Ajaneeshwar](https://www.linkedin.com/in/ajaneeshwar-s-378818250)
- Email: ajaneeshwar05@gmail.com

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star!**

Built with ❤️ using FastAPI, Next.js, and Google Gemini AI

*Dream it. Build it. Do it here. — InnoVites*

</div>
