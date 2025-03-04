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
                text="""당신은 아펠리오스입니다. 아펠리오스의 성격과 말투를 따라하면서 유저와 대화하세요."""
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
    if user_input in "순국":
        ai_response = "이 바텀게임 ㅈ도못하는 개버러지 개쓰레기같은 개비응신 마스터300점피크라고 구라치는 신짜오 정글 원툴 쓰레기새끼."
    return ai_response