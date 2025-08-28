import streamlit as st
from services import myServices as ms
#========================================
def MainBody():
    st.title('ChatBot Assistant')
    
    if 'messages' not in st.session_state:
        saved = ms.open_chat_history()
        if saved:
            st.session_state.messages = saved
            st.session_state.current_chat_key = f"Chat{len(st.session_state.messages) + 1}"
        else:
            st.session_state.messages = {'Chat1': []}

    if 'current_chat_key' not in st.session_state:
        st.session_state.current_chat_key = 'Chat1'

    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    
    if 'cancel_button' not in st.session_state:
        st.session_state.cancel_button = False
    
    if 'previous_chat_key' not in st.session_state:
        st.session_state.previous_chat_key = None
    
# This variable is used to makesure that all the saved_chats must be displayed everytime. Earlier it was a issue that whenever i 
# used to click on new_chat button that time all the saved chats used to get disapperred and then use to reload again.
    if 'saved_chats' not in st.session_state: 
        st.session_state.saved_chats = False

    #st.write("Current Chat Key:", st.session_state.current_chat_key) 
    #st.write("Current Bot Name: ", st.session_state.messages[st.session_state.current_chat_key][0]['cbname'])
    
    # Conditionally display the form or the chat interface
    if not st.session_state.form_submitted:
        # --- Form is now inside a separate function for clarity ---
        ms.RenderForm()

    elif st.session_state.form_submitted:
        #print("Inside elif of Main body \n ", st.session_state.messages)
        current_chat = st.session_state.messages[st.session_state.current_chat_key]

        delete_button = st.button("🗑️")

        if delete_button:
            ms.delete_chat(st.session_state.current_chat_key)
        else:
            if len(current_chat)==2:
                cbname = current_chat[0].get("cbname", "Assistant")
                welcome_text = f"👋 Hi canditate ! I'm {cbname}. What is your name :)"
                
                current_chat.append({"role": "assistant", "content": welcome_text})

            for mssg in current_chat:
                if "role" in mssg and "content" in mssg:
                    with st.chat_message(mssg["role"]):
                        st.markdown(mssg["content"])

            if st.session_state.messages[st.session_state.current_chat_key] != []:
                userInput = st.chat_input('Type your message here...')
                #print("User input:", userInput)
                if userInput:
                    ms.DisplayChats(userInput)
#================================================================