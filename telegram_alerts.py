import requests

BOT_TOKEN = "8344390516:AAHU6j06DzVEu1jzOsBvzxvxKb-nwwgPgKQ" 
CHAT_ID = "1587663363"

def send_telegram_message(message):
    """Sends a message to a specific Telegram chat."""
    # The URL for the Telegram Bot API's sendMessage method
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # The payload containing the chat_id and the message text
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown" 
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        print("Telegram alert sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram alert: {e}")