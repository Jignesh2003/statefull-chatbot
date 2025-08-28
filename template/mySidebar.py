import streamlit as st
from template import myMainFrame as mf

#========================================
def MySidebar(newChatButton):
    if newChatButton:
        if st.session_state.form_submitted:
            st.session_state.form_submitted = False

            new_chat_name = f"Chat{len(st.session_state.messages)+1}"
            st.session_state.current_chat_key = new_chat_name
            st.session_state.previous_chat_key = st.session_state.current_chat_key
            st.session_state.messages[new_chat_name]=[] 
            #print("-------------------------------\nInside my sidebar if part\n-------------------------------\n",st.session_state.messages)
            mf.MainBody()
            st.rerun()
       
        if st.session_state.form_submitted:   
            if st.session_state.messages[st.session_state.current_chat_key][0]['cbname']: 
                for chat_key in st.session_state.messages.keys():
                    # Display buttons for each chat
                    st.sidebar.button(st.session_state.messages[chat_key][0]['cbname'])

                    if st.sidebar.button(st.session_state.messages[chat_key][0]['cbname']):
                        st.session_state.current_chat_key = chat_key
                        st.rerun()  
        
    else:
        new_chat_name = st.session_state.current_chat_key
        if len(st.session_state.messages)<1:
            if st.session_state.form_submitted:
                if st.session_state.messages[st.session_state.current_chat_key][0]['cbname']:
                    #print("-------------------------------\nInside my sidebar else part\n-------------------------------\n",st.session_state.messages)
                    st.session_state.saved_chats = True
        else:
            st.session_state.saved_chats = True
    return st.session_state.saved_chats
#================================================================