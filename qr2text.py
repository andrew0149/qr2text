import argparse
import sys
from PIL import Image

BLACK = 0
WHITE = 255
COLOR_BORDER = 128
inverted = False
alphabet = [' ', '▄', '▀', '█']

def make_pixels_bw(img_pixels, width, height):
    for y in range(height):
        for x in range(width):
            img_pixels[x, y] = BLACK if img_pixels[x, y] < 128 else WHITE
    return img_pixels

def detect_qr_borders(img_pixels, width, height):
    left = width
    right = -1
    upper = height
    lower = -1
    found = False
    for y in range(height):
        for x in range(width):
            if img_pixels[x, y] == BLACK:
                left = x
                upper = y
                found = True
                break
        if found:
            break
    found = False
    for y in range(height - 1, -1, -1):
        for x in range(width - 1, -1, -1):
            if img_pixels[x, y] == BLACK:
                right = x
                lower = y
                found = True
                break
        if found:
            break
    return left, upper, right + 1, lower + 1

def detect_qr_scale(img_pixels, width):
    scale = 1
    for x in range(width):
        if img_pixels[x, x] == 255:
            scale = x
            break
    return scale

def get_normalized_image_pixels(image_name):
    img = Image.open(input_file).convert('L')
    pixels = img.load()
    width, height = img.size

    pixels = make_pixels_bw(pixels, width, height)
    img = img.crop(detect_qr_borders(pixels, width, height))
    
    width, height = img.size
    pixels = img.load()

    scale = detect_qr_scale(pixels, width)

    normalized = [[WHITE for x in range(width // scale)] for y in range(height // scale)]
    
    for y in range(0, height, scale):
        for x in range(0, width, scale):
            if pixels[x,y] == BLACK:
                normalized[x // scale][y // scale] = BLACK

    img.close()
    return normalized

def get_upscaled_image_pixels(img_pixels, scale):
    width = len(img_pixels)
    height = len(img_pixels[0])
    upscaled = [[img_pixels[x // scale][y // scale] for x in range(width * scale)] for y in range(height * scale)]
    return upscaled

def get_symbol(color_a, color_b=None, inverted=False):
    if color_b == None:
        color_b = BLACK if inverted else WHITE
    if color_a == WHITE and color_b == WHITE:
        symbol_number = 0
    elif color_a == WHITE and color_b == BLACK:
        symbol_number = 1
    elif color_a == BLACK and color_b == WHITE:
        symbol_number = 2
    else:
        symbol_number = 3
    symbol = alphabet[symbol_number if not inverted else -symbol_number - 1]
    return symbol

def parse_text_from_pixels(img_pixels):
    width = len(pixels)
    height = len(pixels[0])
    text = ''
    for y in range(0, height - 1, 2):
        line = ''
        for x in range(width):
            line += get_symbol(pixels[x][y], pixels[x][y + 1], inverted)
        text += line + '\n'
    if height % 2 == 1:
        for x in range(0, width, 1):
            text += get_symbol(pixels[x][height - 1], inverted=inverted)
    if text[-1] == '\n':
        text = text[:-1]
    return text

parser = argparse.ArgumentParser(
    description='Turn QR-code image into a Unicode text which looks exactly the same.')
parser.add_argument(
    'input_file', 
    help='input image filename (png/jpg)')
parser.add_argument(
    '--outputfile', '-of', 
    help='output text file name (txt)')
parser.add_argument(
    '--inverted', '-i', 
    help='use this argument to invert colors of the result', 
    action='store_true')
parser.add_argument(
    '--scale', '-s', 
    help='1x1 pixel of original qr-code will be replaced with SCALExSCALE pixels in the result (>=1)')

arguments = parser.parse_args()
input_file = arguments.input_file
inverted = arguments.inverted
output_file = arguments.outputfile

scale = 1
try:
    scale = int(arguments.scale)
    if scale < 1:
        raise ValueError
except Exception:
    print('Invalid scale!')
    exit()

pixels = get_normalized_image_pixels(input_file)

if scale > 1:
    pixels = get_upscaled_image_pixels(pixels, scale)

text = parse_text_from_pixels(pixels)

if output_file == None:
    print(text)
else:
    with open(output_file, 'w', encoding='UTF-8') as output:
        output.write(text)