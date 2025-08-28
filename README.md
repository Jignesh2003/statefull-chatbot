# Custom Chatbot Creation Tool
---
## Project Overview
This tool allows users to create custom AI-powered chatbots designed for specific information gathering needs. The platform enables the creation of specialized chatbots that can handle various requirements, such as gathering information or handling additional questions.

[Demo Link](https://drive.google.com/file/d/1YLV1eXFkocSWdVDgNFX25s7NZhbuHPIi/view?usp=drive_link)

Key capabilities:

1. Create chatbots with predefined information gathering objectives
2. Customize conversation flows based on specific requirements
3. Handle technical and non-technical interactions
4. Deploy user-friendly interfaces for both creators and end-users

## Screenshots
<img width="1916" height="884" alt="image" src="https://github.com/user-attachments/assets/1ddf6875-60da-427a-9a8e-b2e7e67cdd9d" />
<img width="1918" height="904" alt="image" src="https://github.com/user-attachments/assets/ef742fec-cea9-402a-aa24-0b9081c07d7a" />

## Installation Instruction
### Setup Steps
1. Clone the repository:
```bash
git clone https://github.com/Jignesh2003/statefull-chatbot.git
cd statefull-chatbot
```
2. Install required dependencies:
```bash
pip install -r requirements.txt
```
3. Set your API KEY (Inside models/Groq_LLM.py)
```bash
GEMINI_API_KEY=your_api_key_here

or

- Locally: create a `.env` file with `GEMINI_API_KEY=your_key_here`
```
4. Launch the application:
```bash
streamlit run app.py
```

### Usage Guide
Creating a New Chatbot
1. Access the main dashboard and select "Create New Chat"
2. Define your chatbot's purpose and information gathering objectives
3. Add any additional data that you want to collect
4. Test your chatbot

### Technical Details
Libraries and Technologies
1. Streamlit: Frontend interface and deployment
2. Gemini API: Powers the large language model
3. JSON: Data Storage Options

### Architecture
The application follows a modular design with these components:
1. Interface Layer: Streamlit-powered UI for chatbot creation and interaction
2. Logic Layer: Python modules for processing inputs, managing context, and handling conversation flow
3. AI Integration: Connection to language models via Gemini API
4. Storage Layer: Data persistence for chatbot configurations and conversation logs

### Model Details
The system primarily leverages gemini-2.5-flash model.

---

## Prompt Design
System prompts:

```bash
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
```

```bash
For your response, you must follow this json schema (The data fields would depend on the information you are collecting):
And message would be passed as a response to the user.

{
      "cbname": "Talent Scout",
      "additional_information": "Based on the user tech stack, ask them 3-5 questions regarding it to judge their proficiency."
    },
    {
      "information_gathered": false,
      "name": "Jignesh Rana",
      "age": 21,
      "email": "jignesh@gmail.com",
      "phone_number": 1234567890,
      "current_location": "Mumbai",
      "year_of_experience": "0",
      "desired_position": "AI Intern",
      "technical_stack": []
    }
    {
      "role": "assistant",
      "content": "\ud83d\udc4b Hi canditate ! I'm Talent Scout. What is your name :)"
    },
    {
      "role": "user",
      "content": "my name is Jignesh Rana"
    }
}
```
---

## Challenges & Solutions

### Challenge 1: Context Management
Problem: Maintaining conversation context across multiple turns while keeping within token limits. Solution: Implemented temporary system prompts to reduce token count for the message history.

### Challenge 2: Consistency in Information Collection
Problem: Ensuring all necessary information is collected even when conversations take unexpected turns. Solution: Created a state management system that tracks collection progress and can gracefully redirect conversations.

---

## Future Work

The following features are planned for future releases:

User Management
1. User authentication and authorization
2. Role-based permissions for teams
3. Sharing chatbots between users or public

Model Selection
1. Support for multiple LLM providers
2. Ability to choose different models based on use case
3. Fine-tuning options for domain-specific applications

Advanced Features
1. Analytics dashboard for chatbot performance
2. Export of collected data to various formats
3. Integration with external data sources
4. API endpoints for embedding chatbots in other applications
