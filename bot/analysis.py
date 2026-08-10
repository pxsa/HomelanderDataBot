from balethon import Client
from balethon.conditions import command
from balethon.objects import ReplyKeyboard, ReplyKeyboardButton
from balethon.objects import InlineKeyboard, InlineKeyboardButton
import io
import json
from judge import judge
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Client(TOKEN)

DB_PATH = "leaderboard.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Best-score table (used for the leaderboard, unchanged behavior)
cursor.execute("""
CREATE TABLE IF NOT EXISTS leaderboard (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    score INTEGER,
    submitted_at TEXT
)
""")

# NEW: one row per submission -> full history for analysis in Metabase
# (score, timing, file/report metadata, and later the stress rating)
cursor.execute("""
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    score INTEGER,
    max_score INTEGER,
    submitted_at TEXT,
    stress_level INTEGER,
    attempt_number INTEGER,
    file_size_bytes INTEGER,
    error_count INTEGER,
    is_perfect INTEGER
)
""")

conn.commit()
conn.close()

# NEW NEW NEW
last_bot_messages = {}

# Tracks which submission (by id in the submissions table) is waiting for a
# stress rating from a given user, so the callback knows which row to update.
pending_stress = {}

main_menu = InlineKeyboard(
    [InlineKeyboardButton("🏆 لیدربورد", callback_data="leaderboard")],
    [InlineKeyboardButton("ℹ️ راهنما", callback_data="help")],
)

stress_menu = InlineKeyboard(
    [
        InlineKeyboardButton("1", callback_data="stress_1"),
        InlineKeyboardButton("2", callback_data="stress_2"),
        InlineKeyboardButton("3", callback_data="stress_3"),
        InlineKeyboardButton("4", callback_data="stress_4"),
        InlineKeyboardButton("5", callback_data="stress_5"),
    ],
)


@bot.on_message(command("start"))
async def start(client, message):
    await clean_send(
        message.chat.id,
        "سلام 👋\nبه بات داوری تمرین آخر یادگیری عمیق خوش آمدی.\nاز منوی زیر انتخاب کن:",
        main_menu
    )


@bot.on_message(command("leaderboard"))
async def leaderboard_handler(message):
    rows = get_leaderboard()

    if not rows:
        await clean_send(message, "هنوز کسی امتیازی ثبت نکرده است.", main_menu)
        return

    text = "🏆 Leaderboard\n\n"
    medals = ["🥇", "🥈", "🥉"]

    for i, (username, score) in enumerate(rows, start=1):
        rank = medals[i - 1] if i <= 3 else f"{i}."
        text += f"{rank} {username} — {score}/100\n"

    await clean_send(message, text, main_menu)


@bot.on_message()
async def document_handler(client, message):
    document = getattr(message, "document", None)

    if document is None:
        return

    user_id = message.author.id
    username = message.author.first_name

    if (
        document.mime_type != "application/json"
        and not document.name.endswith(".json")
    ):
        await clean_send(
            message.chat.id,
            "❌ فقط فایل JSON قابل قبول است.",
            main_menu
        )
        return

    try:
        content = await bot.download(document.id)
        student_data = json.loads(content.decode("utf-8"))

        report, score, max_score = judge(student_data)

        result = "\n".join(report)
        final_score = f"\n\nFinal Score: {score}/{max_score}"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Keep the "best score" leaderboard exactly as before
        save_score(user_id, username, score, timestamp)

        # NEW: extra metadata for later analysis in Metabase
        attempt_number = get_attempt_number(user_id) + 1
        file_size_bytes = len(content)
        error_count = sum(1 for line in report if line.strip().startswith("❌"))
        is_perfect = 1 if score >= max_score else 0

        # NEW: log this specific attempt (every submission, not just the best)
        submission_id = save_submission(
            user_id, username, score, max_score, timestamp,
            attempt_number, file_size_bytes,
            error_count, is_perfect
        )

        # NEW: remember which row is waiting for a stress rating
        pending_stress[user_id] = submission_id

        await clean_send(
            message.chat.id,
            result + final_score + "\n\n✅ نتیجه ثبت شد.\n\n"
            "😅 میزان استرست هنگام انجام این تمرین از ۱ (خیلی کم) تا ۵ (خیلی زیاد) چقدر بود؟",
            stress_menu
        )

    except json.JSONDecodeError:
        await clean_send(
            message.chat.id,
            "❌ فایل JSON معتبر نیست.",
            main_menu
        )

    except Exception as e:
        print("Judge error:", e)
        await clean_send(
            message.chat.id,
            "❌ خطایی هنگام بررسی فایل رخ داد.",
            main_menu
        )


