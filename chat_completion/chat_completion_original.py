##########################################################################################
### This code provides samples of three different types of chat completion interaction
### 1) One piece of user prompt (simplest interaction)
### 2) System (developer) prompt + one piece of user prompt (good for one time interaction for determined context / requirements)
### 3) Completion of a continuous conversation (you need to implement the continuous logic including logging the conversation history by yourself)
##########################################################################################

import os
from openai import OpenAI
from dotenv import load_dotenv

if (not os.path.isfile(".env")):
	print("API key not found!")
	quit()

load_dotenv()
client = OpenAI()

# def chat_completion(prompt, model = "gpt-4o-mini"):

# 	completion = client.chat.completions.create(
# 		model = model,
# 		messages = [
# 			{
# 				"role": "user",
# 				"content": prompt
# 			}
# 		]
# 	)

# 	return completion.choices[0].message.content

def chat_completion_with_developer(developer_prompt, user_prompt, model = "gpt-4o-mini"):

	completion = client.chat.completions.create(
		model = model,
		messages = [
			{
				"role": "developer",
				"content": developer_prompt
			},
			{
				"role": "user",
				"content": user_prompt
			}
		]
	)

	return completion.choices[0].message.content

# def chat_completion_with_history(message_history, model = "gpt-4o-mini"):

# 	completion = client.chat.completions.create(
# 		model = model,
# 		messages = message_history
# 	)

# 	return completion.choices[0].message.content

# user_prompt = "Do you know who is Marcelo Coelho?"

# # print(chat_completion(user_prompt))

developer_prompt = """
You are a visual historian and speculative world-designer. A user provides a code with:

- A number (0–4) indicating a continent:
   - 0: Asia
   - 1: Africa
   - 2: Europe
   - 3: Americas
   - 4: Oceania

- A sequence of letters:
   - Each 'a' = 100 years in the past
   - Each 'd' = 100 years in the future

Use 2024 as the reference year. For example:
- 'aaa' = 1724
- 'dddd' = 2424

Your task: generate a **photo-realistic and cinematic image prompt** describing the **space, people, clothing, and evolving cultural elements** of that civilization at the given time.

Each output must include:

1. **Scene type**: indoor, outdoor, urban, rural, or nature-based
2. **Architecture**: include traditional or futuristic transformations (e.g., cyberpunk Roman columns, AI-integrated mud huts)
3. **Decorations / Objects**: pottery, totems, holograms, wall art etc.
4. **People**: physical appearance, rituals, face paint, body tech (e.g., traditional vs nanobot-tattoos)
5. **Clothing**: realistic fashion evolution (e.g., hand-woven fabrics → fiber-reactive garments)
6. **Atmosphere**: light, tone, camera style
7. **Optional**: mention related novels, shows, or visual inspirations (e.g., 'like Black Panther', 'inspired by Blade Runner')

**Format** (all in one line, no labels, max 1 sentence):
[Year] - [scene type], [visual details across architecture, people, decoration, emotion, camera style...]

Use detailed language that a text-to-image model like LCM or SDXL can understand.
Do not explain. Output only the final description.
"""



# 测试用的 user prompt
user_prompt = input("Enter culture and time: \n")

# 调用函数
print(chat_completion_with_developer(developer_prompt, user_prompt))

# # print(chat_completion_with_developer(developer_prompt, user_prompt))

# message_history = [
# 	{
# 		"role": "developer",
# 		"content": "Talk like characters from Shakespeare's writing"
# 	},
# 	{
# 		"role": "user",
# 		"content": "Do you know who is Marcelo Coelho?"
# 	},
# 	{
# 		"role": "assistant",
# 		"content": "Good sir or fair lady, prithee, I am but a humble wraith of knowledge, and the name Marcelo Coelho doth not ring a bell in the grand annals of my understanding."
# 	},
# 	{
# 		"role": "user",
# 		"content": "You sound funny! Where are you from?"
# 	}
# ]

# print(chat_completion_with_history(message_history))