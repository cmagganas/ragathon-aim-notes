from generate_embeddings import meeting_vector_index
from context import create_base_context
import time
import os
import logging
from llama_index import get_response_synthesizer, PromptTemplate, QueryBundle
from llama_index.response_synthesizers import ResponseMode
import re
import time
import unicodedata
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from langchain import hub

def build_email_content(summary, action_items):
    pass

#TODO - Try different embedders / models / prompts
# Note - set your OPEN API key in context.py line 7
def summerize(dir_name):
    logger.info(" Creating Base Context")
    service_context, re_ranker = create_base_context()
    logger.info(" Base Context Created")
    logger.info(" Creating Vector Index")
    storage= meeting_vector_index(dir_name)
    logger.info(" Vector Index Created")

    action_item_template = (
        "Context information is below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "You are assistant manager to help with meeting follow-up and determine actions participants need to do after."
        "You will be provided with the meeting transcript."
        "\nPerform the following tasks:\n1 - Determine topics that are being discussed in the transcript from the meeting, "
        "which is delimited by triple backticks.\nMake each item short title and one sentence summary."
        "\n\nFormat your response as a list of topics separated by commas.\n"
        "2 – Provide list of actions based on the transcript and summary "
        "with participant name and action description as list of actions "
    )

    summary_template = (
        "Context information is below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "You are assistant manager to help with meeting follow-up and you need to summerize meeting transcript."
    )

    action_items_res = ask_ai(service_context, re_ranker, storage, action_item_template)
    summary_template_res = ask_ai(service_context, re_ranker, storage, summary_template)

    return  summary_template_res + action_items_res

def ask_ai(service_context, reranker, index, promt_temp):
    start_time = time.time()

    # pull a chat prompt
    prompt = hub.pull("aim-notes/sum-n-act-eval")

    print(prompt)

    DEFAULT_MOM_TMPL_PROMPT = PromptTemplate(promt_temp)
    response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.REFINE, text_qa_template=DEFAULT_MOM_TMPL_PROMPT, service_context=service_context, use_async=True, verbose=True)
    elapsed_time = time.time() - start_time
    logger.info(f"response_synthesizer: {elapsed_time:.2f} seconds")

    query= "Summarize meeting and share action items?"
    retrieve_re_start_time = time.time()
    query_bundle = QueryBundle(query)
    retrieved = index.as_retriever(similarity_top_k=10).retrieve(query_bundle)
    retrieved_nodes_rank = reranker.postprocess_nodes(retrieved, query_bundle)
    nodes = retrieved_nodes_rank
    logger.info(f"retrieve re-rank: {time.time() - retrieve_re_start_time:.2f} seconds")
    logger.info(f'Retrieved chunks: {nodes}')
    try:
        response_synthesizer_start_time = time.time()
        response = response_synthesizer.get_response(
                        query,
                        [node.text for node in nodes]
                   )
        logger.info(f"response_synthesizer : {time.time() - response_synthesizer_start_time:.2f} seconds")
    except Exception as e:
        logger.error(f'Error occurred, while getting response: {e}')
    logger.info(f'response: {response}')
    response = response.replace('\n', '<br>')
    logger.info(f"Processing time: {elapsed_time:.2f} seconds")
    return response

