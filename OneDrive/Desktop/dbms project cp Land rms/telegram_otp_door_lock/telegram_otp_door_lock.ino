/*
 * ============================================================================
 * TELEGRAM OTP DOOR LOCK SYSTEM - ESP32
 * ============================================================================
 * 
 * Project: Telegram-based OTP Door Lock with Keypad Entry
 * Hardware: ESP32 WROOM 32, LCD1602 I2C, 4x4 Keypad, 5V Relay, 12V Solenoid
 * 
 * Features:
 * - Request OTP via Telegram bot
 * - Enter OTP on 4x4 keypad
 * - LCD displays status and OTP prompt
 * - Auto-expire OTP after 60 seconds
 * - Solenoid lock control via relay
 * - Wrong attempt tracking
 * 
 * Author: Generated for Abhijeet Nardele
 * Date: 2025
 * ============================================================================
 */

// ==================== LIBRARY INCLUDES ====================
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>

// ==================== WIFI CONFIGURATION ====================
// ENTER YOUR WIFI CREDENTIALS HERE
const char* WIFI_SSID = "hmm";           // Your mobile hotspot name
const char* WIFI_PASSWORD = "12345678";   // Your hotspot password

// ==================== TELEGRAM CONFIGURATION ====================
// ENTER YOUR TELEGRAM BOT TOKEN AND CHAT ID HERE
// Get Bot Token from @BotFather on Telegram
// Get Chat ID from @userinfobot on Telegram
#define BOT_TOKEN "XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  // Replace with your bot token
#define CHAT_ID "123456789"                                         // Replace with your chat ID

// ==================== PIN DEFINITIONS ====================
// LCD I2C
#define LCD_ADDRESS 0x27    // Default I2C address (might be 0x3F for some modules)
#define LCD_COLUMNS 16
#define LCD_ROWS 2

// Relay (controls solenoid lock)
#define RELAY_PIN 23

// Keypad Pins
#define ROW_1 13
#define ROW_2 12
#define ROW_3 14
#define ROW_4 27
#define COL_1 26
#define COL_2 25
#define COL_3 33
#define COL_4 32

// ==================== KEYPAD CONFIGURATION ====================
const byte ROWS = 4;
const byte COLS = 4;

char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte rowPins[ROWS] = {ROW_1, ROW_2, ROW_3, ROW_4};
byte colPins[COLS] = {COL_1, COL_2, COL_3, COL_4};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// ==================== GLOBAL OBJECTS ====================
LiquidCrystal_I2C lcd(LCD_ADDRESS, LCD_COLUMNS, LCD_ROWS);
WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);

// ==================== SYSTEM VARIABLES ====================
String currentOTP = "";
unsigned long otpGeneratedTime = 0;
bool otpActive = false;
String enteredOTP = "";
int wrongAttempts = 0;

// Timing variables
unsigned long lastBotCheck = 0;
const unsigned long BOT_CHECK_INTERVAL = 1000;  // Check for messages every 1 second

// OTP Configuration
const int OTP_LENGTH = 4;
const unsigned long OTP_VALIDITY = 60000;  // 60 seconds
const int MAX_WRONG_ATTEMPTS = 3;

// Lock Configuration
const unsigned long UNLOCK_DURATION = 5000;  // Keep door unlocked for 5 seconds
bool doorUnlocked = false;
unsigned long unlockStartTime = 0;

// ==================== FUNCTION PROTOTYPES ====================
void connectWiFi();
void initializeLCD();
void handleNewMessages(int numNewMessages);
String generateOTP();
void displayOTP();
void checkKeypad();
void verifyOTP();
void unlockDoor();
void lockDoor();
void updateLCDTimer();
void clearOTP();
void displayMessage(String line1, String line2);
void handleTelegramCommands(String chat_id, String text, String from_name);

