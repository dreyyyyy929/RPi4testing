import st7789
import board
import digitalio

# Use your pins - IO2 (GPIO 24) as DC pin
tft = st7789.ST7789(
    board.SPI(),
    width=240,        # Use 240x240 square area
    height=240,
    cs=0,     # CE0
    dc=digitalio.DigitalInOut(board.D24),     # IO2 as DC pin
    rst=digitalio.DigitalInOut(board.D25),    # RST pin
    rotation=0,
    spi_speed_hz=40000000,
)

# That's it! Now use it like any ST7789 display:
tft.fill(st7789.RED)           # Fill with red
tft.rect(10, 10, 100, 100, st7789.GREEN)  # Draw rectangle