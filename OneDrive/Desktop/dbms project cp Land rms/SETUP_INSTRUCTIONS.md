# 🚀 TELEGRAM OTP DOOR LOCK - SETUP INSTRUCTIONS

## 📋 Prerequisites

Before uploading the code, you need to:

### 1. Install Arduino IDE
- Download from: https://www.arduino.cc/en/software
- Install ESP32 board support

### 2. Install Required Libraries

Open Arduino IDE → Tools → Manage Libraries, then install:

| Library Name | Author | Purpose |
|--------------|--------|---------|
| **ESP32** | Espressif | ESP32 board support |
| **UniversalTelegramBot** | Brian Lough | Telegram API |
| **ArduinoJson** | Benoit Blanchon | JSON parsing (v6.x) |
| **LiquidCrystal I2C** | Frank de Brabander | LCD control |
| **Keypad** | Mark Stanley | Keypad matrix |

#### Installing ESP32 Board Support:
1. Go to **File → Preferences**
2. Add this URL to "Additional Board Manager URLs":
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Go to **Tools → Board → Boards Manager**
4. Search "ESP32" and install

---

## 🤖 Step 1: Create Telegram Bot

### A. Get Bot Token from BotFather

1. Open Telegram app
2. Search for **@BotFather**
3. Send command: `/newbot`
4. Follow instructions:
   - Choose a name (e.g., "My Door Lock")
   - Choose a username (e.g., "mydoorlock_bot")
5. **Copy the Bot Token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### B. Get Your Chat ID

1. Search for **@userinfobot** on Telegram
2. Send: `/start`
3. **Copy your Chat ID** (looks like: `123456789`)

---

## ⚙️ Step 2: Configure the Code

Open `telegram_otp_door_lock.ino` in Arduino IDE and edit these lines:

### WiFi Settings (Lines 33-34):
```cpp
const char* WIFI_SSID = "YOUR_WIFI_SSID";           // ← Put your WiFi name here
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";   // ← Put your WiFi password here
```

**Example:**
```cpp
const char* WIFI_SSID = "Home_WiFi_5G";
const char* WIFI_PASSWORD = "MySecurePass123";
```

### Telegram Settings (Lines 40-41):
```cpp
#define BOT_TOKEN "XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  // ← Paste Bot Token here
#define CHAT_ID "123456789"                                         // ← Paste Chat ID here
```

**Example:**
```cpp
#define BOT_TOKEN "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
#define CHAT_ID "987654321"
```

### LCD I2C Address (Line 45):
```cpp
#define LCD_ADDRESS 0x27    // Default is 0x27, might be 0x3F
```

**Note:** If LCD doesn't work, try changing to `0x3F`

---

## 🔌 Step 3: Upload Code to ESP32

1. **Connect ESP32 to Computer**
   - Use Micro USB cable
   - Connect to your computer

2. **Select Board in Arduino IDE**
   - Go to **Tools → Board → ESP32 Arduino**
   - Select: **ESP32 Dev Module**

3. **Select COM Port**
   - Go to **Tools → Port**
   - Select the COM port (e.g., COM3, COM4)
   - If no port appears, install CP210x USB driver

4. **Upload Code**
   - Click **Upload** button (→)
   - Wait for "Done uploading" message

5. **Open Serial Monitor**
   - Go to **Tools → Serial Monitor**
   - Set baud rate to: **115200**
   - You should see boot messages

---

## 🔍 Step 4: Test the System

### A. Check Serial Monitor Output

You should see:
```
============================================
  TELEGRAM OTP DOOR LOCK SYSTEM - ESP32
============================================
✅ LCD Initialized
Connecting to WiFi: Your_WiFi
✅ WiFi Connected!
IP Address: 192.168.1.100
Testing Telegram bot...
Telegram bot connected successfully!
✅ System Ready!
Send /unlock command to Telegram bot
============================================
```

### B. Test Telegram Bot

1. Open Telegram
2. Find your bot (search for username you created)
3. Send: `/start`
4. Bot should respond with welcome message

