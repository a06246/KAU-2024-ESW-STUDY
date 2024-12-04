import digitalio
import board

# 백라이트를 GPIO 핀 D26에 연결
backlight = digitalio.DigitalInOut(board.D26)
backlight.switch_to_output()

# 백라이트 켜기
backlight.value = True
print("Backlight is ON!")
