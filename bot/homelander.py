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
conn = sqlite3.connect("leaderboard.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leaderboard (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    score INTEGER,
    submitted_at TEXT
)
""")

conn.commit()
conn.close()

@bot.on_message(command('start'))
async def start(client, message):
    await message.reply('Hi and Welcome')

@bot.on_message(command("leaderboard"))
async def leaderboard_handler(message):

    rows = get_leaderboard()
    if not rows:
        await message.reply("هنوز کسی امتیازی ثبت نکرده است.")
        return
    text = "🏆 Leaderboard\n\n"
    medals = ["🥇", "🥈", "🥉"]
    for i, (username, score) in enumerate(rows, start=1):
        if i <= 3:
            rank = medals[i - 1]
        else:
            rank = f"{i}."
        text += (
            f"{rank} {username} — {score}/100\n"
        )
    await message.reply(text)

@bot.on_message()
async def document_handler(message):

    user_id = message.author.id
    print(message.document)


    if not hasattr(message, "document"):
        return

    document = message.document
    if (
        document.mime_type != "application/json"
        and not document.name.endswith(".json")
    ):
        await message.reply(
            "❌ فقط فایل JSON قابل قبول است."
        )
        return
    else:
        content = await bot.download(document.id)
        student_data = json.loads(content.decode('utf-8'))
        report, score, max_score = judge(student_data)
        result = '\n'.join(report)
        final_score = f'\nFinal Score: {score}/{max_score}'
        await message.reply(result + final_score)

        # save result
        username = message.author.first_name
        user_id = message.author.id
        score = score
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = save_score(user_id, username, score, timestamp)
        await message.reply(row)




def save_score(user_id, username, score, timestamp):

    conn = sqlite3.connect("leaderboard.db")
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





def get_leaderboard(limit=30):

    conn = sqlite3.connect("leaderboard.db")
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






bot.run()