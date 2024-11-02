from openai import OpenAI

# Inicjalizacja klienta API z kluczem
client = OpenAI(api_key="your_openai_api_key")

# Stworzenie wiadomości z zapytaniem
chat_completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ],
  max_tokens = 400,
  temperature = 0.3
)

# Wyświetlenie odpowiedzi
print(chat_completion.choices[0].message.content)
