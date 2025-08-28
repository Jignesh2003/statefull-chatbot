import os
import json
import streamlit as st
import time
from models import Groq_LLM as gl
#===================================

def save_chat_history(chat_history):
    try:
        os.makedirs("chatHistory", exist_ok=True)

        with open('chatHistory/chat_history.json', 'w+',encoding="utf-8") as f:
            json.dump(chat_history,f, indent=2)
    except Exception as e:
            st.error(f"An error occurred in save_chat_history(): {e}")
            print(f"Error in save_chat_history(): {e}")

#======================================
def open_chat_history():
        if os.path.exists('chatHistory/chat_history.json'):
            try:
                with open('chatHistory/chat_history.json','r') as f:
                    entire_chat_app_mssgs = json.load(f)
                    return entire_chat_app_mssgs
            except Exception as e:
                #st.error(f'An error occurred in open_chat_history(): {e}')
                print(f"Error in open_chat_history(): {e}")
                return {}
                
        else:
            return False
        
#============================================
def StreamData(result):
    placeholder = st.empty()
    full_response = ""
    for char in result:
        full_response+=char
        placeholder.markdown(full_response+" ")
        time.sleep(0.002)
    placeholder.markdown(full_response)
    return full_response

#============================================
def DisplayChats(userInput):
    st.session_state.messages[st.session_state.current_chat_key].append({"role": "user", "content": userInput})
    
    response = gl.GatherInformation(gl.GeminiConnection(),st.session_state.messages[st.session_state.current_chat_key],userInput)
    if response is not None and isinstance(response, dict):
        #storing the value of user information into dictionary
        print('Inside line 203')
        for k in response.keys():
            #print("Inside line 187")
            dummy = k
        
        for k in st.session_state.messages[st.session_state.current_chat_key][1]:
            if k==dummy:
                #print("Inside line 192")
                st.session_state.messages[st.session_state.current_chat_key][1][dummy]= response[dummy]

    for mssg in st.session_state.messages[st.session_state.current_chat_key][-1:]:    # Display only the latest message of user
        with st.chat_message(mssg["role"]):
            st.markdown(mssg["content"])

    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            if response is not None and isinstance(response, dict):
                info_dict = st.session_state.messages[st.session_state.current_chat_key][1]
                # exclude control keys
                fields_to_check = {k: v for k, v in info_dict.items() if k not in ["information_gathered"]}
                
                if not info_dict["information_gathered"]:
                    # if any field is still empty → ask for it
                    missing_field = next((k for k, v in fields_to_check.items() if v in ["", [], None]), None)
                    
                    if missing_field:
                        pretty_field = missing_field.replace("_", " ")
                        result = f"Please provide your {pretty_field}"
                    else:
                        # all filled → mark as gathered
                        info_dict["information_gathered"] = True
                        result = (
                            "This is all the information so far you have provided  \n"
                            f"Name: {info_dict['name']}  \n"
                            f"Age: {info_dict['age']}  \n"
                            f"Email: {info_dict['email']}  \n"
                            f"Phone Number: {info_dict['phone_number']}  \n"
                            f"Current Location: {info_dict['current_location']}  \n"
                            f"Year of Experience: {info_dict['year_of_experience']}  \n"
                            f"Desired Position: {info_dict['desired_position']}  \n"
                            f"Technological Stack: {info_dict['technical_stack']}  \n"
                            "✅ Let's start the interview!"
                        )
                        
                        # 🔥 Immediately fetch first interview question
                        first_question = gl.BotResponse(
                            gl.GeminiConnection(),
                            st.session_state.messages[st.session_state.current_chat_key],
                            "Let's begin the interview"
                        )
                        result += f"\n\n{first_question}"
                else:
                    # all gathered → continue to interview
                    result = gl.BotResponse(gl.GeminiConnection(), st.session_state.messages[st.session_state.current_chat_key], userInput)
            else:
                # once gathered, continue to interview
                result = gl.BotResponse(gl.GeminiConnection(), st.session_state.messages[st.session_state.current_chat_key], userInput)

            result = StreamData(result)       
            st.session_state.messages[st.session_state.current_chat_key].append({"role": "assistant", "content": result})
            save_chat_history(st.session_state.messages)

#============================================
def RenderForm():
    
    with st.form("chatbot_config_form", clear_on_submit=True):
        chatbot_name = st.text_input("Chatbot Name",placeholder="Give your chatbot a name",key='chatbot_name',help="Enter a unique name for your chatbot.")
        
        st.header("Additional Information")
        additional_info = st.text_area("Additional Information",placeholder="Enter the behavior of Model", help="Based on the user tech stack, ask them 3-5 questions regarding it to judge their proficiency.")
        
        col1, col2 = st.columns([0.6,0.4])
        with col1:
            submitted = st.form_submit_button("Submit", use_container_width=True)
        with col2:
            cancelled = st.form_submit_button("Cancel")
    
    if cancelled:
        st.session_state.form_submitted = False
        st.session_state.cancel_button = True

    if submitted:
        if chatbot_name=="" and additional_info=="":
            #print("inside if of submit")
            st.session_state.form_submitted = False
            st.warning("Please fill in all fields.")
            
        elif chatbot_name==None and additional_info==None:
            #print("inside elif of submit")
            st.session_state.form_submitted = False
            st.warning("Please fill in all fields.")
            
        else:
            print("inside else of submit")
            st.session_state.form_submitted = True
            st.session_state.cancel_button = False

            st.session_state.messages[st.session_state.current_chat_key].append({
                    "cbname": chatbot_name,
                    "additional_information": additional_info
                    })
            st.session_state.messages[st.session_state.current_chat_key].append(
                {'information_gathered':False,
                 "name":"",
                 "age":"",
                 "email":"",
                 "phone_number":"",
                 "current_location":"",
                 "year_of_experience":"",
                 "desired_position":"",
                 "technical_stack":[]
                })
            st.rerun()

#==================================================
def delete_chat(mychatkey):
    del st.session_state.messages[mychatkey]
    temp_dict = {}
    for index, (k,v) in enumerate(st.session_state.messages.items(),start=1):
        temp_dict[f'chat{index}'] = v
    st.session_state.messages = temp_dict

    st.session_state.current_chat_key = f"chat{len(st.session_state.messages) + 1}"
    st.session_state.form_submitted = False
    st.session_state.saved_chats = False

    save_chat_history(st.session_state.messages)
    RenderForm()  # Re-render the form after deletion
    st.rerun()

#==================================================