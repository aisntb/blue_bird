import io
import random
import traceback

from iris import ChatContext

admin = [7831346840253704798, 6628050693993113317]
class EvalCommand:
    invoke = "blue"
    help = "관리자용 명령어입니다."
    type = "kl"

    def handle(self, event: ChatContext, kl: str):
        # 관리자 체크
        if event.sender.id not in admin:
            return

        # 전체 메시지에서 "!blue " 뒤의 코드만 꺼내기
        raw = event.message.msg  # 예: "!blue\na = 1\nprint(a)"
        # invoke와 공백(또는 개행) 뒤에 오는 부분을 code로 추출
        # ex. raw = "!blue   \na = 1\nprint(a)"
        parts = raw.split(None, 1)
        if len(parts) < 2:
            event.reply("실행할 코드를 입력해 주세요.")
            return
        code = parts[1].strip()

        # stdout 캡처용 버퍼
        buf = io.StringIO()
        # 최소 권한 exec 환경
        exec_globals = {
            "__builtins__": __builtins__,
            "event": event,
            "kl": kl,  # 원래 받던 kl 변수도 그대로 노출
        }
        # print() 은 buf에 기록
        exec_globals["print"] = lambda *args, **kwargs: __builtins__ \
            .print(*args, file=buf, **kwargs)

        try:
            exec(code, exec_globals, {})
            output = buf.getvalue().strip() or "✅ 실행 완료 — 출력 결과가 없습니다."
        except Exception:
            output = "❌ 실행 중 오류 발생:\n" + traceback.format_exc()
        finally:
            buf.close()

        event.reply(output)




