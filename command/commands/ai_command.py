import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyCiyzVA1I7lcM-NTFDcxaxQfUrIZwmD5NM"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=[])
MAX_HISTORY = 50

from iris import ChatContext

class AiCommand:
    invoke = "먀"
    help = ">ai명령어로 ai와 대화할 수 있습니다."
    type = "text"

    def handle(self, event:ChatContext):
        content = event.message.msg[len(">먀 "):].strip()
        response = chat.send_message(content)
        event.reply(response.text)


        if len(chat.history) > MAX_HISTORY:
            chat.history = chat.history[-MAX_HISTORY:]
            print(chat.history)


