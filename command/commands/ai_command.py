from google import genai
client = genai.Client(api_key="AIzaSyCiyzVA1I7lcM-NTFDcxaxQfUrIZwmD5NM")
from iris import ChatContext

class AiCommand:
    invoke = "먀"
    help = ">ai명령어로 ai와 대화할 수 있습니다."
    type = "text"

    def handle(self, event:ChatContext):
        content = event.message.msg[len(">먀 "):].strip()
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=content
        )
        event.reply(response.text)


