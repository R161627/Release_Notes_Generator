from langchain_ollama import ChatOllama
from AI.prompt import generate_executive_summary_prompt, changelog_prompt

llm = ChatOllama(model="qwen2.5", temperature=0.3)

def release_notes_summarization(prs):
    """
    prs: List of PR dictionaries. Each PR can optionally have 'jira_details'.
    """
    pr_text_list = []
    for pr in prs:
        iid = pr.get('iid', 'N/A')
        title = pr.get('title', 'No Title')
        description = pr.get('description', '')
        entry = f"- {title} (#{iid})\n  Description: {description}"
        pr_text_list.append(entry)
    pr_text = "\n".join(pr_text_list)
    jira_text_list = []
    for pr in prs:
        jira = pr.get('jira_details')
        if jira:
            summary = jira.get('summary', 'No Summary')
            issue_type = jira.get('issue_type', 'Task')
            key = jira.get('key', 'Unknown-ID')
            desc = jira.get('description', '')
            jira_line = f"- {summary} ({issue_type}) [{key}]"
            if desc:
                jira_line += f": {desc[:200]}..."
            jira_text_list.append(jira_line)
    jira_text = "\n".join(jira_text_list)

    executive_prompt = generate_executive_summary_prompt(pr_text, jira_text)
    changelog_prompt_text = changelog_prompt(pr_text, jira_text)

    exec_response = llm.invoke(executive_prompt)
    changelog_response = llm.invoke(changelog_prompt_text)

    return exec_response.content, changelog_response.content