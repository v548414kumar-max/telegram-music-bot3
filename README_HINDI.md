# Telegram Music Bot (Simple) — सेटअप गाइड (हिन्दी)

यह प्रोजेक्ट एक बेसिक Telegram म्यूज़िक बॉट देता है जो YouTube से ऑडियो डाउनलोड करके यूज़र को भेजता है।

## फ़ाइलें
- `music_bot.py` : मुख्य कोड
- `requirements.txt` : Python dependencies
- `.env` : (विकल्प) BOT_TOKEN यहाँ रखा गया है
- `README_HINDI.md` : यह फ़ाइल

## ज़रूरी कदम

1. Python इंस्टॉल करें (3.8+ सुझाया गया)।
2. वर्चुअल एनवायरनमेंट बनाना अच्छा रहता है:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows
   ```
3. डिपेंडेंसी इंस्टॉल करें:
   ```bash
   pip install -r requirements.txt
   ```
4. Bot Token सेट करें:
   - आप `.env` में `BOT_TOKEN` बदल सकते हैं (यह पहले से दिया गया है), या
   - सीधे environment variable में सेट करें:
     ```bash
     export BOT_TOKEN="your_token_here"     # Linux / macOS
     set BOT_TOKEN="your_token_here"        # Windows (cmd)
     $env:BOT_TOKEN="your_token_here"       # PowerShell
     ```
5. बोट चलाएँ:
   ```bash
   python music_bot.py
   ```
   अगर सब ठीक रहा तो कंसोल में `Bot is running...` दिखाई देगा।

## नोट्स और सावधानियाँ
- Telegram बोट का टोकन कृपया सार्वजनिक रूप से शेयर न करें। अगर यह टोकन कही लीक हो गया है, तो BotFather में जाकर `Revoke`/`Regenerate` कर लें।
- कॉपीराइटेड म्यूज़िक सार्वजनिक रूप से शेयर करना कानूनन समस्याग्रस्त हो सकता है — केवल व्यक्तिगत/टेस्टिंग प्रयोजनों के लिए प्रयोग करें।
- Telegram के फ़ाइल साइज लिमिट्स का ध्यान रखें (बोट-अपलोड्स पर सीमा हो सकती है)।
- प्रोडक्शन के लिए आप temp फ़ाइल नामों को और सुरक्षित बना लें और concurrency हैंडल करें।