def save_score(user_id, username, score, timestamp):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT score FROM leaderboard WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    if row is None:
        cursor.execute(
            """
            INSERT INTO leaderboard
            (user_id, username, score, submitted_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, username, score, timestamp)
        )

    elif score > row[0]:
        cursor.execute(
            """
            UPDATE leaderboard
            SET username=?,
                score=?,
                submitted_at=?
            WHERE user_id=?
            """,
            (username, score, timestamp, user_id)
        )

    conn.commit()
    conn.close()
    return row


def get_attempt_number(user_id):
    """Returns how many times this user has submitted so far."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM submissions WHERE user_id=?",
        (user_id,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def save_submission(
    user_id, username, score, max_score, timestamp,
    attempt_number, file_size_bytes,
    error_count, is_perfect
):
    """Logs every single judged attempt (for Metabase analysis)."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO submissions
        (user_id, username, score, max_score, submitted_at, stress_level,
         attempt_number, file_size_bytes, error_count, is_perfect)
        VALUES (?, ?, ?, ?, ?, NULL, ?, ?, ?, ?)
        """,
        (
            user_id, username, score, max_score, timestamp,
            attempt_number, file_size_bytes,
            error_count, is_perfect
        )
    )

    submission_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return submission_id


def save_stress_level(submission_id, stress_level):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE submissions SET stress_level=? WHERE id=?",
        (stress_level, submission_id)
    )

    conn.commit()
    conn.close()


def get_leaderboard(limit=30):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, score
        FROM leaderboard
        ORDER BY score DESC,
                 submitted_at ASC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


async def clean_send(chat_id, text, keyboard=None):
    old_message_id = last_bot_messages.get(chat_id)

    if old_message_id:
        try:
            await bot.delete_message(chat_id, old_message_id)
        except Exception as e:
            print("Delete error:", e)

    sent = await bot.send_message(
        chat_id,
        text,
        reply_markup=keyboard
    )

    sent_id = getattr(sent, "id", None) or getattr(sent, "message_id", None)

    if sent_id:
        last_bot_messages[chat_id] = sent_id

    return sent


@bot.on_callback_query()
async def menu_handler(callback_query):
    data = callback_query.data
    message = callback_query.message
    chat_id = message.chat.id
    user_id = callback_query.author.id

    await callback_query.answer("✅")

    if data == "leaderboard":
        rows = get_leaderboard()

        if not rows:
            text = "هنوز کسی امتیازی ثبت نکرده است."
        else:
            text = "🏆 Leaderboard\n\n"
            medals = ["🥇", "🥈", "🥉"]

            for i, (username, score) in enumerate(rows, start=1):
                rank = medals[i - 1] if i <= 3 else f"{i}."
                text += f"{rank} {username} — {score}/100\n"

        await clean_send(chat_id, text, main_menu)

    elif data == "submit_json":
        await clean_send(
            chat_id,
            "📤 لطفاً فایل JSON خودت را همینجا ارسال کن.\n\n"
            "فقط فایل با پسوند `.json` قابل قبول است.",
            main_menu
        )

    elif data == "help":
        await clean_send(
            chat_id,
            "ℹ️ راهنما:\n\n"
            "1. فایل JSON را ارسال کن.\n"
            "2. بات آن را داوری می‌کند.\n"
            "3. اگر امتیازت بهتر از قبل باشد، در لیدربورد ذخیره می‌شود.\n\n"
            "برای دیدن رتبه‌ها از دکمه لیدربورد استفاده کن.",
            main_menu
        )

    # NEW: handle stress rating buttons (stress_1 .. stress_5)
    elif data.startswith("stress_"):
        stress_level = int(data.split("_")[1])
        submission_id = pending_stress.pop(user_id, None)

        if submission_id is not None:
            save_stress_level(submission_id, stress_level)
            await clean_send(
                chat_id,
                "🙏 ممنون بابت پاسخت! ثبت شد.",
                main_menu
            )
        else:
            # No pending submission found (e.g. old button pressed twice)
            await clean_send(
                chat_id,
                "این درخواست دیگر معتبر نیست.",
                main_menu
            )


bot.run()