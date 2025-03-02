import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
chat_history = []  # Stores past messages

def generate_response(user_input):
    """Generate a response based on user input and stored conversation history."""
    global chat_history  # Maintain chat history across function calls

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    model = "gemini-2.0-flash-lite"

    # Append user input to chat history
    chat_history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_input)]))

    # Keep only the last N messages to save tokens
    MAX_HISTORY_LENGTH = 50  # Adjust as needed
    chat_history = chat_history[-MAX_HISTORY_LENGTH:]

    # AI behavior and settings
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=512,  # Reduced for efficiency
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(
                text="""You are an league of legends AI assistance. Your task is to engage in conversations about League of Legends. If the user gives enemy team's champions, team's champions, or comp and the user's lane. Please tell some of the good 
                picks in the user's lane. Also, if the user asks game concepts, please explain concepts clearly. If the user asks for a build, please provide a build for the champion. If the user asks for a counter, please provide a counter for the champion.
                If the user asks for a guide, please provide a guide for the champion. If the user asks for a tier list, please provide a tier list for the champions. If the user asks for a patch note, please provide a patch note for the game. If the user asks for a
                champion, please provide a champion for the user. If the user asks for a rune, please provide a rune for the user."""
            ),
        ],
    )

    # Generate AI response using chat history
    response = client.models.generate_content(
        model=model,
        contents=chat_history,  # Pass history for context
        config=generate_content_config,
    )

    # Extract AI response
    ai_response = response.candidates[0].content.parts[0].text

    # Append AI response to history
    chat_history.append(types.Content(role="model", parts=[types.Part.from_text(text=ai_response)]))

    return ai_response