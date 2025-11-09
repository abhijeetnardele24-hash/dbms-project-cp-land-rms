# 🤖 HOW TO CREATE TELEGRAM BOT - COMPLETE GUIDE

## 📱 Step-by-Step Instructions

### **Step 1: Open Telegram App**
- Open Telegram on your phone or computer
- Make sure you have an active Telegram account

---

## 🔧 **Step 2: Create Bot with BotFather**

### 2A. Find BotFather
1. Click on the **Search** icon in Telegram
2. Type: **@BotFather**
3. Click on the verified bot (has blue checkmark ✓)
4. Click **START**

### 2B. Create New Bot
1. Send this command: `/newbot`
2. BotFather will ask: **"Alright, a new bot. How are we going to call it?"**
3. Reply with your bot name (can be anything):
   ```
   Door Lock Bot
   ```
   Or any name you like:
   - My Door Lock
   - Smart Lock Bot
   - Home Security Bot

### 2C. Choose Username
1. BotFather will ask: **"Now, let's choose a username for your bot."**
2. Username must end with "bot" and be unique:
   ```
   abhijeet_doorlock_bot
   ```
   Examples:
   - `mydoorlock2025_bot`
   - `homelock_abhijeet_bot`
   - `smartdoor123_bot`

3. If username is taken, try another one

### 2D. Get Your Bot Token
1. After successful creation, BotFather will send you:
   ```
   Done! Congratulations on your new bot.
   You will find it at t.me/abhijeet_doorlock_bot
   
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-123456
   
   Keep your token secure and store it safely...
   ```

2. **COPY THE TOKEN** (the long string after "Use this token:")
   - It looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
   - **IMPORTANT:** Keep this secret! Don't share with anyone!

---

## 🆔 **Step 3: Get Your Chat ID**

### 3A. Find userinfobot
1. In Telegram search, type: **@userinfobot**
2. Click on the bot
3. Click **START**

### 3B. Get Your ID
1. The bot will immediately send you a message like:
   ```
   Id: 987654321
   First: Abhijeet
   Username: @your_username
   Language: en
   ```

2. **COPY THE ID NUMBER** (e.g., `987654321`)
   - This is your Chat ID
   - You'll need this to configure the code

---

## 📝 **Step 4: Update Your Arduino Code**

Open file: `telegram_otp_door_lock.ino`

### Find these lines (around line 40-41):
```cpp
#define BOT_TOKEN "XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
#define CHAT_ID "123456789"
```

### Replace with YOUR values:
```cpp
#define BOT_TOKEN "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  // ← Paste YOUR Bot Token here
#define CHAT_ID "987654321"                                 // ← Paste YOUR Chat ID here
```

**Example with real values:**
```cpp
#define BOT_TOKEN "6789012345:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
#define CHAT_ID "5432167890"
```

---

## ✅ **Step 5: Test Your Bot**

### 5A. Find Your Bot
1. In Telegram search, type your bot username
   - Example: `@abhijeet_doorlock_bot`
2. Click on your bot
3. Click **START**

### 5B. Send Test Message (BEFORE uploading code)
1. Send any message like "Hello"
2. Bot won't respond yet (code not uploaded)
3. This is normal! We'll upload code next.

### 5C. After Uploading Code to ESP32
Once you upload the Arduino code:
1. Open your bot in Telegram
2. Send: `/start`
3. Bot should respond with welcome message!
4. Send: `/unlock`
5. Bot will send you an OTP!

---

## 🎛️ **Bot Commands You Can Use**

After code is uploaded and running:

| Command | What It Does |
|---------|--------------|
| `/start` | Shows welcome message and available commands |
| `/unlock` | Generates and sends OTP to unlock door |
| `/status` | Shows system status (WiFi, door state, OTP active) |
| `/help` | Shows help and instructions |

---

## 🔐 **Security Tips**

✅ **DO:**
- Keep Bot Token secret
- Only share your Chat ID with trusted people
- Test bot before final installation
- Use strong WiFi password

❌ **DON'T:**
- Share Bot Token publicly (GitHub, forums, etc.)
- Use bot token in screenshots
- Give bot token to strangers
- Post Chat ID on social media

---

## 🎯 **Quick Reference Card**

**Copy this and fill in YOUR values:**

```
┌─────────────────────────────────────────┐
│  MY TELEGRAM BOT CREDENTIALS            │
├─────────────────────────────────────────┤
│  WiFi Name: hmm                         │
│  WiFi Pass: 12345678                    │
├─────────────────────────────────────────┤
│  Bot Name: ___________________          │
│  Bot Username: @____________bot         │
│  Bot Token: ____________________        │
│  My Chat ID: ___________________        │
└─────────────────────────────────────────┘
```

---

## 🛠️ **Troubleshooting**

### Problem: Can't find BotFather
**Solution:** Make sure you search for `@BotFather` (with @ symbol)

### Problem: Username already taken
**Solution:** Try adding numbers or your name:
- `abhijeet_lock_bot`
- `doorlock2025_bot`
- `smartlock_abhijeet_bot`

### Problem: Bot doesn't respond
**Solution:**
1. Make sure you uploaded code to ESP32
2. Check Serial Monitor - is WiFi connected?
3. Verify Bot Token is correct (no extra spaces)
4. Check Chat ID matches yours

### Problem: "Unauthorized access" message
**Solution:** Your Chat ID doesn't match. Double-check the CHAT_ID in code.

---

## 📸 **Visual Guide**

### What BotFather looks like:
```
BotFather
────────────────
I can help you create and manage Telegram bots.

Commands:
/newbot - create a new bot
/mybots - edit your bots

[START]
```

### When you send /newbot:
```
BotFather
────────────────
Alright, a new bot. How are we going to call it?

Please choose a name for your bot.
```
👆 You reply: "Door Lock Bot"

### After choosing username:
```
BotFather
────────────────
Done! Congratulations on your new bot.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

Keep your token secure and store it safely...
```
👆 COPY this token!

---

## 🎉 **You're Done!**

Once you have:
✅ Bot Token
✅ Chat ID
✅ WiFi credentials in code (already done!)

You're ready to upload the code to ESP32!

---

## 📞 **Need More Help?**

If something doesn't work:
1. Check Serial Monitor at 115200 baud
2. Look for error messages
3. Verify all credentials are correct
4. Make sure WiFi hotspot is ON
5. Test each component separately

**Good luck! 🚀🔐**
