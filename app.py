import streamlit as st
from template import myMainFrame as mf
from template import mySidebar as ms
#=======================================================================
def main():
    try:
        mf.MainBody()

        st.sidebar.header('Chatbot creator')
        st.sidebar.write('This chatbot allows you to create customs chatbots with specific behaviors.')
        st.sidebar.subheader('Instructions')
        st.sidebar.markdown('1. Click on "New Chat" to start a new conversation.')
        st.sidebar.markdown('2. Fill in the configuration details')
        st.sidebar.markdown('3. Click on chatbot to start')

        st.sidebar.subheader('Create New Chatbot')
        newChatButton = st.sidebar.button('New Chat')
        st.sidebar.subheader('Saved Chats')

        if ms.MySidebar(newChatButton):
            for chat_key in st.session_state.messages.keys():
                if st.sidebar.button(f"{st.session_state.messages[chat_key][0]['cbname']} "):
                    if st.session_state.form_submitted:
                        #print("inside line 216")
                        st.session_state.current_chat_key = chat_key
                        st.rerun()
                    else:
                        #print("inside line 219")
                        st.session_state.current_chat_key = chat_key
                        #print("Previous chat key: ", st.session_state.previous_chat_key)
                        st.session_state.messages.pop(st.session_state.previous_chat_key,None) #deleting the chat which is not submitted 

                    st.session_state.form_submitted= True
                    st.rerun()
                
    except Exception as e:
        #st.error(f"An error occurred in main(): {e}")
        print(f"An error occurred in main(): {e}")
        #print(st.session_state.messages)
        

    #print("End of main() function. Outside try-except block.")

if __name__ == '__main__':
    main()
