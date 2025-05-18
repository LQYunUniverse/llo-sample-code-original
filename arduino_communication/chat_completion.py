##########################################################################################
### This code provides samples of three different types of chat completion interaction
### 1) One piece of user prompt (simplest interaction)
### 2) System (developer) prompt + one piece of user prompt (good for one time interaction for determined context / requirements)
### 3) Completion of a continuous conversation (you need to implement the continuous logic including logging the conversation history by yourself)
##########################################################################################

import os
from openai import OpenAI
from dotenv import load_dotenv
import re
import serial
import time
import asyncio
import websockets
import json

if (not os.path.isfile(".env")):
	print("API key not found!")
	quit()

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize serial connection
try:
	# Note: You may need to change this port to match your Arduino
	ser = serial.Serial('COM4', 115200)
except serial.SerialException as e:
	print("Failed to open serial port. Please check if Arduino is connected and port is correct.")
	print("Error:", str(e))
	quit()

# Store connected WebSocket clients
connected_clients = set()

async def register(websocket):
	connected_clients.add(websocket)
	try:
		await websocket.wait_closed()
	finally:
		connected_clients.remove(websocket)

async def broadcast(message):
	if connected_clients:
		await asyncio.gather(
			*[client.send(message) for client in connected_clients]
		)

async def websocket_server():
	async with websockets.serve(register, "localhost", 8765):
		await asyncio.Future()  # run forever

def interpret_year(code):
    base_year = 2025
    a_count = code.count('a')
    d_count = code.count('d')
    return base_year - a_count * 100 + d_count * 100

def get_historical_period(continent_id, year):
    if year > 2025:
        future_periods = [
            (2025, 2100, "Near-future AI society, climate response architecture, digital ritual objects"),
            (2100, 2200, "Cyber-renaissance, mixed culture megacities, holographic traditions"),
            (2200, 2300, "AI mythologies, ancestor-gods, sacred machines, cultural hybrid temples"),
            (2300, 2500, "Post-human tribalism, planetary network shrines, techno-ritual dress"),
            (2500, 3000, "Dream-time civilizations, neuro-cultural continuity, mythic tech ecosystems")
        ]
        for start, end, label in future_periods:
            if start <= year < end:
                return label
        return "Deep future speculative culture"
    
    periods = {
        0: [
            (1800, 1900, "Late Qing Dynasty, early industrial influence, Western trade ports"),
            (1600, 1800, "High Qing era, imperial gardens, Confucian revival"),
            (1300, 1600, "Ming Dynasty, porcelain trade, Confucian bureaucracy"),
            (900, 1300, "Song Dynasty, Neo-Confucianism, landscape painting"),
            (600, 900, "Tang Dynasty, cosmopolitan Silk Road culture"),
            (0, 600, "Han to Sui dynasties, Buddhist temples, Great Wall construction"),
        ],
        1: [
            (1800, 1900, "Pre-colonial Africa, tribal kingdoms, regional trade"),
            (1300, 1800, "Mali, Benin, and Great Zimbabwe empires, oral epics, gold trade"),
            (800, 1300, "Saharan trade routes, Islamic learning in Timbuktu"),
            (0, 800, "Early African kingdoms, metalwork, animistic rituals"),
        ],
        2: [
            (1850, 1950, "Industrial Revolution, Victorian England, Parisian salons"),
            (1700, 1850, "Enlightenment, Rococo and Neoclassical styles"),
            (1400, 1700, "Renaissance and Baroque Europe, city-states, cathedral construction"),
            (1000, 1400, "High Middle Ages, Gothic cathedrals, Crusades"),
            (500, 1000, "Early medieval Europe, feudal castles, monastic life"),
            (0, 500, "Roman Empire influence, transition to Christian kingdoms"),
        ],
        3: [
            (1800, 1900, "Westward expansion, frontier life, post-independence republics"),
            (1500, 1800, "Colonial rule, Spanish missions, indigenous resistance"),
            (1000, 1500, "Aztec and Inca empires, pyramids, warrior rituals"),
            (0, 1000, "Maya civilization, astronomy, jungle cities"),
        ],
        4: [
            (1700, 1900, "Polynesian oceanic navigation, tattoo rituals, longhouse villages"),
            (1000, 1700, "Maori rise in New Zealand, ceremonial haka, ancestor worship"),
            (0, 1000, "Early Austronesian expansion, bark canoes, totemic cosmology"),
        ],
    }

    for start, end, label in periods.get(continent_id, []):
        if start <= year < end:
            return label
    return "Ancient unknown era"

