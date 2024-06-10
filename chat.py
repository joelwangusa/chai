import model
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

# Define the configuration model for inputs
class InputModel(BaseModel):
    user_name: str
    bot_name: str
    memory: str
    chat_history: str
    input_text: str

# Example usage of model.CustomModelLLM and model.CustomModelConfig
config = model.CustomModelConfig(
    api_url="https://guanaco-submitter.chai-research.com/endpoints/onsite/chat",
    api_key="CR_6700b8e747434541924772becb8fa85a"
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

# Function to run the sequence manually
def run_sequence(inputs):
    # Validate inputs using InputModel
    input_data = InputModel(**inputs)
    # Format the prompt using the template
    prompt = prompt_template.format(**input_data.dict())
    # Call the model with the formatted prompt
    response = model_instance._call(prompt)
    return {"response": response}

# Example chat history
chat_history = [
    {"sender": "Bot", "message": "Hi there"},
    {"sender": "User", "message": "Hey Bot!"}
]

# Convert chat history to string format
chat_history_str = "\n".join(f"{msg['sender']}: {msg['message']}" for msg in chat_history)

# Run the sequence with an example input
input_text = "What's the weather like today?"
result = run_sequence({
    "user_name": "User",
    "bot_name": "Bot",
    "memory": "I am Bot, and this is my mind.",
    "chat_history": chat_history_str,
    "input_text": input_text
})

print(result["response"])