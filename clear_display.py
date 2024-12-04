import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789
from digitalio import DigitalInOut

# 디스플레이 핀 및 설정
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000
spi = board.SPI()

disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=240,
    x_offset=0,
    y_offset=80,
)

# 화면 초기화
width = disp.height
height = disp.width
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

# 검정색으로 화면 초기화
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

# 백라이트 끄기
backlight = DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = False

print("Display cleared and backlight turned off.")
