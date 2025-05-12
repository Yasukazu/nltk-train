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

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)
breakpoint()
line_break = completion.choices[0].message.content.find("\n")
print(completion.choices[0].message.content[:line_break])
print(completion.choices[0].message.content[line_break:])
print(completion.choices[0].message.content)
print(completion.choices[0].message)
