import os,json
from dotenv import load_dotenv
from Data.merge_requests import fetch_merge_requests, save_to_file
from AI.summarization import release_notes_summarization
load_dotenv()
def main():
    START = os.getenv("START_DATE")
    END = os.getenv("END_DATE")

    if not START or not END:
        raise ValueError("START_DATE and END_DATE must be set in .env file")

    print(f"🔍 Fetching PRs from {START} to {END}...")
    prs = fetch_merge_requests(START, END, include_diff=True)
    save_to_file(prs, filename="gitlab_prs.json")
    print("📁 Saved raw PR + Jira JSON to Data/gitlab_prs.json")
    print("🧠 Generating Release Notes using LLM...")

    with open("gitlab_prs.json") as f:
        pr_list = json.load(f)  # pr_list now contains dicts

    executive_summary, technical_changelog = release_notes_summarization(pr_list)
    output_file = "Release_Notes.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 🚀 Release Notes\n\n")
        f.write("## Executive Summary\n\n")
        f.write(executive_summary)
        f.write("\n\n## Technical Changelog\n\n")
        f.write(technical_changelog)
    print(f"✅ Release Notes generated successfully → {output_file}")
if __name__ == "__main__":
    main()