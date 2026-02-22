import telebot
from telebot import types
import random
import requests

# --- KONFIGURASI ---
TOKEN = "8312255798:AAFw5c-tpU1EmVmiTokpx6E_gXYwX0drm3g"
MY_WALLET = "0x51E20092dB3Ad826848777726584285741088414"
bot = telebot.TeleBot(TOKEN)

def get_header():
    return "╭━━━ ⋅◈⋅ ━━━╮\n  ✨ **TRAC NETWORK** ✨\n╰━━━ ⋅◈⋅ ━━━╯"

# --- MENU UTAMA ---
@bot.message_handler(commands=['start', 'menu'])
def main_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📤 Send Crypto", callback_data="transfer"),
        types.InlineKeyboardButton("🎮 Mini Games", callback_data="games_menu"),
        types.InlineKeyboardButton("💎 Wallet Rank", callback_data="rank"),
        types.InlineKeyboardButton("📅 Daily Tasks", callback_data="tasks"),
        types.InlineKeyboardButton("⛽ Gas Tracker", callback_data="gas"),
        types.InlineKeyboardButton("📊 Price Check", callback_data="price")
    )
    
    text = (
        f"{get_header()}\n\n"
        "🚀 **DASHBOARD HUB V1.0**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 User: `{message.from_user.first_name}`\n"
        "🏅 Rank: `Elite Member` ✨\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 *Pilih menu di bawah ini:*"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_all(call):
    # Navigasi Kembali
    if call.data == "back_home":
        main_menu(call.message)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return

    # Menu Games
    elif call.data == "games_menu":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🎲 Dice", callback_data="g_dice"),
            types.InlineKeyboardButton("💣 Mines", callback_data="g_mines"),
            types.InlineKeyboardButton("🔙 Menu Utama", callback_data="back_home")
        )
        bot.edit_message_text(f"{get_header()}\n\n🎮 **CASINO ARCADE**", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # Game Dice
    elif call.data == "g_dice":
        u, b = random.randint(1,6), random.randint(1,6)
        res = "🏆 WIN!" if u > b else ("💀 LOSE!" if u < b else "🤝 DRAW!")
        text = f"{get_header()}\n\n🎲 **DICE ROLL**\n👤 You: `{u}` | 🤖 Bot: `{b}`\n\nHasil: **{res}**"
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🔄 Main Lagi", callback_data="g_dice"),
            types.InlineKeyboardButton("🔙 Back", callback_data="games_menu")
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # Game Mines
    elif call.data == "g_mines":
        tiles = ["💎", "💎", "💎", "💣"]
        random.shuffle(tiles)
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton("❓", callback_data=f"m_res_{i}_{','.join(tiles)}") for i in range(4)]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="games_menu"))
        bot.edit_message_text(f"{get_header()}\n\n💣 **MINES GAME**\nHindari Bom!", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("m_res_"):
        d = call.data.split("_")
        idx = int(d[2])
        t = d[3].split(",")
        res_text = "💥 **BOOM! GAME OVER**" if t[idx] == "💣" else "💎 **WIN! SAFE!**"
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🔄 Main Lagi", callback_data="g_mines"),
            types.InlineKeyboardButton("🔙 Back", callback_data="games_menu")
        )
        bot.edit_message_text(f"{get_header()}\n\n{res_text}", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # Fitur Airdrop & Info
    elif call.data == "transfer":
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🔹 Send via Metamask", url=f"https://metamask.app.link/send/{MY_WALLET}"),
            types.InlineKeyboardButton("🔙 Back", callback_data="back_home")
        )
        bot.edit_message_text(f"{get_header()}\n\n📤 **TRANSFER GATEWAY**\n📍 Target: `{MY_WALLET}`", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "price":
        try:
            r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum,binancecoin&vs_currencies=usd").json()
            text = f"{get_header()}\n\n📊 **PRICE LIVE**\nETH: `${r['ethereum']['usd']}`\nBNB: `${r['binancecoin']['usd']}`"
        except: text = "Error fetching price."
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 Back", callback_data="back_home")))

if __name__ == "__main__":
    bot.infinity_polling()

