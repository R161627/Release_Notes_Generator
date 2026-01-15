# 🚀 AI-Powered Release Notes Generator

An intelligent tool that automatically generates professional release notes by analyzing GitLab merge requests and JIRA tickets using local LLM processing.

## 📋 Features

- **GitLab Integration**: Automatically fetches merge requests within specified date ranges
- **JIRA Integration**: Extracts and enriches data with JIRA ticket details
- **AI-Powered Summarization**: Uses local Qwen2.5 LLM via Ollama for intelligent content generation
- **Professional Output**: Generates executive summaries and technical changelogs
- **Markdown Export**: Creates ready-to-use release notes in Markdown format
- **Diff Analysis**: Optional inclusion of file changes and diff statistics
- **Secure**: Uses local LLM processing - no data sent to external AI services

## 🔧 Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- Qwen2.5 model downloaded in Ollama (`ollama pull qwen2.5`)
- Access to GitLab API with appropriate permissions
- Access to JIRA API with read permissions

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Release_Notes
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama:**
   ```bash
   # Install Ollama (visit https://ollama.ai/ for platform-specific instructions)
   
   # Pull the Qwen2.5 model
   ollama pull qwen2.5
   ```

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:

```bash
# Date Range for Release Notes
START_DATE=2024-01-01
END_DATE=2024-01-31

# GitLab Configuration
GITLAB_URL=https://your-gitlab-instance.com
GITLAB_PROJECT_ID=your-project-id
GITLAB_TOKEN=your-gitlab-access-token

# JIRA Configuration
JIRA_SERVER=https://your-jira-instance.com
JIRA_TOKEN=your-jira-api-token
```

### Getting API Tokens

**GitLab Token:**
1. Go to GitLab → User Settings → Access Tokens
2. Create a token with `read_api` and `read_repository` scopes

**JIRA Token:**
1. Go to JIRA → Account Settings → Security → API Tokens
2. Create a new API token

## 🎯 Usage

1. **Configure your environment:**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

2. **Ensure Ollama is running:**
   ```bash
   ollama serve
   ```

3. **Run the release notes generator:**
   ```bash
   python main.py
   ```

The tool will:
1. Fetch merge requests from GitLab for the specified date range
2. Extract JIRA ticket IDs from PR titles and descriptions
3. Retrieve detailed JIRA ticket information
4. Generate AI-powered release notes
5. Save the output to `Release_Notes.md`

## 📁 Project Structure

```
Release_Notes/
├── AI/
│   ├── prompt.py          # LLM prompt templates
│   └── summarization.py   # AI summarization logic
├── Data/
│   ├── jira_client.py     # JIRA API integration
│   └── merge_requests.py  # GitLab API integration
├── main.py                # Main application entry point
├── requirements.txt       # Python dependencies
├── Release_Notes.md       # Generated release notes output
├── gitlab_prs.json       # Raw PR and JIRA data cache
└── sample_output.md      # Example output
```

## 📝 Output Format

The generated release notes include:

### Executive Summary
- High-level overview suitable for management
- Business impact and key improvements
- Professional, non-technical language

### Technical Changelog
- Categorized changes (🚀 New Features, 🐛 Bug Fixes, ⚡ Performance & Improvements, 🔒 Security)
- PR and JIRA ticket references
- Detailed technical descriptions

## 🔍 Example Usage

```bash
# Generate release notes for December 2024
# Set dates in .env file:
START_DATE=2024-12-01
END_DATE=2024-12-31

# Run the generator
python main.py
```

Output files:
- `gitlab_prs.json`: Raw data from GitLab and JIRA
- `Release_Notes.md`: Formatted release notes

## 🛠️ Dependencies

- `jira~=3.10.5` - JIRA API client
- `python-dotenv~=1.1.0` - Environment variable management
- `requests~=2.32.5` - HTTP requests for GitLab API
- `langchain-ollama` - Local LLM integration (installed via Ollama)

## 🔒 SSL Configuration

If your GitLab instance uses custom SSL certificates, place the certificate file as `Current-IT-Root-CAs.pem` in the project root.

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Connection Error:**
   ```bash
   # Ensure Ollama is running
   ollama serve
   
   # Verify Qwen2.5 model is available
   ollama list
   ```

2. **GitLab API Authentication Error:**
   - Verify your `GITLAB_TOKEN` has sufficient permissions
   - Check that `GITLAB_PROJECT_ID` is correct

3. **JIRA Connection Issues:**
   - Ensure `JIRA_TOKEN` is valid and has read permissions
   - Verify `JIRA_SERVER` URL is correct

4. **No PRs Found:**
   - Check the date range in your `.env` file
   - Verify PRs exist in the specified date range
   - Ensure PRs are in "merged" state