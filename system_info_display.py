import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789  # Adafruit ST7789 라이브러리

# 핀 구성
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# 디스플레이 초기화
spi = board.SPI()
disp = st7789.ST7789(
    spi,
    rotation=180,  # 1.3" 디스플레이는 240x240 픽셀
    width=240,
    height=240,
    x_offset=0,
    y_offset=80,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=24000000,
)

# 빈 이미지 생성
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

# 글꼴 설정 (라즈베리파이에 기본 설치된 DejaVuSans.ttf 사용)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# 루프 시작
while True:
    # 화면 초기화
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    # 시스템 정보 수집
    cmd = "hostname -I | cut -d' ' -f1"
    IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

    cmd = "cat /sys/class/thermal/thermal_zone0/temp | awk '{printf \"CPU Temp: %.1f C\", $1 / 1000}'"
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

    # 텍스트 출력
    y = 0
    draw.text((0, y), IP, font=font, fill="#FFFFFF")
    y += font.getsize(IP)[1]
    draw.text((0, y), CPU, font=font, fill="#FFFF00")
    y += font.getsize(CPU)[1]
    draw.text((0, y), MemUsage, font=font, fill="#00FF00")
    y += font.getsize(MemUsage)[1]
    draw.text((0, y), Disk, font=font, fill="#0000FF")
    y += font.getsize(Disk)[1]
    draw.text((0, y), Temp, font=font, fill="#FF00FF")

    # 디스플레이에 이미지 표시
    disp.image(image)
    time.sleep(0.5)