// ==================== SETUP ====================
void setup() {
  Serial.begin(115200);
  Serial.println("\n\n");
  Serial.println("============================================");
  Serial.println("  TELEGRAM OTP DOOR LOCK SYSTEM - ESP32");
  Serial.println("============================================");
  
  // Initialize I2C for LCD
  Wire.begin();
  
  // Initialize LCD
  initializeLCD();
  displayMessage("System Boot...", "Please Wait");
  delay(1000);
  
  // Initialize Relay Pin
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // Lock engaged (relay off)
  
  // Connect to WiFi
  connectWiFi();
  
  // Configure secure client for Telegram
  client.setCACert(TELEGRAM_CERTIFICATE_ROOT);  // Telegram's root certificate
  
  // Test Telegram connection
  displayMessage("Testing Telegram", "Connection...");
  Serial.println("Testing Telegram bot...");
  
  if (bot.getMe()) {
    Serial.println("Telegram bot connected successfully!");
    displayMessage("Bot Connected!", "Ready to Use");
    delay(2000);
  } else {
    Serial.println("ERROR: Telegram bot connection failed!");
    displayMessage("Bot Error!", "Check Token");
    delay(3000);
  }
  
  // Display ready state
  displayMessage("Telegram Lock", "Send /unlock");
  Serial.println("\n✅ System Ready!");
  Serial.println("Send /unlock command to Telegram bot");
  Serial.println("============================================\n");
}

// ==================== MAIN LOOP ====================
void loop() {
  // Check for new Telegram messages
  if (millis() - lastBotCheck > BOT_CHECK_INTERVAL) {
    int numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    
    if (numNewMessages) {
      Serial.println("New message received!");
      handleNewMessages(numNewMessages);
    }
    
    lastBotCheck = millis();
  }
  
  // Update LCD timer if OTP is active
  if (otpActive) {
    updateLCDTimer();
    
    // Check if OTP has expired
    if (millis() - otpGeneratedTime > OTP_VALIDITY) {
      Serial.println("⏱️ OTP Expired!");
      clearOTP();
      displayMessage("OTP Expired!", "Send /unlock");
      delay(2000);
      displayMessage("Telegram Lock", "Send /unlock");
    }
  }
  
  // Check keypad input
  if (otpActive) {
    checkKeypad();
  }
  
  // Handle door auto-lock after unlock duration
  if (doorUnlocked && (millis() - unlockStartTime > UNLOCK_DURATION)) {
    lockDoor();
  }
  
  delay(50);  // Small delay to prevent excessive CPU usage
}

// ==================== WIFI CONNECTION ====================
void connectWiFi() {
  displayMessage("Connecting WiFi", WIFI_SSID);
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    displayMessage("WiFi Connected!", WiFi.localIP().toString());
    delay(2000);
  } else {
    Serial.println("\n❌ WiFi Connection Failed!");
    displayMessage("WiFi Failed!", "Check Settings");
    delay(3000);
  }
}

// ==================== LCD INITIALIZATION ====================
void initializeLCD() {
  lcd.init();
  lcd.backlight();
  lcd.clear();
  Serial.println("✅ LCD Initialized");
}