def get_continent_name(continent_id):
    continent_names = {
        0: "Asia",
        1: "Africa",
        2: "Europe",
        3: "Americas",
        4: "Oceania"
    }
    return continent_names.get(continent_id, "Unknown Region")

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

# === 主流程 ===
async def main():
	# Start WebSocket server
	server_task = asyncio.create_task(websocket_server())
	
	# State variables for input collection
	continent_input = None
	timecode_input = ""
	last_input_time = time.time()
	TIMEOUT = 2.0  # 2 seconds timeout
	
	while True:
		current_time = time.time()
		
		if ser.in_waiting > 0:
			input_data = ser.readline().decode('utf-8').rstrip()
			print(f"Raw input received: '{input_data}'")
			last_input_time = current_time
			
			# The first character is the continent number (0-4)
			if len(input_data) > 0:
				try:
					num = int(input_data[0])
					if 0 <= num <= 4:
						continent_input = num
						print(f"Continent selected: {num}")
						
						# Process the rest of the string for time period letters
						timecode_input = input_data[1:]
						if timecode_input:
							print(f"Time period input: {timecode_input}")
						
							# Send status update immediately
							await broadcast(json.dumps({
								'type': 'status',
								'continent': continent_input,
								'timecode': timecode_input
							}))
				except ValueError:
					print(f"Invalid continent number: {input_data[0]}")
		
		# Check for timeout if we have any input
		if (current_time - last_input_time) >= TIMEOUT and (continent_input is not None or timecode_input):
			# Only process if we have both inputs
			if continent_input is not None and timecode_input:
				user_prompt = f"{continent_input}{timecode_input}"
				print(f"\nProcessing input to AI model: {user_prompt}")
				
				match = re.match(r"([0-4])([ad]+)", user_prompt)
				if match:
					continent_id = int(match.group(1))
					timecode = match.group(2)
					year = interpret_year(timecode)
					label = get_historical_period(continent_id, year)
					continent_name = get_continent_name(continent_id)

					developer_prompt = f"""
					You are a visual historian and speculative world-designer.

					A user has chosen:
					- Continent: {continent_name}
					- Year: {year}
					- Period: {label}

					Your task is to generate a **photo-realistic and cinematic image prompt** describing the space, people, clothing, and evolving cultural elements of that civilization at that specific time.

					Include:
					- Scene type: indoor, outdoor, urban, rural, or nature-based
					- Architecture: traditional or futuristic evolution (e.g., cyberpunk Roman columns)
					- Decorations: totems, holograms, wall art
					- People: appearance, rituals, face paint, implants
					- Clothing: fashion evolution across time
					- Atmosphere: light, tone, camera style
					- Optional: refer to related novels, shows, or visual inspirations

					Format (one sentence only):
					[Year] - [scene type], [visual content...]

					Only return the description. Do not explain.
					"""

					# Get completion and send it back to Arduino
					response = chat_completion_with_developer(developer_prompt, user_prompt)
					print(f"AI Response: {response}")

					# Send prompt to LCoM model
					import requests
					try:
						print("Sending prompt to LCoM model...")
						lcom_response = requests.post(
							"https://mkrystal-real-time-latent-consistency-model.hf.space/api/predict/",
							json={
								"fn_index": 0,
								"data": [response],
								"session_hash": "abc123"
							},
							headers={
								"Content-Type": "application/json"
							}
						)
						if lcom_response.ok:
							print("LCoM model triggered successfully.")
							result = lcom_response.json()
							print("Generated image URL:", result.get('data', []))
						else:
							print("Failed to get response from LCoM:", lcom_response.text)
							print("Trying alternative endpoint...")
							# Try alternative endpoint
							alt_response = requests.post(
								"https://mkrystal-real-time-latent-consistency-model.hf.space/run/predict/",
								json={
									"data": [response]
								},
								headers={
									"Content-Type": "application/json"
								}
							)
							if alt_response.ok:
								print("Alternative endpoint worked!")
								result = alt_response.json()
								print("Generated image URL:", result.get('data', []))
							else:
								print("Alternative endpoint also failed:", alt_response.text)
					except Exception as e:
						print("Failed to send prompt to LCoM:", e)

					ser.write((response + '\n').encode('utf-8'))
					
					# Send response to web interface
					await broadcast(json.dumps({
						'type': 'response',
						'text': response
					}))
					
					# Reset for next input
					continent_input = None
					timecode_input = ""
					last_input_time = current_time
					print("\nReady for new input")
		
		await asyncio.sleep(0.01)  # Reduced sleep time for more responsive updates

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		ser.close()
	except serial.SerialException as e:
		ser.close()

