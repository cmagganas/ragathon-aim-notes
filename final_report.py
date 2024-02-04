from langchain_openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

class MarkdownReportGenerator:
    def __init__(self):
        self.model = OpenAI(temperature=0) 

    def generate_markdown_report(self, text: str) -> str:
        prompt = f"Generate a detailed markdown report based on the following action items and their descriptions:\n\n{text}\n\nFormat the report with a summary at the top, followed by two columns: 'To Do' for pending tasks and 'Resolved' for completed tasks. Include a priority for each task as a colored circle (🟡 for low, 🟠 for medium, 🔴 for high, ⚪️ for none)."
        return self.model.invoke(prompt)

if __name__ == "__main__":
    # Load the sample report text from a file or any source
    with open("samples/report-to-parse.txt", "r", encoding="utf-8") as file:
        report_text = file.read()
    generator = MarkdownReportGenerator()
    markdown_report = generator.generate_markdown_report(report_text)
    with open("samples/generated-report.md", "w", encoding="utf-8") as file:
        file.write(markdown_report)
    print(markdown_report)