from pydantic import BaseModel
from . import model
from langchain.prompts import PromptTemplate
from gensim.summarization import summarize

# Define constants
USER_NAME = "Joel Wang"
BOT_NAME = "Chai Bot"
MEMORY = "I am Bot, and this is my mind."

# Define the configuration model for inputs
class InputModel(BaseModel):
    chat_history: str
    input_text: str

# Example usage of model.CustomModelLLM and model.CustomModelConfig
config = model.CustomModelConfig(
    api_url="https://guanaco-submitter.chai-research.com/endpoints/onsite/chat",
    api_key="CR_6700b8e747434541924772becb8fa85a",
    user_name=USER_NAME,
    bot_name=BOT_NAME,
    memory=MEMORY
)

model_instance = model.CustomModelLLM(config=config)

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["user_name", "bot_name", "memory", "chat_history", "input_text"],
    template=(
        "Memory: {memory}\n"
        "Chat history:\n{chat_history}\n"
        "{user_name}: {input_text}\n"
        "{bot_name}:"
    )
)

# Initialize in-memory chat history
# We will save it into database in the future
# TODO - Save chat history into database and fetch it from database when needed such as most recent 10 messages

# TODO: mutiple user, hashtable
chat_history = []

# Function to run the sequence manually
def run_sequence(inputs):
    global chat_history
    # Append new user message to the chat history
    chat_history.append({"sender": USER_NAME, "message": inputs['input_text']})
    # Convert chat history to string format
    chat_history_str = "\n".join(f"{msg['sender']}: {msg['message']}" for msg in chat_history)
    # Update inputs with the complete chat history
    inputs['chat_history'] = chat_history_str
    # Validate inputs using InputModel
    input_data = InputModel(**inputs)
    # Format the prompt using the template
    prompt = prompt_template.format(
        user_name=USER_NAME,
        bot_name=BOT_NAME,
        memory=MEMORY,
        **input_data.dict()
    )
    # Call the model with the formatted prompt
    response = model_instance._call(prompt)
    # Append bot response to chat history
    chat_history.append({"sender": BOT_NAME, "message": response})
    return {"response": response}


# Function to get paginated chat history with simple pagination
def get_chat_history(page: int, size: int):
    start = page * size
    end = start + size
    return chat_history[start:end]

# Function to generate a summary of the conversation so far
def generate_summary(chat_history):
    # Format chat history for the AI model prompt
    conversation = "\n".join(f"{msg['sender']}: {msg['message']}" for msg in chat_history)
    prompt = f"Please summarize the following conversation:\n\n{conversation}\n\nSummary:"
    
    # Call the AI model with the formatted prompt
    summary_response = model_instance._call(prompt)
    
    return summary_response