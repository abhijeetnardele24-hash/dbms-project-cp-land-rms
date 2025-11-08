"""
Telegram OTP Door Lock - Cardboard Layout Image Generator
This script creates a visual diagram of the component placement
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import matplotlib.lines as mlines

# Create figure with two subplots (front and back view)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 12))

# ==================== FRONT VIEW ====================
ax1.set_xlim(0, 30)
ax1.set_ylim(0, 40)
ax1.set_aspect('equal')
ax1.set_title('FRONT VIEW (User Side)\nCardboard: 30cm x 40cm', 
              fontsize=16, fontweight='bold', pad=20)
ax1.set_xlabel('Width (cm)', fontsize=12)
ax1.set_ylabel('Height (cm)', fontsize=12)
ax1.grid(True, alpha=0.3, linestyle='--')

# Cardboard border
border = Rectangle((0, 0), 30, 40, linewidth=3, 
                   edgecolor='brown', facecolor='wheat', alpha=0.3)
ax1.add_patch(border)

# Title banner
title_banner = FancyBboxPatch((2, 36), 26, 3, 
                             boxstyle="round,pad=0.1",
                             edgecolor='navy', facecolor='lightblue',
                             linewidth=2)
ax1.add_patch(title_banner)
ax1.text(15, 37.5, 'TELEGRAM OTP DOOR LOCK', 
         ha='center', va='center', fontsize=14, fontweight='bold')

# LCD Display (8cm x 3.6cm at position 5,30)
lcd = FancyBboxPatch((5, 30), 8, 3.6,
                     boxstyle="round,pad=0.05",
                     edgecolor='blue', facecolor='darkblue',
                     linewidth=2)
ax1.add_patch(lcd)
# LCD screen
lcd_screen = Rectangle((5.3, 30.3), 7.4, 3,
                       edgecolor='lightblue', facecolor='navy',
                       linewidth=1)
ax1.add_patch(lcd_screen)
ax1.text(9, 32, 'Telegram Lock', ha='center', va='center',
         color='cyan', fontsize=9, family='monospace')
ax1.text(9, 31.2, 'Send /unlock', ha='center', va='center',
         color='cyan', fontsize=8, family='monospace')
ax1.text(9, 28, 'LCD1602\nDisplay', ha='center', va='top',
         fontsize=9, fontweight='bold', style='italic')

# 4x4 Keypad (7cm x 7cm at position 11.5, 18)
keypad = Rectangle((11.5, 18), 7, 7,
                   edgecolor='black', facecolor='lightgray',
                   linewidth=2)
ax1.add_patch(keypad)

# Keypad buttons (4x4 grid)
keys = [['1','2','3','A'], ['4','5','6','B'], 
        ['7','8','9','C'], ['*','0','#','D']]
for row in range(4):
    for col in range(4):
        btn_x = 12 + col * 1.6
        btn_y = 23.5 - row * 1.6
        btn = FancyBboxPatch((btn_x, btn_y), 1.3, 1.3,
                            boxstyle="round,pad=0.05",
                            edgecolor='black', facecolor='white',
                            linewidth=1)
        ax1.add_patch(btn)
        ax1.text(btn_x + 0.65, btn_y + 0.65, keys[row][col],
                ha='center', va='center', fontsize=11, fontweight='bold')

ax1.text(15, 16.5, '4×4 Keypad', ha='center', va='top',
         fontsize=9, fontweight='bold', style='italic')

# Solenoid Lock (5cm x 3cm at position 12.5, 8)
lock_body = Rectangle((12.5, 8), 5, 3,
                      edgecolor='darkred', facecolor='silver',
                      linewidth=2)
ax1.add_patch(lock_body)
lock_bolt = Rectangle((14.7, 9.2), 3, 0.6,
                     edgecolor='black', facecolor='gold',
                     linewidth=2)
ax1.add_patch(lock_bolt)
ax1.text(15, 6.5, '12V Solenoid\nLock', ha='center', va='top',
         fontsize=9, fontweight='bold', style='italic', color='darkred')

# WiFi indicator
wifi_circle = Circle((3, 3), 0.5, color='green', alpha=0.7)
ax1.add_patch(wifi_circle)
ax1.text(3, 1.5, 'WiFi', ha='center', fontsize=8, fontweight='bold')

# Power LED
power_circle = Circle((27, 3), 0.5, color='red', alpha=0.7)
ax1.add_patch(power_circle)
ax1.text(27, 1.5, 'Power', ha='center', fontsize=8, fontweight='bold')

# ==================== BACK VIEW ====================
ax2.set_xlim(0, 30)
ax2.set_ylim(0, 40)
ax2.set_aspect('equal')
ax2.set_title('BACK VIEW (Electronics Side)\nCardboard: 30cm x 40cm',
              fontsize=16, fontweight='bold', pad=20)
ax2.set_xlabel('Width (cm)', fontsize=12)
ax2.set_ylabel('Height (cm)', fontsize=12)
ax2.grid(True, alpha=0.3, linestyle='--')

# Cardboard border
border2 = Rectangle((0, 0), 30, 40, linewidth=3,
                   edgecolor='brown', facecolor='wheat', alpha=0.3)
ax2.add_patch(border2)

# Power Adapter Jack (3cm x 2cm at position 20, 35)
power_jack = FancyBboxPatch((20, 35), 3, 2,
                           boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor='yellow',
                           linewidth=2)
ax2.add_patch(power_jack)
ax2.text(21.5, 36, '12V DC\nInput', ha='center', va='center',
         fontsize=8, fontweight='bold')
ax2.text(21.5, 33.5, 'Power Jack', ha='center', va='top',
         fontsize=8, style='italic')

# Buck Converter (4cm x 2cm at position 15, 33)
buck = Rectangle((15, 33), 4, 2,
                edgecolor='purple', facecolor='mediumpurple',
                linewidth=2)
ax2.add_patch(buck)
ax2.text(17, 34, 'Buck\n12V→5V', ha='center', va='center',
         fontsize=8, fontweight='bold', color='white')
ax2.text(17, 31.5, 'Buck Converter', ha='center', va='top',
         fontsize=8, style='italic')

# Power line from jack to buck
ax2.plot([21.5, 17], [35, 35], 'r-', linewidth=2)
ax2.plot([17, 17], [35, 35], 'r-', linewidth=2)

# ESP32 (5cm x 2.5cm at position 8, 22)
esp32 = Rectangle((8, 22), 5, 2.5,
                 edgecolor='blue', facecolor='darkslateblue',
                 linewidth=2)
ax2.add_patch(esp32)
ax2.text(10.5, 23.2, 'ESP32', ha='center', va='center',
         fontsize=10, fontweight='bold', color='white')
ax2.text(10.5, 22.5, 'WROOM', ha='center', va='center',
         fontsize=7, color='lightblue')

# ESP32 pins
for i in range(10):
    ax2.plot([8.3 + i*0.45, 8.3 + i*0.45], [22, 21.7], 'gold', linewidth=1.5)
    ax2.plot([8.3 + i*0.45, 8.3 + i*0.45], [24.5, 24.8], 'gold', linewidth=1.5)

ax2.text(10.5, 20.5, 'ESP32 WROOM\n(Microcontroller)', ha='center', va='top',
         fontsize=8, style='italic', fontweight='bold')

# USB port on ESP32
usb_port = Rectangle((7.5, 23), 0.5, 0.5,
                     edgecolor='black', facecolor='silver',
                     linewidth=1)
ax2.add_patch(usb_port)

# Relay Module (4cm x 3cm at position 8, 14)
relay = Rectangle((8, 14), 4, 3,
                 edgecolor='darkgreen', facecolor='lightgreen',
                 linewidth=2)
ax2.add_patch(relay)
# Relay cube
relay_cube = FancyBboxPatch((9, 15), 2, 1.5,
                           boxstyle="round,pad=0.05",
                           edgecolor='black', facecolor='blue',
                           linewidth=1.5)
ax2.add_patch(relay_cube)
ax2.text(10, 15.75, 'RELAY', ha='center', va='center',
         fontsize=7, fontweight='bold', color='white')
ax2.text(10, 12.5, '5V Relay\nModule', ha='center', va='top',
         fontsize=8, style='italic', fontweight='bold')

# Solenoid Lock (back view - 5cm x 3cm at position 12.5, 8)
lock_back = Rectangle((12.5, 8), 5, 3,
                     edgecolor='darkred', facecolor='dimgray',
                     linewidth=2, linestyle='--', alpha=0.5)
ax2.add_patch(lock_back)
ax2.text(15, 9.5, 'Solenoid\n(through\ncardboard)', ha='center', va='center',
         fontsize=7, style='italic')

# Wiring connections
# Power from buck to ESP32
ax2.plot([17, 17, 10.5], [33, 28, 24.5], 'r-', linewidth=2, label='5V Power')
# Power from buck to relay
ax2.plot([17, 10], [33, 17], 'r--', linewidth=1.5)
# ESP32 to relay control
ax2.plot([10.5, 10], [22, 17], 'orange', linewidth=1.5, label='Control Signal')
# Relay to solenoid
ax2.plot([10, 15], [14, 11], 'darkred', linewidth=2, label='12V to Lock')
# 12V from jack to solenoid
ax2.plot([21.5, 21.5, 15], [35, 11, 11], 'r:', linewidth=1.5)

# Cable management area
cable_area = FancyBboxPatch((1, 1), 6, 4,
                           boxstyle="round,pad=0.1",
                           edgecolor='gray', facecolor='none',
                           linewidth=1, linestyle='--')
ax2.add_patch(cable_area)
ax2.text(4, 2.5, 'Cable\nManagement\nZone', ha='center', va='center',
         fontsize=7, style='italic', color='gray')

# Legend for back view
legend_elements = [
    mlines.Line2D([0], [0], color='r', linewidth=2, label='5V Power'),
    mlines.Line2D([0], [0], color='r', linewidth=2, linestyle='--', label='12V Power'),
    mlines.Line2D([0], [0], color='orange', linewidth=1.5, label='Control Signal'),
]
ax2.legend(handles=legend_elements, loc='upper left', fontsize=8)

# Add measurement annotations
ax1.annotate('', xy=(5, 41), xytext=(13, 41),
            arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
ax1.text(9, 41.5, '8cm', ha='center', fontsize=8, color='red', fontweight='bold')

ax1.annotate('', xy=(19, 18), xytext=(19, 25),
            arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
ax1.text(20.5, 21.5, '7cm', ha='center', fontsize=8, color='red', 
         fontweight='bold', rotation=90)

plt.tight_layout()

# Save the image
output_file = 'Telegram_OTP_Door_Lock_Layout.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ Layout diagram saved as: {output_file}")
print(f"📍 Location: {output_file}")
print("\nOpen the image to see your cardboard layout!")

# Also save high quality version
plt.savefig('Telegram_OTP_Door_Lock_Layout_HD.png', dpi=600, 
           bbox_inches='tight', facecolor='white')
print(f"✅ HD version saved as: Telegram_OTP_Door_Lock_Layout_HD.png")

plt.show()
