# Contributing to BooJ 👻

First off, thanks for taking the time to contribute! 🎉

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Setup Development Environment

1. **Clone the repository**
```bash
git clone https://github.com/Loonder/BooJ.git
cd BooJ
```

2. **Backend Setup (Python)**
```bash
# Create virtual environment
python -m venv venv311
.\venv311\Scripts\activate  # Windows
source venv311/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys
```

3. **Frontend Setup (Next.js)**
```bash
cd jobpulse-dashboard
npm install
```

4. **Run Tests**
```bash
# Backend tests
pytest

# Frontend (when implemented)
cd jobpulse-dashboard
npm test
```

---

## 🏃 Running Locally

### Backend API
```bash
# Start FastAPI server
python -m uvicorn api.main:app --reload --port 8001
```

### Frontend Dashboard
```bash
cd jobpulse-dashboard
npm run dev
```

### Run Scrapers
```bash
python src/hunter.py
```

---

## 📝 Code Style

### Python
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Max line length: 100 characters

```python
def fetch_jobs(search_terms: list[str]) -> list[dict]:
    """Fetch jobs from external API.
    
    Args:
        search_terms: List of search keywords
        
    Returns:
        List of job dictionaries
    """
    pass
```

### TypeScript/React
- Use TypeScript strict mode
- Functional components with hooks
- Use shadcn/ui components
- Follow Airbnb style guide

```typescript
interface JobCardProps {
  job: Job
  onBookmark: (id: number) => void
}

export function JobCard({ job, onBookmark }: JobCardProps) {
  // Component code
}
```

---

## 🧪 Testing

### Backend
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_database.py
```

### Frontend
```bash
cd jobpulse-dashboard
npm test
npm run test:coverage
```

All PRs must maintain or improve test coverage.

---

## 🔀 Pull Request Process

1. **Fork the repo** and create your branch from `main`
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new features
   - Update documentation

3. **Run tests and linting**
   ```bash
   pytest
   # (linting setup coming soon)
   ```

4. **Commit your changes**
   ```bash
   git commit -m "✨ Add amazing feature"
   ```
   
   Use conventional commits:
   - `✨ feat:` New feature
   - `🐛 fix:` Bug fix
   - `📝 docs:` Documentation
   - `🎨 style:` Formatting
   - `♻️ refactor:` Code refactoring
   - `✅ test:` Adding tests
   - `🔧 chore:` Maintenance

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Describe what you changed and why
   - Reference any related issues
   - Request review

---

## 🐛 Reporting Bugs

### Before Submitting
- Check if the bug was already reported in Issues
- Try to reproduce with the latest version

### Bug Report Template
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Windows 11]
- Python version: [e.g. 3.11]
- Node version: [e.g. 18.17]
```

---

## 💡 Suggesting Features

We love feature suggestions! Open an issue with:
- Clear description of the feature
- Why it would be useful
- Possible implementation approach

---

## 🏗️ Project Structure

```
BooJ/
├── src/              # Python scrapers and logic
├── api/              # FastAPI backend
├── jobpulse-dashboard/  # Next.js frontend
├── tests/            # Python tests
├── data/             # SQLite database (gitignored)
└── .github/          # CI/CD workflows
```

---

## 📚 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [JobSpy Library](https://github.com/cullenwatson/JobSpy)

---

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Give credit where it's due

---

## ❓ Questions?

- Open an issue with the `question` label
- Check existing issues and discussions

---

## 🎯 Good First Issues

Look for issues labeled `good first issue` - these are great for beginners!

---

**Thank you for contributing to BooJ!** 👻✨
