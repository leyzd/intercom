import telebot
import requests
import time

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
        # Menambahkan timeout agar script tidak menggantung jika koneksi lambat
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error API: {e}")
        return None

@bot.message_handler(commands=['price', 'evm'])
def send_evm_prices(message):
    bot.send_chat_action(message.chat.id, 'typing')
    data = get_evm_prices()
    
    if not data:
        bot.reply_to(message, "❌ Gagal mengambil data. Server API mungkin sedang sibuk, coba lagi nanti.")
        return

    text = "📊 **Harga Jaringan EVM Terkini**\n\n"
    for short_name, cg_id in EVM_CHAINS.items():
        # Cek apakah koin ada di dalam data untuk menghindari KeyError 'usd'
        coin_data = data.get(cg_id)
        if coin_data and 'usd' in coin_data:
            price = coin_data['usd']
            change = coin_data.get('usd_24h_change', 0)
            emoji = "📈" if change >= 0 else "📉"
            # Format angka dengan koma (ribuan)
            text += f"🔹 **{short_name.upper()}**: ${price:,.2f} ({emoji} {change:.2f}%)\n"
        else:
            text += f"🔹 **{short_name.upper()}**: Data tidak ditemukan\n"
    
    text += "\n💡 *Gunakan /chart untuk melihat grafik.*"
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['chart'])
def send_chart_info(message):
    chart_text = (
        "📈 **Link Grafik Blockchain**\n\n"
        "Klik link di bawah untuk melihat chart real-time:\n\n"
        "🔗 [BTC Chart](https://www.coingecko.com/en/coins/bitcoin)\n"
        "🔗 [ETH Chart](https://www.coingecko.com/en/coins/ethereum)\n"
        "🔗 [BSC Chart](https://www.coingecko.com/en/coins/binancecoin)\n"
        "🔗 [POLYGON Chart](https://www.coingecko.com/en/coins/matic-network)"
    )
    bot.reply_to(message, chart_text, parse_mode="Markdown", disable_web_page_preview=False)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Halo! Gunakan perintah berikut:\n/evm - Cek harga semua jaringan EVM\n/chart - Lihat grafik blockchain")

if __name__ == "__main__":
    print("Bot TRAC NETWORK Aktif...")
    # Infinity polling dengan penanganan error koneksi otomatis
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Koneksi terputus: {e}. Mencoba lagi dalam 5 detik...")
            time.sleep(5)

