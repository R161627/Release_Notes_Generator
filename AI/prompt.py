def generate_executive_summary_prompt(pr_list, jira_list):
    """
    pr_list: List of dicts with PR info: [{'title': ..., 'labels': ..., 'id': ...}, ...]
    jira_list: List of dicts with Jira info: [{'summary': ..., 'type': ..., 'status': ...}, ...]
    """

    prompt = f"""
                You are a technical writer creating an executive summary for a software release notes document.
                Release Version: xxxxx
                Release Date: xxxxxx
                The release includes the following changes:
                Pull Requests: {pr_list}
                Jira Tickets: {jira_list}
                Task:
                Write a **concise executive summary** suitable for senior management. 
                    - Highlight key new features, important fixes, and critical security updates.
                    - Keep it short, professional, and easy to read.
                    - Avoid technical details like code, diffs, or PR numbers unless necessary.
                    - Emphasize business impact or improvements to user experience and system reliability.
                Output format:
                1-2 short paragraphs summarizing the release.
            """
    return prompt

def changelog_prompt(pr_list, jira_list):
    """
    Generates a detailed technical changelog in Markdown.
    """
    prompt = f"""
                You are generating a Markdown technical changelog for the release.
                Use the following data:
                Pull Requests: {pr_list}
                Jira Tickets: {jira_list}
                Instructions:
                    - Group changes into categories: 🚀 New Features, 🐛 Bug Fixes, ⚡ Performance & Improvements, Security.
                    - Include PR ID or Jira ID in parentheses.
                    - Use bullet points with concise, clear descriptions.
                    - Output ready-to-paste Markdown suitable for release notes.
            """
    return prompt