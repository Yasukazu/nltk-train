import dotenv
from openai import OpenAI
from pathlib import Path

secret_fullpath = Path("/etc/secrets/.env")
config = dotenv.dotenv_values(secret_fullpath)
openai_client_key = config["OPENAI_API_KEY"]
assert openai_client_key, "OPENAI_API_KEY not found in .env file"
client = OpenAI(
  api_key=openai_client_key
)
# Initialize conversation history
messages = [
    {"role": "system", "content": "You are an experienced engineer."},
    {"role": "user", "content": "How do you think about nuclear power plants?"} # Say something to cheer up an elder person.
]
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=messages
)
breakpoint()
# Append assistant's response to the conversation
assistant_response = completion.choices[0].message.content
messages.append({"role": "assistant", "content": assistant_response})

# Print the response
print(assistant_response)

# Continue the conversation
messages.append({"role": "user", "content": "what do you think about the future of nuclear power plants?"})
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=messages
)

# Append and print the next response
assistant_response = completion.choices[0].message.content
messages.append({"role": "assistant", "content": assistant_response})
print(assistant_response)
