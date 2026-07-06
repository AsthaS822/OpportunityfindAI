# OpportunityOS AI 🎓

> Your intelligent companion for discovering scholarships, internships, jobs, and educational opportunities worldwide.

OpportunityOS AI is a smart platform that combines a comprehensive dataset of 6,400+ opportunities with live web search to help students and professionals find the perfect match for their goals. Think of it as having a knowledgeable advisor who understands what you're looking for and explains everything in simple terms.

## ✨ What Makes It Special

### 🧠 Smart Understanding
The AI doesn't just search for keywords. It understands what you actually need:
- Ask about "career after MCA" → Gets jobs, scholarships, internships, and higher study options
- Say "PhD in Germany" → Finds funded positions, research fellowships, and doctoral programs
- Want "internships in India" → Searches both our dataset and live sources for the latest opportunities

### 🔍 Hybrid Search Engine
We search two places to give you the best results:
- **Our Dataset**: 6,400+ curated opportunities from trusted sources (Kaggle datasets)
- **Live Web**: Real-time verification from official websites like DAAD, Fulbright, Erasmus+, NSP, and more

### 📊 Detailed Explanations
No more generic "check eligibility" messages. We tell you:
- **Exact eligibility** (e.g., "BSc graduates with 60%+ marks")
- **Age limits** (when mentioned)
- **Funding details** (fully funded / partial / self-funded, what's covered)
- **Application fees** (if specified)
- **Required documents** (transcripts, tests, language requirements)
- **Deadlines** (exact dates when available)
- **Next steps** (how to apply, what to prepare)

### 🎯 Profile-Aware Matching
Tell us your background, and we'll show you relevant opportunities:
- **MCA graduate** → Software engineering jobs, CS scholarships, tech internships
- **BSc Maths** → MSc programs, research fellowships, PhD positions, education loans
- **MBA student** → Management consulting roles, business programs, executive fellowships

### 🌍 Global Coverage
Search opportunities across 48+ countries:
- Study abroad programs (Germany, USA, UK, Canada, Australia...)
- Scholarships and fellowships (DAAD, Fulbright, Chevening, Erasmus+)
- Jobs and internships (India and international)
- Government schemes (NSP, AICTE, UGC)
- Research positions and grants

## 🚀 Features

### For Students
- **Scholarship Discovery**: Find fully-funded and partial scholarships matching your profile
- **Study Abroad Guidance**: Programs, universities, funding options explained clearly
- **Career Planning**: Get personalized roadmaps after your degree (BSc, MCA, B.Tech, MBA, etc.)
- **Internship Search**: Paid and unpaid opportunities in your field
- **Government Schemes**: Discover schemes you're eligible for (based on category, income, marks)

### For Professionals
- **Job Opportunities**: Entry-level and experienced positions worldwide
- **Fellowship Programs**: Research and professional development fellowships
- **Grant Funding**: Startup grants, research grants, project funding
- **PhD Positions**: Funded doctoral programs with stipends

### Smart Features
- **Eligibility Check**: Know instantly if you qualify
- **Deadline Tracking**: Never miss an application deadline
- **Document Checklist**: Know exactly what you need to apply
- **Comparison Tool**: Compare multiple opportunities side-by-side
- **Bilingual Support**: English + हिंदी interface

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for lightning-fast development
- **Tailwind CSS** for beautiful, responsive design
- **Wouter** for lightweight routing
- **React Query** for data fetching
- **Radix UI** for accessible components

### Backend
- **FastAPI** (Python) - High-performance async API
- **Groq AI** - Advanced language model for understanding queries and reasoning
- **Jina AI** - Live web search and content extraction
- **RapidFuzz** - Fast fuzzy matching for better search results
- **uvicorn** - ASGI server

### Intelligence Layer
- **Dataset Analyzer**: Builds knowledge graphs from 6,400+ opportunities
- **Intent Detector**: Understands what users actually want
- **Multi-Search Engine**: Combines dataset + web search intelligently
- **Reasoning Engine**: Explains opportunities in detail
- **Verification System**: Validates information from official sources

## 📁 Dataset Sources

Our opportunities come from trusted Kaggle datasets:
- QS World University Rankings (1,504 universities)
- Scholarship databases (227 + 390 + 879 scholarships)
- Updated opportunities dataset (3,400+ entries)

All data is regularly verified against official sources.

## 🚀 Getting Started

### Prerequisites
- **Node.js** 18+ (for frontend)
- **Python** 3.9+ (for backend)
- **API Keys**:
  - Groq API key (get from [groq.com](https://groq.com))
  - Jina AI key (get from [jina.ai](https://jina.ai))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/opportunityos-ai.git
cd opportunityos-ai
```

2. **Set up environment variables**
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_key_here
JINA_API_KEY=your_jina_key_here
```

3. **Install frontend dependencies**
```bash
npm install
```

4. **Install backend dependencies**
```bash
pip install -r backend/requirements.txt
```

5. **Run the application**

**Option 1: Use the start script (Windows)**
```bash
start.bat
```

**Option 2: Run manually**

Terminal 1 (Backend):
```bash
cd backend
uvicorn main:app --reload --port 8001
```

Terminal 2 (Frontend):
```bash
npm run dev
```

6. **Open your browser**
Navigate to `http://localhost:5173`

## 📖 How to Use

1. **Ask naturally**: "Show me scholarships in Germany for Computer Science"
2. **Get smart results**: AI understands you want CS scholarships, not German language courses
3. **Read details**: Each opportunity shows eligibility, funding, deadlines, and next steps
4. **Take action**: Follow the roadmap provided for each opportunity

### Example Queries
- "Career options after MCA"
- "Fully funded PhD in AI"
- "Internships in India for engineering students"
- "Education loans for study abroad"
- "Government schemes for SC category students"
- "Research fellowships in Europe"

## 🎯 Use Cases

### For Final Year Students
"What should I do after B.Tech CSE?" → Get personalized options for jobs, Masters, startups, government exams

### For Study Abroad Aspirants
"Masters in Data Science in Germany" → Find programs, scholarships, eligibility, costs, deadlines

### For Career Switchers
"Career change from engineering to MBA" → Discover MBA programs, entrance exams, funding options

### For Researchers
"PhD positions in Artificial Intelligence" → Funded positions, research grants, fellowship programs

## 🤝 Contributing

We welcome contributions! Here's how you can help:
- **Add more datasets**: Know a good source of opportunities? Share it!
- **Improve explanations**: Make the AI responses clearer
- **Fix bugs**: Report issues or submit PRs
- **Translate**: Add support for more Indian languages

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Opportunity data sourced from **Kaggle** datasets
- Official sources: DAAD, Fulbright, Erasmus+, NSP, UGC, AICTE, British Council
- Built with love for students and job seekers everywhere

## 📧 Contact

Have questions or suggestions? Open an issue on GitHub or reach out!

---

**Made with ❤️ to help students discover their next big opportunity**
