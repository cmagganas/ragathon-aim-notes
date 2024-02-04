import logging
import os
import shutil
import streamlit as st
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from generate_embeddings import construct_index, PERSIST_DIR
from main import ask_ai, create_base_context

def process_uploaded_files(user_dir, uploaded_file):
    print("user_dir :: ",user_dir)
    print("uploaded_file :: ",uploaded_file)

    os.makedirs(user_dir, exist_ok=True)
    target_file_path = os.path.join(user_dir, uploaded_file.name)
    with open(target_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

def main():
    st.title("Minutes of meeting")
    st.markdown(
        "Minutes of meeting summary and action items"
    )

    # if prompt := st.chat_input("How may I help you?"):
    #     st.chat_message("user").markdown(prompt)
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #     with st.spinner("Generating Response..."):
    #         response = f": {ask_ai(st.session_state.service_context, prompt, st.session_state.reranker, index_dir)}"
    #         response = process_code_blocks(response)
    #         with st.chat_message("assistant"):
    #             st.markdown(response, unsafe_allow_html=True)
    #
    #     st.session_state.messages.append({"role": "assistant", "content": response})

    uploaded_files = st.file_uploader('Choose document to upload', type=['mp3', 'mp4'])
    if uploaded_files:
        with st.spinner("Processing uploaded file..."):
            raw_file_directory_path ="mom"
            process_uploaded_files(raw_file_directory_path, uploaded_files)
            storage = construct_index(raw_file_directory_path)

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
            service_context, re_ranker = create_base_context()
            action_items_res = ask_ai(service_context, re_ranker, storage, action_item_template)
            summary_template_res = ask_ai(service_context, re_ranker, storage, summary_template)
            st.write("Summary:\n")
            st.markdown(summary_template_res, unsafe_allow_html=True)
            st.write("Action Items:\n")
            st.markdown(action_items_res, unsafe_allow_html=True)


            shutil.rmtree(raw_file_directory_path, ignore_errors=True)
            st.markdown('''<style>
                        .uploadedFile {display: none}
                        .streamlit-paginator {display: none}
                        <style>''', unsafe_allow_html=True)

if __name__ == "__main__":
    st.markdown( '''<style>
                    div[data-testid="stToolbar"] {
                        display: none !important;
                    }
                </style>
                ''', unsafe_allow_html=True)
    main()