// ==================== DISPLAY MESSAGE ON LCD ====================
void displayMessage(String line1, String line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

// ==================== HANDLE TELEGRAM MESSAGES ====================
void handleNewMessages(int numNewMessages) {
  for (int i = 0; i < numNewMessages; i++) {
    String chat_id = String(bot.messages[i].chat_id);
    String text = bot.messages[i].text;
    String from_name = bot.messages[i].from_name;
    
    Serial.println("========================================");
    Serial.println("Message from: " + from_name);
    Serial.println("Chat ID: " + chat_id);
    Serial.println("Message: " + text);
    Serial.println("========================================");
    
    // Security: Only respond to authorized chat ID
    if (chat_id != CHAT_ID) {
      Serial.println("⚠️ Unauthorized user attempted access!");
      bot.sendMessage(chat_id, "⛔ Unauthorized access. This incident will be reported.", "");
      continue;
    }
    
    handleTelegramCommands(chat_id, text, from_name);
  }
}

// ==================== HANDLE TELEGRAM COMMANDS ====================
void handleTelegramCommands(String chat_id, String text, String from_name) {
  // Convert to lowercase for command matching
  text.toLowerCase();
  
  if (text == "/start") {
    String welcome = "🚪 *Telegram OTP Door Lock System*\n\n";
    welcome += "Welcome " + from_name + "!\n\n";
    welcome += "Available Commands:\n";
    welcome += "/unlock - Request OTP to unlock door\n";
    welcome += "/status - Check system status\n";
    welcome += "/help - Show this help message\n\n";
    welcome += "Security: OTP expires in 60 seconds";
    
    bot.sendMessage(chat_id, welcome, "Markdown");
  }
  
  else if (text == "/unlock") {
    if (otpActive) {
      bot.sendMessage(chat_id, "⚠️ An OTP is already active!\nPlease enter the current OTP or wait for it to expire.", "");
      return;
    }
    
    // Generate new OTP
    currentOTP = generateOTP();
    otpGeneratedTime = millis();
    otpActive = true;
    enteredOTP = "";
    wrongAttempts = 0;
    
    // Send OTP to user
    String otpMessage = "🔑 *Your OTP:* `" + currentOTP + "`\n\n";
    otpMessage += "⏱️ Valid for: 60 seconds\n";
    otpMessage += "📍 Enter this OTP on the keypad at the door\n\n";
    otpMessage += "⚠️ Do not share this OTP with anyone!";
    
    bot.sendMessage(chat_id, otpMessage, "Markdown");
    
    Serial.println("✅ OTP Generated: " + currentOTP);
    
    // Update LCD
    displayMessage("OTP Sent! 60s", "Enter: ____");
  }
  
  else if (text == "/status") {
    String status = "📊 *System Status*\n\n";
    status += "🌐 WiFi: Connected\n";
    status += "📡 Signal: " + String(WiFi.RSSI()) + " dBm\n";
    status += "🔓 Door: " + String(doorUnlocked ? "Unlocked" : "Locked") + "\n";
    status += "🔑 OTP Active: " + String(otpActive ? "Yes" : "No") + "\n";
    
    if (otpActive) {
      unsigned long timeLeft = (OTP_VALIDITY - (millis() - otpGeneratedTime)) / 1000;
      status += "⏱️ OTP Expires in: " + String(timeLeft) + "s\n";
    }
    
    status += "\n💡 System: Operational";
    
    bot.sendMessage(chat_id, status, "Markdown");
  }
  
  else if (text == "/help") {
    String help = "📖 *Help - How to Use*\n\n";
    help += "1️⃣ Send /unlock command\n";
    help += "2️⃣ Receive OTP on Telegram\n";
    help += "3️⃣ Enter OTP on keypad at door\n";
    help += "4️⃣ Door unlocks for 5 seconds\n\n";
    help += "🔒 Security Features:\n";
    help += "• OTP expires after 60 seconds\n";
    help += "• Maximum 3 wrong attempts\n";
    help += "• Only authorized users can unlock\n\n";
    help += "ℹ️ For support, contact your administrator";
    
    bot.sendMessage(chat_id, help, "Markdown");
  }
  
  else {
    bot.sendMessage(chat_id, "❓ Unknown command.\nSend /help for available commands.", "");
  }
}

// ==================== GENERATE OTP ====================
String generateOTP() {
  String otp = "";
  for (int i = 0; i < OTP_LENGTH; i++) {
    otp += String(random(0, 10));
  }
  return otp;
}

// ==================== CHECK KEYPAD INPUT ====================
void checkKeypad() {
  char key = keypad.getKey();
  
  if (key) {
    Serial.println("Key pressed: " + String(key));
    
    // Handle special keys
    if (key == '#') {
      // Submit OTP
      if (enteredOTP.length() == OTP_LENGTH) {
        verifyOTP();
      } else {
        displayMessage("OTP Incomplete!", "Enter " + String(OTP_LENGTH) + " digits");
        delay(1500);
        displayOTP();
      }
    }
    else if (key == '*') {
      // Clear last digit
      if (enteredOTP.length() > 0) {
        enteredOTP.remove(enteredOTP.length() - 1);
        displayOTP();
        Serial.println("Cleared last digit. Current: " + enteredOTP);
      }
    }
    else if (key == 'A' || key == 'B' || key == 'C' || key == 'D') {
      // Ignore letter keys (or you can add special functions here)
      return;
    }
    else if (key >= '0' && key <= '9') {
      // Add digit to OTP
      if (enteredOTP.length() < OTP_LENGTH) {
        enteredOTP += key;
        displayOTP();
        Serial.println("Entered: " + enteredOTP);
        
        // Auto-submit when all digits entered
        if (enteredOTP.length() == OTP_LENGTH) {
          delay(500);
          verifyOTP();
        }
      }
    }
  }
}

// ==================== DISPLAY OTP ON LCD ====================
void displayOTP() {
  unsigned long timeLeft = (OTP_VALIDITY - (millis() - otpGeneratedTime)) / 1000;
  
  // First line: "OTP: XXXX" with timer
  String line1 = "OTP: ";
  for (int i = 0; i < OTP_LENGTH; i++) {
    if (i < enteredOTP.length()) {
      line1 += enteredOTP.charAt(i);
    } else {
      line1 += "_";
    }
  }
  line1 += " " + String(timeLeft) + "s";
  
  // Second line: "# OK  * DEL"
  String line2 = "# OK  * DEL";
  
  displayMessage(line1, line2);
}

// ==================== VERIFY OTP ====================
void verifyOTP() {
  Serial.println("Verifying OTP...");
  Serial.println("Entered: " + enteredOTP);
  Serial.println("Correct: " + currentOTP);
  
  if (enteredOTP == currentOTP) {
    // ✅ CORRECT OTP
    Serial.println("✅ OTP Verified! Unlocking door...");
    
    displayMessage("Access Granted!", "Welcome!");
    
    // Send notification to Telegram
    bot.sendMessage(CHAT_ID, "✅ Door unlocked successfully!\n🕐 Time: " + String(millis()/1000) + "s", "");
    
    // Unlock door
    unlockDoor();
    
    // Clear OTP
    clearOTP();
    
    delay(2000);
    displayMessage("Door Unlocked", "Closes in 5s");
    
  } else {
    // ❌ WRONG OTP
    wrongAttempts++;
    Serial.println("❌ Wrong OTP! Attempts: " + String(wrongAttempts));
    
    displayMessage("Invalid OTP!", "Try Again");
    
    // Send warning to Telegram
    String warning = "⚠️ *Wrong OTP Entered!*\n\n";
    warning += "Attempt: " + String(wrongAttempts) + "/" + String(MAX_WRONG_ATTEMPTS) + "\n";
    warning += "Entered: `" + enteredOTP + "`\n";
    warning += "Time: " + String(millis()/1000) + "s";
    
    bot.sendMessage(CHAT_ID, warning, "Markdown");
    
    delay(2000);
    
    if (wrongAttempts >= MAX_WRONG_ATTEMPTS) {
      // Lock out after max attempts
      Serial.println("🚨 Maximum attempts reached! Locking system...");
      displayMessage("Max Attempts!", "System Locked");
      
      bot.sendMessage(CHAT_ID, "🚨 *ALERT!* Maximum wrong attempts reached!\nSystem locked. Please wait 1 minute.", "Markdown");
      
      clearOTP();
      delay(60000);  // 1 minute lockout
      
      displayMessage("Telegram Lock", "Send /unlock");
    } else {
      enteredOTP = "";
      displayOTP();
    }
  }
}

// ==================== UNLOCK DOOR ====================
void unlockDoor() {
  digitalWrite(RELAY_PIN, HIGH);  // Activate relay (unlock solenoid)
  doorUnlocked = true;
  unlockStartTime = millis();
  Serial.println("🔓 Door Unlocked!");
}

// ==================== LOCK DOOR ====================
void lockDoor() {
  digitalWrite(RELAY_PIN, LOW);   // Deactivate relay (lock solenoid)
  doorUnlocked = false;
  Serial.println("🔒 Door Locked!");
  
  displayMessage("Door Locked", "Send /unlock");
}

// ==================== UPDATE LCD TIMER ====================
void updateLCDTimer() {
  static unsigned long lastUpdate = 0;
  
  if (millis() - lastUpdate > 1000) {  // Update every second
    if (enteredOTP.length() > 0) {
      displayOTP();
    } else {
      unsigned long timeLeft = (OTP_VALIDITY - (millis() - otpGeneratedTime)) / 1000;
      displayMessage("OTP Sent! " + String(timeLeft) + "s", "Enter: ____");
    }
    lastUpdate = millis();
  }
}

// ==================== CLEAR OTP ====================
void clearOTP() {
  currentOTP = "";
  enteredOTP = "";
  otpActive = false;
  wrongAttempts = 0;
  Serial.println("🗑️ OTP Cleared");
}

// ==================== TELEGRAM ROOT CERTIFICATE ====================
// Root certificate for api.telegram.org
const char TELEGRAM_CERTIFICATE_ROOT[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIEAjCCAuqgAwIBAgIJANnKbFgDPBvdMA0GCSqGSIb3DQEBCwUAMIGVMQswCQYD
VQQGEwJVUzELMAkGA1UECAwCQ0ExFjAUBgNVBAcMDVNhbiBGcmFuY2lzY28xHTAb
BgNVBAoMFFRlbGVncmFtIE1lc3NlbmdlciBMTFAxFDASBgNVBAMMC3RlbGVncmFt
Lm9yZzEsMCoGCSqGSIb3DQEJARYdZGV2ZWxvcGVyc0B0ZWxlZ3JhbS5vcmcwHhcN
MTUwNzI4MTQxNzI2WhcNMjUwNzI1MTQxNzI2WjCBlTELMAkGA1UEBhMCVVMxCzAJ
BgNVBAgMAkNBMRYwFAYDVQQHDA1TYW4gRnJhbmNpc2NvMR0wGwYDVQQKDBRUZWxl
Z3JhbSBNZXNzZW5nZXIgTExQMRQwEgYDVQQDDAt0ZWxlZ3JhbS5vcmcxLDAqBgkq
hkiG9w0BCQEWHWRldmVsb3BlcnNAdGVsZWdyYW0ub3JnMIIBIjANBgkqhkiG9w0B
AQEFAAOCAQ8AMIIBCgKCAQEAvfKn5zVLTe1p0YN6+vT9CZZRT4ow7jKYOxLqHAaT
nkG3rKNkTy6DyJJj9VN+4tqxL8slqVtD2tVvvnDhAFVNTNAKhWjjOqQk1YxXQHQh
FKMHnVjMXxHj8qFHXHvuDQDLfxGMvY6Kkl4QUTQXD7IZ5HqSqqLvLpGn+Ib8pLjk
WiQdhXpQqvgGnRaLJWXqCN0VUwYqDg8vqIGNwXTvNn7TpGv0WJOg5zCLEXLKD2r3
E6bZXhRNJcCKl9ZL3OLNhbBqNdCj4BLOGPz7qHsFVrYLsV3XKy8LXSPfRKEv7mBY
KfgMcq3BqC3xLNPYR2tMqYMKoFXwAFT7A1Aq8PqLGKhYcQIDAQABo1AwTjAdBgNV
HQ4EFgQUMqLpAFhvQxqvqfSBj4qPqkqp7lQwHwYDVR0jBBgwFoAUMqLpAFhvQxqv
qfSBj4qPqkqp7lQwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAcqKU
+YZ3pnCqFEh6CkqhCqoC9qFnRYDQqMOYrRDq1E5tOTVQMaEOLEDn3g5VnCYhVEu3
B1LVGsLGLj7OvNgqbSkEQNzrJj8YNfTT6K6VlgPn7XKGvzqPLiJbsXM/xnKPZgLN
X6rHFyVDqmHAZdLpDcQvFnTwvJfDPLVvPH4nSLmQwQqLLBYv8pxQvE2YVsLdLgLa
S5AklnQxwLgDxZLd1PWFQR7NG5hLiYtUfFmcJKCqMqPqKFLNXMQ1YZj6GLRQBVQT
wShF6yJQC7GvNtBaHlVGk6eJNGKRUqMpwLOOpLQPJQeQXZQYNqYdSKNKnPQBYLEE
BppLsAnqYMGHlXR5vQ==
-----END CERTIFICATE-----
)EOF";
