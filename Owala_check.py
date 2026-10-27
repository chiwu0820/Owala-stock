import os
import requests
from bs4 import BeautifulSoup

# Owala 泡泡藍 740ml 網址
PRODUCT_URL = "https://www.eslite.com/product/10052271402683151705000"

# 從 GitHub Secrets 讀取 Webhook 網址（維護安全性）
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.eslite.com/"
}

def send_discord_notify(message):
    if not DISCORD_WEBHOOK_URL:
        print("❌ 未設定 DISCORD_WEBHOOK_URL 環境變數")
        return

    payload = {
        "content": f"🚨 **【誠品線上 Owala 補貨通知】** 🚨\n{message}\n🔗 **快速搶購連結**：{PRODUCT_URL}"
    }
    try:
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if res.status_code == 204:
            print("🟢 [通知成功] 已發送推播到 Discord！")
        else:
            print(f"🔴 [通知失敗] Status Code: {res.status_code}")
    except Exception as e:
        print(f"❌ [發送異常] {e}")

def check_stock():
    print("正在檢查 Owala 泡泡藍庫存...")
    try:
        response = requests.get(PRODUCT_URL, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            print(f"⚠️ 存取網頁異常，HTTP 狀態碼: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        
        out_of_stock_keywords = ["暫無庫存", "售完補貨中", "已售完", "補貨中"]
        is_out_of_stock = any(keyword in text_content for keyword in out_of_stock_keywords)
        has_buy_button = ("加入購物車" in text_content or "立即購買" in text_content)

        if not is_out_of_stock and has_buy_button:
            print("🎉 偵測到商品有庫存！可以購買！")
            send_discord_notify("💙 Owala FreeSip Tritan 740ml 泡泡藍 有貨囉！手刀快搶！")
        else:
            print("🔒 目前仍顯示無庫存 / 補貨中。")

    except Exception as e:
        print(f"❌ 擷取失敗: {e}")

if __name__ == "__main__":
    check_stock()
