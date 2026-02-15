from picamera2 import Picamera2
import time

# Initialize and configure the camera once
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (2592, 1944)})  # Use preview config for speed
picam2.configure(config)
picam2.start()
time.sleep(2)  # Initial camera warm-up
picam2.options["quality"] = 100
print("init finish")

# Now captures are very fast
for i in range(3):
    picam2.capture_file(f"fast_image_{i}.png")
    print(f"Captured image {i}")
    # Small pause if needed between shots
    time.sleep(0.1)

picam2.stop()
print("Done.")