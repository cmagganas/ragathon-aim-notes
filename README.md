# Ragathon-AIM Notes: Streamlining Meetings with AI
LlamaIndex - FutureProof Labs RAG Hackathon 2024: Action Item Meeting Notes

## About the Project

### Overview
Ragathon-AIM Notes transforms tedious meeting processes into streamlined, actionable insights using AI. Born from the need to enhance meeting efficiency, this tool automates minutes, prioritizes tasks, and generates clear action items, revolutionizing team collaboration.

### Setup

1. Clone the repository to your local machine:

   ```bash
   git clone <repository-url>
   cd path-to-repository
   pip install -r requirements.txt
   API_KEY = "your_open_api_key_here"
   python main.py
   ```
2. main.py
    * TODO - Try different embedders / models / prompts
    * Note - set your OPEN API key in context.py line 7

### Built with
- **Python:** For backend logic and AI model integration.
- **Llama-index:** To efficiently index and search through meeting transcripts.
- **Whisper:** For accurate audio transcription.
- **Streamlit:** To create an intuitive user interface.
- **OpenAI:** Leveraging AI for summarization and task extraction.

### Development Journey
Our exploration into AI's potential to optimize meeting workflows led to significant discoveries about language processing and user-centric design. We learned to balance AI's analytical prowess with the intricacies of human dialogue, ensuring our summaries and tasks are both accurate and actionable.

### Key Features
- **Efficient Summaries:** Condenses meetings into precise, informative overviews.
- **Automated Task Lists:** Extracts and assigns tasks directly from discussions.
- **Priority Sorting:** Identifies and categorizes tasks by urgency, streamlining focus.

### Challenges & Solutions
Adapting AI to navigate diverse conversational nuances was challenging. We iteratively refined our models for better accuracy and integrated feedback loops for continuous improvement. Handling large audio files efficiently prompted us to develop a robust chunking and transcription process, ensuring scalability.

## Impact
Ragathon-AIM Notes offers a smarter way to capture the essence of meetings, turning discussions into defined paths forward. It's a testament to how AI can elevate operational efficiency and team dynamics.

### Example Output
```
# Summary:
Staff concerns over parking led to proposed priority and visitor parking solutions. A new team member, Jason, was introduced. Discussions on boosting morale with team activities and addressing IT and cleanliness issues were pivotal. A financial downturn highlights the need for strategic sales improvements.

# To Do | Resolved
🟡 Jason: Introduce to team. | ✅ (Completed during meeting)
```

Ragathon-AIM Notes is not just a tool; it's a new paradigm for productive meetings, proving that with the right technology, even the most mundane tasks can be transformed into opportunities for efficiency and innovation.
