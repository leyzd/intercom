import telebot
from telebot import types
import requests
import random

# --- KONFIGURASI ---
TOKEN = "8312255798:AAFw5c-tpU1EmVmiTokpx6E_gXYwX0drm3g"
MORALIS_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjQyMzBlNjQ0LWQ2NGItNDQ1Mi04OGU5LTQwZjBiNGZhMzhlOCIsIm9yZ0lkIjoiNTAxNzU5IiwidXNlcklkIjoiNTE2Mjg0IiwidHlwZUlkIjoiYzZiYjA1NjUtMTQwYy00Y2U4LThlOGEtMzdjYzVmZDg0MTM5IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NzE3MTQ1NTYsImV4cCI6NDkyNzQ3NDU1Nn0.ac2li2f39lRgyzABDY_IogUEcaJYXr4El-L4q6pNpx8"

bot = telebot.TeleBot(TOKEN)

# --- DATABASE SEDERHANA (HANYA UNTUK HARGA) ---
EVM_CHAINS = {
    "eth": "ethereum", "bsc": "binancecoin", "polygon": "matic-network",
    "arbitrum": "arbitrum", "optimism": "optimism", "base": "base", "avax": "avalanche-2"
}

def get_evm_prices():
    ids = ",".join(EVM_CHAINS.values())
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else None
    except: return None

def get_wallet_balance(address, chain="eth"):
    url = f"https://deep-index.moralis.io/api/v2/{address}/balance?chain={chain}"
    headers = {"X-API-Key": MORALIS_API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return int(response.json()['balance']) / 10**18
        return None
    except: return None

@bot.message_handler(commands=['start', 'menu'])
def main_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Prices", callback_data="get_prices"),
        types.InlineKeyboardButton("🔍 Wallet", callback_data="wallet_menu"),
        types.InlineKeyboardButton("🎮 Lucky Spin", callback_data="play_game")
    )
    bot.send_message(message.chat.id, "🔥 **TRAC NETWORK DASHBOARD** 🔥\nSelect a feature:", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "get_prices":
        data = get_evm_prices()
        if not data: return
        text = "📊 **EVM PRICES**\n\n"
        for short, cg_id in EVM_CHAINS.items():
            coin = data.get(cg_id, {})
            price = coin.get('usd', 0)
            text += f"• **{short.upper()}**: `${price:,.2f}`\n"
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Back", callback_data="back_home"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "play_game":
        outcomes = ["🚀 MOON!", "📉 REKT!", "💎 DIAMOND HANDS!", "🐳 WHALE!"]
        result = random.choice(outcomes)
        text = f"🎰 **LUCKY SPIN** 🎰\n\nResult: **{result}**"
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🎰 Spin Again", callback_data="play_game"), types.InlineKeyboardButton("⬅️ Back", callback_data="back_home"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "back_home":
        main_menu(call.message)

@bot.message_handler(commands=['wallet'])
def wallet_check(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/wallet [address] [chain]`")
        return
    balance = get_wallet_balance(parts[1], parts[2].lower() if len(parts) > 2 else "eth")
    bot.reply_to(message, f"👛 Balance: **{balance:.4f}**" if balance is not None else "❌ API Error")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()

