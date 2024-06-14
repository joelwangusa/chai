from . import model
from langchain.prompts import PromptTemplate
import logging
from collections import defaultdict

# Set up logging
logging.basicConfig(filename='bot_conversations.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Keep the chat history in memory for retriveing chat history
# TODO, will store it into database and retrieve it from there
chat_history_memory = defaultdict(list)

class InputModel:
    def __init__(self, chat_history: str, input_text: str):
        self.chat_history = chat_history
        self.input_text = input_text

class BotConfig:
    def __init__(self, user_name: str, bot_name: str, memory: str, prompt_template: PromptTemplate):
        if not isinstance(prompt_template, PromptTemplate):
            raise ValueError('prompt_template must be an instance of PromptTemplate')
        self.user_name = user_name
        self.bot_name = bot_name
        self.memory = memory
        self.prompt_template = prompt_template

def create_bot_config(user_name: str, bot_name: str, memory: str) -> BotConfig:
    prompt_template = PromptTemplate(
        input_variables=["user_name", "bot_name", "memory", "chat_history", "input_text"],
        template="Memory: {memory}\nChat history:\n{chat_history}\n{user_name}: {input_text}\n{bot_name}:"
    )
    return BotConfig(
        user_name=user_name,
        bot_name=bot_name,
        memory=memory,
        prompt_template=prompt_template
    )

def run_sequence(bot_config: BotConfig, input_text: str, chat_history: list):
    # store the chat history in memory
    chat_history_memory[bot_config.user_name].append({"sender": bot_config.user_name, "message": input_text})
    # Convert chat history to string format
    chat_history_str = "\n".join(f"{msg['sender']}: {msg['message']}" for msg in chat_history)
    # Create InputModel instance
    inputs = InputModel(chat_history=chat_history_str, input_text=input_text)
    # Format the prompt using the template
    prompt = bot_config.prompt_template.format(
        user_name=bot_config.user_name,
        bot_name=bot_config.bot_name,
        memory=bot_config.memory,
        chat_history=inputs.chat_history,
        input_text=inputs.input_text
    )
    # Call the model with the formatted prompt
    response = model_instance._call(prompt)

    # store the chat history in memory
    chat_history_memory[bot_config.user_name].append({"sender": bot_config.bot_name, "message": response})
    # Append bot response to chat history
    chat_history.append({"sender": bot_config.bot_name, "message": response})
    return {"response": response, "chat_history": chat_history}

# Function to get paginated chat history with simple pagination
def get_chat_history(bot_config: BotConfig, page: int, size: int):
    start = page * size
    end = start + size
    return chat_history_memory[bot_config.user_name][start:end]

# Function to generate a summary of the conversation so far
def generate_summary(chat_history):
    # Format chat history for the AI model prompt
    conversation = "\n".join(f"{msg['sender']}: {msg['message']}" for msg in chat_history)
    prompt = f"Please summarize the following conversation:\n\n{conversation}\n\nSummary:"
    
    # Call the AI model with the formatted prompt
    summary_response = model_instance._call(prompt)
    
    return summary_response

# Example usage of model.CustomModelLLM and model.CustomModelConfig
config = model.CustomModelConfig(
    api_url="https://guanaco-submitter.chai-research.com/endpoints/onsite/chat",
    api_key="CR_6700b8e747434541924772becb8fa85a",
    user_name="User",
    bot_name="Bot",
    memory="I am Bot, and this is my mind."
)

model_instance = model.CustomModelLLM(config=config)