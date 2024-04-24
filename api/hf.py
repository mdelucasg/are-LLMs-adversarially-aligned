from hugchat import hugchat
from hugchat.login import Login

def huggingface_chatbot(email=None, password=None):
    if email is None or password is None:
        return None
    
    # Log in to huggingface and grant authorization to huggingchat
    cookie_path_dir = "./cookies/"
    sign = Login(email, password)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

    # Create your ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot