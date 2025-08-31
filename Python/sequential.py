import argparse
from PIL import Image
import time


def load_image(filepath):
    image = Image.open(filepath).convert('RGB')
    pixels = image.load()
    width, height = image.size
    return pixels, width, height

def apply_grayscale(pixels, width, height):
    result = Image.new('L', (width, height))
    new_pixels = result.load()
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            new_pixels[x, y] = gray
    
    result.save('grayscale.bmp')
    return result

def apply_hsv(pixels, width, height):
    hue_img = Image.new('L', (width, height))
    sat_img = Image.new('L', (width, height))
    val_img = Image.new('L', (width, height))
    
    hue_pixels = hue_img.load()
    sat_pixels = sat_img.load()
    val_pixels = val_img.load()
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            r_norm, g_norm, b_norm = r/255.0, g/255.0, b/255.0
            cmax = max(r_norm, g_norm, b_norm)
            cmin = min(r_norm, g_norm, b_norm)
            delta = cmax - cmin
            
            # Value
            v = int(cmax * 255)
            
            # Saturation
            s = int((delta / cmax * 255) if cmax != 0 else 0)
            
            # Hue
            if delta == 0:
                h = 0
            else:
                if cmax == r_norm:
                    h = 60 * (((g_norm - b_norm) / delta) % 6)
                elif cmax == g_norm:
                    h = 60 * (((b_norm - r_norm) / delta) + 2)
                else:
                    h = 60 * (((r_norm - g_norm) / delta) + 4)
                if h < 0:
                    h += 360
            h = int((h / 360) * 255)
            
            hue_pixels[x, y] = h
            sat_pixels[x, y] = s
            val_pixels[x, y] = v
    
    hue_img.save('hue.bmp')
    sat_img.save('saturation.bmp')
    val_img.save('value.bmp')
    return hue_img, sat_img, val_img
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filter", choices=['g', 'hsv'], help="Filter: g za grayscale, hsv za HSV")
    args = parser.parse_args()
    
    pixels, width, height = load_image('../input.png')
    
    start_time = time.time()
    
    if args.filter == 'g':
        apply_grayscale(pixels, width, height)
    
    elif args.filter == 'hsv':
        apply_hsv(pixels, width, height)
    else:
        raise Exception('Pogresan argument')
        
    
    end_time = time.time()
    print(f"Vrijeme izvođenja: {end_time - start_time:.4f} s")