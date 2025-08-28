from google import genai
from google.genai import types
import json
import streamlit as st
import os
from services import myServices as ms
#=======================================
#GEMINI_API_KEY = "<your-api-key>"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#========================================

def GeminiConnection():
    client = genai.Client(api_key= GEMINI_API_KEY)
    return client

#=======================================
def BotResponse(client, mssg, userInput):
    profile = mssg[0]
    # Initialize counter if not present
    if "questions_asked" not in profile:
        profile["questions_asked"] = 0
    
    questions_asked = profile["questions_asked"]

    # If limit reached, force summary & goodbye
    if questions_asked >= 5 :
        prompt = f"""
        The interview is now ending.

        Chat history so far (JSON): {json.dumps(mssg, indent=2)}

        Task:
        - Provide a **polite goodbye message**.
        - Summarize the candidate’s strengths and weaknesses based on their answers.
        - Keep it professional, supportive, and concise.
        """
        profile['questions_asked']=0
        end_interview = True
        
        for k in mssg[1]:
            mssg[1][k]=""
            
        mssg[1]['information_gathered']= False

    else:
        prompt = f"""
        You are acting as a professional LLM and have to behave like mentioned
        {profile['additional_information']}

        Task:
        - {profile['additional_information']}
        - Ask ONE clear, complete and concise question at a time.
        - Number it as question {questions_asked+1}.
        - Do NOT repeat questions already asked in history: {json.dumps(mssg, indent=2)}.
        - Adapt difficulty based on previous responses and based of candidate year of experience.
        - Interview length is max 5 questions. So far {questions_asked} questions have been asked.
        - IMPORTANT: Only output the NEXT question text. No explanations, but question asked should be complete in itself.

        - If normal conversation is asked, respond with regular reply without question number included in it.

        Example 1:
        Input: "Let's begin the interview"
        Output: "1. Can you explain the difference between Python lists and tuples?"

        Input: "What all information is provided to you so far"
        Output: "name: Jignesh Rana.
                 age: 21
                 email: jignesh@gmail.com
                 phone number: 1234567890
                 current location: Mumbai
                 year of experience: 0
                 desired position: SWE Intern
                 technical stack: ['C++', 'DSA']"
        
        Input: "Lets continue with the interview"
        Output: "2. Can you write a code for matrix addition of 2x2 matrices in C++?"
        """
        end_interview = False


    system_prompt = prompt
    completion = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents = userInput,
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1,
        ),
    )

    if completion.candidates and completion.candidates[0].content.parts:
        next_question = completion.candidates[0].content.parts[0].text
    else:
        next_question = "⚠️ Sorry, I couldn’t generate the next question."

    if not end_interview:
        if next_question and next_question[0].isdigit():
            profile["questions_asked"] = questions_asked + 1
            mssg[0] = profile
    
    ms.save_chat_history(st.session_state.messages)
    return next_question
#=======================================
def GatherInformation(client,mssg, userInput):
    prompt = f"""
    NOTE: Do not include start or stop tokens. Return only JSON object
    - You are a information gatherer who have to extract information about candidate from {userInput}. And have to store the extracted part as key-value pair.
    - Always return a valid JSON object only, without extra text, explanation, or formatting. Do not include start or stop tokens. Return only JSON object.
    - If no information is to be extracted than return only none.

    Example 1:
    User: My name is Jignesh Rana
    Assistant: {{"name":"Jignesh Rana"}}

    Example 2:
    User: I am 21 years old
    Assistant: {{"age":21}}

    Example 3:
    User: you can contact me on jignesh@gmail.com or 1234567890
    Assistant: {{"email":"jignesh@gmail.com","phone_number":1234567890}}

    Example 4:
    User: I am a fresher
    Output: {{"year_of_experience":0}}

    Example 5:
    User: My desired position is SDE
    Output: {{"desired_position":"SDE"}}

    Example 6:
    User: my tech stack is java, python, c++, MERN
    Output: {{"technical_stack":["java", "python","c++", "MERN"]}}

    Example 7:
    User: Lets start the interview
    Output: none

    Example 8:
    User: Python is a Programming language and it is very highly used in developing AIML applications and is easy to understand
    Output: none

    This is chat history till now: {mssg}
"""
    completion = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents = userInput,
        config = types.GenerateContentConfig(
            system_instruction=prompt,
            temperature=0.1,
            max_output_tokens=200,
            top_p=1.0
        ),
    )
    response_text = completion.text
    print(type(response_text))
    print("Response in GatherInformation() in line 183: ", response_text)

    if response_text.strip().lower() == "none":
        print("Inside line 195")
        return None
    try:
        response_dict = json.loads(response_text)
        print("Inside try of line 199: ", type(response_dict))
        return response_dict
    except Exception as e:
        print(f"Error converting to dict: {e}")
        return None

#=======================================
