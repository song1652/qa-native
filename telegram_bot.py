import asyncio
import subprocess
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8780431124:AAFnKp6S-s7cIijCy9F1Rw1koalZHlc1o5E"
CLAUDE_CMD = r"C:\Users\User\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\npm\claude.cmd"
PYTHON  = r"C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe"
CWD     = r"C:\TEST MANAGER\qa-native"
ANSI    = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
USERS   = set()


def _claude(prompt: str) -> str:
    import os, uuid
    inp = os.path.join(CWD, f"_in_{uuid.uuid4().hex[:8]}.txt")
    try:
        with open(inp, "w", encoding="utf-8") as f:
            f.write(prompt)
        env = os.environ.copy()
        env["_QA_P"] = prompt
        r = subprocess.run(
            [CLAUDE_CMD, "--dangerously-skip-permissions", "-p", prompt],
            capture_output=True,
            cwd=CWD,
            timeout=120,
            env=env,
        )
        if r.stdout:
            output = r.stdout.decode("utf-8", errors="replace")
            output = ANSI.sub("", output).strip()
            if output:
                return output[:4000]
        if r.stderr:
            err = r.stderr.decode("cp949", errors="replace").strip()
            return f"[오류] {err[:300]}"
        return "(응답 없음)"
    except subprocess.TimeoutExpired:
        return "시간 초과"
    except Exception as e:
        return f"오류: {e}"
    finally:
        if os.path.exists(inp):
            try: os.remove(inp)
            except: pass


def _script(name: str) -> str:
    r = subprocess.run(
        [PYTHON, name], capture_output=True, cwd=CWD, timeout=120
    )
    raw = (r.stdout or r.stderr).decode("utf-8", errors="replace")
    return raw.strip()[:4000] or "(출력 없음)"


def _allow(uid): return not USERS or uid in USERS


async def on_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USERS.add(update.effective_user.id)
    kb = [
        [InlineKeyboardButton("📊 현황", callback_data="status")],
        [InlineKeyboardButton("▶️ QA 실행", callback_data="run_qa")],
        [InlineKeyboardButton("✅ 승인", callback_data="approve"),
         InlineKeyboardButton("❌ 반려", callback_data="reject")],
        [InlineKeyboardButton("🔧 힐링", callback_data="heal")],
    ]
    await update.message.reply_text("QA 봇 시작!", reply_markup=InlineKeyboardMarkup(kb))


async def on_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USERS.add(update.effective_user.id)
    await update.message.reply_text("테스트1: 한글 하드코딩 정상!")
    res = await asyncio.to_thread(_claude, "say hi in one word")
    await update.message.reply_text(f"테스트2: {res}")


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    try: await q.answer()
    except: pass
    if not _allow(q.from_user.id):
        await q.edit_message_text("권한 없음"); return

    d = q.data
    if d == "status":
        await q.edit_message_text("확인 중...")
        r = await asyncio.to_thread(_claude, "state.json 파일을 읽고 현재 step, url, 실행 결과를 한국어로 요약해줘")
        await q.edit_message_text(f"📊 현황\n\n{r}")
    elif d == "run_qa":
        await q.edit_message_text("URL과 테스트케이스 경로를 입력하세요.\n예: https://example.com testcases/login/cases.md")
        context.user_data["w"] = "run_qa"
    elif d == "approve":
        await q.edit_message_text("승인 처리 중...")
        r = await asyncio.to_thread(_claude, "state.json의 approval_status를 approved로 변경 저장 후 scripts/05_execute.py 실행해줘")
        await q.edit_message_text(f"✅ 승인\n\n{r}")
    elif d == "reject":
        await q.edit_message_text("반려 사유를 입력하세요:")
        context.user_data["w"] = "reject"
    elif d == "heal":
        await q.edit_message_text("힐링 중...")
        r = await asyncio.to_thread(_script, "scripts/06_heal.py")
        await q.edit_message_text(f"🔧 힐링\n\n{r}")


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allow(update.effective_user.id):
        await update.message.reply_text("권한 없음"); return
    text = update.message.text
    w = context.user_data.get("w")
    if w == "run_qa":
        context.user_data.pop("w")
        await update.message.reply_text("실행 중...")
        r = await asyncio.to_thread(_claude, f"run_qa.py를 실행해줘. URL과 케이스: {text}")
        await update.message.reply_text(r)
    elif w == "reject":
        context.user_data.pop("w")
        await asyncio.to_thread(_claude, f"state.json의 approval_status를 rejected로, rejection_reason을 다음으로 저장: {text}")
        await update.message.reply_text(f"❌ 반려: {text}")
    else:
        await update.message.reply_text("처리 중...")
        r = await asyncio.to_thread(_claude, text)
        await update.message.reply_text(r)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", on_start))
    app.add_handler(CommandHandler("test", on_test))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    print("봇 시작됨.")
    app.run_polling(drop_pending_updates=True, allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
