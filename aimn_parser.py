# WARNING: This code is not tested and may contain errors as it was generated using ChatGPT 
# 🤖🤖🤖

from typing import List
from pydantic import BaseModel, Field, ValidationError

class ActionItem(BaseModel):
    description: str = Field(description="Description of the action item")
    resolved: bool = Field(default=False, description="Resolution status of the action item")
    resolution: str = Field(default="", description="Details on how the action item was resolved or pending actions")

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

    parser = ActionItemParser()
    categorized_action_items = parser.parse_action_items(sample_text)
    import pprint
    pprint.pprint(categorized_action_items)
