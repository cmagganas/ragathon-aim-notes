from langchain.embeddings import HuggingFaceBgeEmbeddings
from llama_index import LLMPredictor, PromptHelper, ServiceContext
from llama_index.indices.postprocessor import SentenceTransformerRerank
import os
from langchain_community.llms import OpenAI
## Add your key here
os.environ["OPENAI_API_KEY"] ="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"
os.environ["TOKENIZERS_PARALLELISM"] ="true"

llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.5)

def create_base_context():
    model_name = "BAAI/bge-large-en"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    service_context = ServiceContext.from_defaults(llm=llm,
                                                   embed_model=embeddings)
    re_ranker = SentenceTransformerRerank(model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=2)

    return service_context, re_ranker