### C. Test OTP Generation

1. Send: `/unlock`
2. Bot sends OTP (e.g., "Your OTP: 1234")
3. LCD should show: "OTP Sent! 60s"
4. Enter OTP on keypad: `1234` + `#`
5. Door should unlock!

---

## 🛠️ Troubleshooting

### Problem: WiFi won't connect
**Solutions:**
- Check WiFi name and password (case-sensitive!)
- Ensure ESP32 is close to router
- Try 2.4GHz WiFi (ESP32 doesn't support 5GHz)

### Problem: Telegram bot doesn't respond
**Solutions:**
- Verify Bot Token is correct (no spaces!)
- Check Chat ID matches your user
- Ensure WiFi is connected
- Test internet connection

### Problem: LCD shows nothing
**Solutions:**
- Check I2C address (try 0x3F if 0x27 doesn't work)
- Verify wiring: SDA→GPIO21, SCL→GPIO22
- Adjust LCD contrast potentiometer on back

### Problem: Keypad not working
**Solutions:**
- Check all 8 wires are connected correctly
- Test keypad with Serial Monitor (should print key presses)
- Verify pin numbers match your wiring

### Problem: Relay/Solenoid not activating
**Solutions:**
- Check relay module has power (LED should light)
- Verify signal wire: ESP32 GPIO23 → Relay IN
- Ensure 12V power is connected to solenoid
- Test relay manually by connecting IN to 5V

---

## 📱 Available Commands

Once system is running, you can use these Telegram commands:

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and command list |
| `/unlock` | Request OTP to unlock door |
| `/status` | Check system status (WiFi, door state, OTP) |
| `/help` | Show help and instructions |

---

## 🔐 Security Features

✅ **OTP expires after 60 seconds**
✅ **Maximum 3 wrong attempts** (1 minute lockout)
✅ **Only authorized Chat ID** can control lock
✅ **Notifications** sent for wrong attempts
✅ **Auto-lock** after 5 seconds

---

## ⚙️ Configuration Options

You can customize these values in the code:

| Variable | Line | Default | Description |
|----------|------|---------|-------------|
| `OTP_LENGTH` | 95 | 4 | Number of OTP digits (4-6 recommended) |
| `OTP_VALIDITY` | 96 | 60000 | OTP validity in milliseconds (60 seconds) |
| `MAX_WRONG_ATTEMPTS` | 97 | 3 | Maximum wrong attempts before lockout |
| `UNLOCK_DURATION` | 100 | 5000 | How long door stays unlocked (5 seconds) |
| `BOT_CHECK_INTERVAL` | 92 | 1000 | How often to check for messages (1 second) |

---

## 📊 Keypad Usage

| Key | Function |
|-----|----------|
| `0-9` | Enter OTP digits |
| `#` | Submit OTP |
| `*` | Delete last digit |
| `A-D` | Reserved for future features |

**Note:** OTP auto-submits when all 4 digits are entered!

---

## 🎯 Project Demo Tips

For demonstration:

1. **Show idle state:** LCD displays "Telegram Lock / Send /unlock"
2. **Open Telegram:** Show bot conversation
3. **Send `/unlock`:** Show OTP received
4. **Enter OTP:** Enter digits on keypad (LCD updates)
5. **Success:** Solenoid unlocks, LCD shows "Access Granted!"
6. **Auto-lock:** After 5 seconds, door locks
7. **Wrong OTP:** Show invalid attempt notification
8. **Status check:** Send `/status` to show system info

---

## 📞 Support

If you need help:

1. Check Serial Monitor for error messages
2. Verify all wiring matches the diagram
3. Test each component individually
4. Check library versions are up to date

---

## 🎉 You're All Set!

Your Telegram OTP Door Lock is now ready to use!

**Next Steps:**
1. Mount components on cardboard as per layout diagram
2. Test thoroughly before final installation
3. Consider adding backup power (power bank)
4. Add more authorized users by modifying CHAT_ID check

**Enjoy your smart door lock! 🚪🔐**
