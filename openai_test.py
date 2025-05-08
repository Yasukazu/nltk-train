from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
