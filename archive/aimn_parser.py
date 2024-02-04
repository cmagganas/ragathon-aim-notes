# WARNING: This code is not tested and may contain errors as it was generated using ChatGPT 
# 🤖🤖🤖

from typing import List, Literal
from pydantic import BaseModel, Field, ValidationError

class ActionItem(BaseModel):
    """
    This class represents an action item with its description, resolution status, resolution details and priority.
    It is meant to be used as a pydantic model for parsing and validating action items.
    It's format will be used to guide the LLM Extraction model to extract and categorize action items from a given text.
    """
    description: str = Field(description="Description of the action item")
    resolved: bool = Field(default=False, description="Resolution status of the action item")
    resolution: str = Field(default="", description="Details on how the action item was resolved or pending actions")
    priority: Literal["low 🟡", "medium 🟠", "high 🔴", "none ⚪️"] = Field(default="none ⚪️", description="Priority of the action item.\n\ne.g low=🟡 medium=🟠 high=🔴 none=⚪️")

class ActionItemParser:
    @staticmethod
    def parse_action_items(text: str) -> dict[str, List[ActionItem]]:
        categories = {"resolved": [], "pending": []}
        lines = text.split('\n')
        for line in lines:
            if line.startswith("To Do:") or line.startswith("Tasks:"):
                continue  # Skip headers

            # Extract action item description and resolution status
            if "✅" in line:
                resolved = True
                resolution = line.split("✅")[-1].strip(" ()")
            else:
                resolved = False
                resolution = "Pending actions: " + line.split("❌")[-1].strip(" ()") if "❌" in line else ""

            description = line.split(".")[1].strip() if "." in line else line.strip()
            action_item = ActionItem(description=description, resolved=resolved, resolution=resolution)

            # Categorize action item based on its resolution status
            if resolved:
                categories["resolved"].append(action_item)
            else:
                categories["pending"].append(action_item)

        return categories

if __name__ == "__main__":
    # Assume `sample_text` contains the provided sample text to be parsed.
    with open("samples/report-to-parse.txt", "r", encoding="utf-8") as file:
        sample_text = file.read()

    # Line by line parsing with code
    # parser = ActionItemParser()
    # categorized_action_items = parser.parse_action_items(sample_text)
    # import pprint
    # pprint.pprint(categorized_action_items)
    

    # With LLM model extraction
    from langchain.output_parsers import PydanticOutputParser
    from langchain.prompts import PromptTemplate
    from langchain_openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv()

    # Set up a parser for ActionItem
    parser = PydanticOutputParser(pydantic_object=ActionItem)
    prompt_template = PromptTemplate(
        template="Extract and categorize action items from the following text:\n{format_instructions}\n{text}\n",
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    formatted_input = prompt_template.format_prompt(text=sample_text)
    model = OpenAI(temperature=0) 
    output = model(formatted_input.to_string())
    parsed_action_items = parser.invoke(output)
    sample_markdown_format = open("samples/sample_markdown_format.txt", "r", encoding="utf-8").read()
    print(sample_markdown_format)
    final_report = model(f"Using this markdown format:\n{sample_markdown_format}\n\nCreate a final report with the below information:\n{parsed_action_items}")
    print(final_report)