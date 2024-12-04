import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

# Constants for shapes and text
BORDER = 20
FONTSIZE = 24

# Pin configuration for the display
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI
spi = board.SPI()

# Create the display with correct offset and rotation
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=240,
    x_offset=0,  # Adjust as needed
    y_offset=80,  # Adjust to correct vertical position
    rotation=180,  # Adjust rotation if necessary
)

# Create blank image for drawing
if disp.rotation % 180 == 90:
    height = disp.width
    width = disp.height
else:
    width = disp.width
    height = disp.height

image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

# Draw a green background
draw.rectangle((0, 0, width, height), fill=(0, 255, 0))

# Draw a purple border
draw.rectangle(
    (BORDER, BORDER, width - BORDER, height - BORDER),
    fill=(170, 0, 136),
)

# Load a font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

# Draw centered text
text = "Hello World!"
(font_width, font_height) = font.getsize(text)
text_x = (width - font_width) // 2
text_y = (height - font_height) // 2
draw.text((text_x, text_y), text, font=font, fill=(255, 255, 0))

# Display the image on the screen
disp.image(image)
