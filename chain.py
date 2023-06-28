from typing import Tuple
from uuid import uuid4
import json
import pinecone
from langchain.vectorstores import Pinecone
from langchain import ConversationChain
from langchain.memory import ConversationBufferMemory, DynamoDBChatMessageHistory
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import messages_to_dict
from transformers import CLIPTokenizerFast, CLIPProcessor, CLIPModel
import torch

import config

def openai_semantic_parse(openai_api_key, memory, qry):
    template = """
    {query_txt}

    What is user asking for and in which location and give me in below output format
    disaster damage type, location name 
    """

    prompt = PromptTemplate(
        input_variables=["query_text"],
        template=template,
    )
    final_prompt = prompt.format(query_text=qry)

    llm = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key)

    response = llm(final_prompt)
    return response



def pinecone_search(pinecone_api_key, llm_response, pinecone_api_env, pinecone_index):
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_api_env)

    index = pinecone.Index(pinecone_index)

    device = "cuda" if torch.cuda.is_available() else \
         ("mps" if torch.backends.mps.is_available() else "cpu")
    model_id = "openai/clip-vit-base-patch32"

    tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
    processor = CLIPProcessor.from_pretrained(model_id)
    model = CLIPModel.from_pretrained(model_id).to(device)

    txt_tokens = tokenizer(llm_response, return_tensors="pt")
    query_emb = model.get_text_features(**txt_tokens)
    result = index.query(query_emb.tolist(), top_k=6, include_metadata=True)
    result_metadata = [x["metadata"] for x in result["matches"]]
    return json.dumps(result_metadata)


def run(openai_api_key: str, pinecone_api_key: str, session_id: str, qry: str) -> Tuple[str, str]:
    """This is the main function that executes the prediction chain.
    Updating this code will change the predictions of the service.
    Current implementation creates a new session id for each run, client
    should pass the returned session id in the next execution run, so the
    conversation chain can load message context from previous execution.

    Args:
        api_key: api key for the LLM service, OpenAI used here
        session_id: session id from the previous execution run, pass blank for first execution
        qry: question entered by the user

    Returns:
        The prediction from LLM
    """
    #Setting Pinecone environment variables
    pinecone_api_env = ''
    pinecone_index = ''
    
    if not session_id:
        session_id = str(uuid4())
    
    chat_memory = DynamoDBChatMessageHistory(
        table_name=config.config.DYNAMODB_TABLE_NAME,
        session_id=session_id
    )
    messages = chat_memory.messages

    # Maintains immutable sessions
    # If previous session was present, create
    # a new session and copy messages, and 
    # generate a new session_id 
    if messages:
        session_id = str(uuid4())
        chat_memory = DynamoDBChatMessageHistory(
            table_name=config.config.DYNAMODB_TABLE_NAME,
            session_id=session_id
        )
        # This is a workaround at the moment. Ideally, this should
        # be added to the DynamoDBChatMessageHistory class
        try:
            messages = messages_to_dict(messages)
            chat_memory.table.put_item(
                Item={"SessionId": session_id, "History": messages}
            )
        except Exception as e:
            print(e)
    
    memory = ConversationBufferMemory(chat_memory=chat_memory, return_messages=True)

    llm_response = openai_semantic_parse(openai_api_key, memory, qry)

    search_response = pinecone_search(pinecone_api_key, llm_response, pinecone_api_env, pinecone_index)
    
    return search_response, session_id

