import digitalio
import board
from PIL import Image
import adafruit_rgb_display.st7789 as st7789

# 디스플레이 설정
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
spi = board.SPI()

disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=24000000,
    width=240,
    height=240,
    x_offset=0,
    y_offset=80,
    rotation=270,  # 디스플레이의 기본 회전
)

# 이미지 로드 및 크기 조정
image = Image.open("blinka.jpg")

# 이미지 크기를 디스플레이 크기(240x240)에 맞춤
image = image.resize((240, 240), Image.BICUBIC)

# 필요한 경우 회전
rotated_image = image.rotate(-90, expand=False)  # 반시계 방향으로 90도 회전

# 이미지를 디스플레이에 출력
disp.image(rotated_image)
