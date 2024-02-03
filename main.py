from generate_embeddings import meeting_vector_index
from context import create_base_context
import time
import logging
from llama_index import get_response_synthesizer, PromptTemplate, QueryBundle
from llama_index.response_synthesizers import ResponseMode
import re
import time
import unicodedata
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#TODO - Try different embedders / models / prompts
# Note - set your OPEN API key in context.py line 7
def summerize(dir_name):
    logger.info(" Creating Base Context")
    service_context, re_ranker = create_base_context()
    logger.info(" Base Context Created")
    logger.info(" Creating Vector Index")
    storage= meeting_vector_index(dir_name)
    logger.info(" Vector Index Created")
    return ask_ai(service_context, re_ranker, storage)

def ask_ai(service_context, reranker, index):
    start_time = time.time()
    DEFAULT_MOM_TMPL = (
        "Context information is below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Your task is to generate a meeting summary out of given transcript and action items."
        # "Use complete output length if needed but don't leave response without closing statement or incomplete sentence, a proper context should end with full stop in end"
    )
    DEFAULT_MOM_TMPL_PROMPT = PromptTemplate(DEFAULT_MOM_TMPL)
    response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.SIMPLE_SUMMARIZE, text_qa_template=DEFAULT_MOM_TMPL_PROMPT, service_context=service_context, use_async=True, verbose=True)
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

print(summerize("recording_01"))