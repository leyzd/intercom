import telebot
import requests

# Masukkan Token Anda
TOKEN = "8312255798:AAFw5c-tpU1EmVmiTokpx6E_gXYwX0drm3g"
bot = telebot.TeleBot(TOKEN)

# Daftar ID koin di CoinGecko untuk jaringan EVM
EVM_CHAINS = {
    "eth": "ethereum",
    "bsc": "binancecoin",
    "polygon": "matic-network",
    "arbitrum": "arbitrum",
    "optimism": "optimism",
    "base": "base",
    "avax": "avalanche-2"
}

def get_evm_prices():
    ids = ",".join(EVM_CHAINS.values())
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        return requests.get(url).json()
    except:
        return None

@bot.message_handler(commands=['price', 'evm'])
def send_evm_prices(message):
    data = get_evm_prices()
    if not data:
        bot.reply_to(message, "❌ Gagal mengambil data dari jaringan EVM.")
        return

    text = "📊 **Harga Jaringan EVM Terkini**\n\n"
    for short_name, cg_id in EVM_CHAINS.items():
        price = data[cg_id]['usd']
        change = data[cg_id]['usd_24h_change']
        emoji = "📈" if change > 0 else "📉"
        text += f"🔹 **{short_name.upper()}**: ${price:,} ({emoji} {change:.2f}%)\n"
    
    text += "\n💡 *Gunakan /chart untuk melihat grafik.*"
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['chart'])
def send_chart_info(message):
    # Solusi paling aman agar tidak gagal muat gambar: Berikan Link Preview
    chart_text = (
        "📈 **Link Grafik Blockchain**\n\n"
        "Klik link di bawah untuk melihat chart real-time:\n"
        "🔗 [BTC Chart](https://www.coingecko.com/en/coins/bitcoin)\n"
        "🔗 [ETH Chart](https://www.coingecko.com/en/coins/ethereum)\n"
        "🔗 [BSC Chart](https://www.coingecko.com/en/coins/binancecoin)"
    )
    bot.reply_to(message, chart_text, parse_mode="Markdown", disable_web_page_preview=False)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Halo! Gunakan perintah berikut:\n/evm - Cek harga semua jaringan EVM\n/chart - Lihat grafik blockchain")

if __name__ == "__main__":
    print("Bot EVM & Blockchain Aktif...")
    bot.infinity_polling()

