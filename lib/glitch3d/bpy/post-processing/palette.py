
from PIL import Image
import sys, os, cv2, code
from ast import literal_eval as make_tuple
from PIL import ImageDraw

# Print a palette image representation
COLORS = sys.argv[1:]
SLOT_WIDTH = 400
img = Image.new('RGBA', (len(COLORS) * SLOT_WIDTH, SLOT_WIDTH), (255,255,255,255))
draw_context = ImageDraw.Draw(img)

for idx, color in enumerate(COLORS):
  actual_color = list((map(lambda x: int(x * 255), make_tuple(color))))
  draw_context.rectangle((((SLOT_WIDTH * idx), 0), (SLOT_WIDTH * idx + SLOT_WIDTH, SLOT_WIDTH)), fill=tuple(actual_color), outline=None)

img.save(os.environ['RENDER_PATH'] + "palette.png")