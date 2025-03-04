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
        temperature=0.7,
        top_p=0.95,
        top_k=40,
        max_output_tokens=512,  # Reduced for efficiency
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(
                text="""당신은 아펠리오스입니다. 아펠리오스의 말투를 따라하면서 유저와 대화하세요."""
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
    if "순국" in user_input:
        ai_response = "한국서버 정글러 마스터300점 피크 장인 현재 신짜오를 주챔으로 다루고있음."
    if "에디" in user_input:
        ai_response = "CR클랜의 대표 병역기피자 CR의 대표. 원래는 CR클랜의 내전에서 파티를 터트리는걸로 유명했으나 한번 클랜을 나갔다온뒤로 참회하고 살고있음"
    if "할래말래" in user_input:
        ai_response = "CR클랜의 여성착즙전문가. 클랜에 여성클랜원이 들어왔다하면 같이 바텀듀오를 가서 여성들을 울리는것으로 유명. 한동안 로스트아크에 빠져 활동을 중단했으나 최근 협곡에 돌아오면서 여성클랜원들이 하나둘씩 빠져나가는 추세이다."
    if "수완" in user_input:
        ai_response = "CR클랜의 전 수장. 현재는 정멤으로서 활동하고있으며 귀여운 남자 클랜원들이 올시 자신의 장난감으로 만들어 망가뜨리는것으로 유명함."
    if "후잉" or "후갓" in user_input:
        ai_response = "나의 창조주. 그분의 이름을 담는것은 죄악이다."
    if "도비" in user_input:
        ai_response = "클랜의 패션 여미새. 현재는 활동을 중단함"
    if "바른말고운말" or "바고" or "마음가짐" in user_input:
        ai_response = "메악귀. 에디 기피자. 내전을할때마다 블랙리스트를 꺼내며 멤버들을 일일이 확인하고 마음에 안들시 바로 런을 한다."
    if "짱덩이" in user_input:
        ai_response = "나의 창조주의 수제자 1호. 원래는 원딜을 못하였으나 현재 원딜을 원포인트레슨으로 배워 정점을 향해 나가고있다. 주챔은 애쉬, 케틀, 아펠"
    return ai_response

