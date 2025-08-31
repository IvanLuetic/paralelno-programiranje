import argparse
from PIL import Image
import time
from multiprocessing import Pool
import os


def load_image(filepath):
    image = Image.open(filepath).convert('RGB')
    width, height = image.size
    pixels_array = list(image.getdata())
    return pixels_array, width, height

def process_grayscale_chunk(args):
    start_idx, end_idx, width, pixels_array = args
    chunk_result = []
    
    for i in range(start_idx, end_idx):
        r, g, b = pixels_array[i]
        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        x = i % width
        y = i // width
        chunk_result.append((x, y, gray))
    
    return chunk_result

def apply_grayscale_parallel(pixels_array, width, height):
    num_processes = os.cpu_count()
    total_pixels = len(pixels_array)
    chunk_size = total_pixels // num_processes
    
    chunks = []
    for i in range(num_processes):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < num_processes - 1 else total_pixels
        chunks.append((start_idx, end_idx, width, pixels_array))
    
    with Pool(num_processes) as pool:
        results = pool.map(process_grayscale_chunk, chunks)
    
    result_img = Image.new('L', (width, height))
    new_pixels = result_img.load()
    
    for chunk in results:
        for x, y, gray in chunk:
            new_pixels[x, y] = gray
    
    result_img.save('grayscale.bmp')
    return 

def process_hsv_chunk(args):
    start_idx, end_idx, width, pixels_array = args
    hue_chunk = []
    sat_chunk = []
    val_chunk = []
    
    for idx in range(start_idx, end_idx):
        r, g, b = pixels_array[idx]
        
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
        
        x = idx % width
        y = idx // width
        
        hue_chunk.append((x, y, h))
        sat_chunk.append((x, y, s))
        val_chunk.append((x, y, v))
    
    return hue_chunk, sat_chunk, val_chunk

def apply_hsv_parallel(pixels_array, width, height):
    num_processes = os.cpu_count()
    total_pixels = len(pixels_array)
    chunk_size = total_pixels // num_processes
    
    chunks = []
    for i in range(num_processes):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < num_processes - 1 else total_pixels
        chunks.append((start_idx, end_idx, width, pixels_array))
    
    with Pool(num_processes) as pool:
        results = pool.map(process_hsv_chunk, chunks)
    
    hue_img = Image.new('L', (width, height))
    sat_img = Image.new('L', (width, height))
    val_img = Image.new('L', (width, height))
    
    hue_pixels = hue_img.load()
    sat_pixels = sat_img.load()
    val_pixels = val_img.load()
    
    for hue_chunk, sat_chunk, val_chunk in results:
        for x, y, h in hue_chunk:
            hue_pixels[x, y] = h
        for x, y, s in sat_chunk:
            sat_pixels[x, y] = s
        for x, y, v in val_chunk:
            val_pixels[x, y] = v
    
    hue_img.save('hue.bmp')
    sat_img.save('saturation.bmp')
    val_img.save('value.bmp')
    return 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filter", choices=['g', 'hsv'], help="Filter: g za grayscale, hsv za HSV")
    args = parser.parse_args()
    
    pixels_array, width, height = load_image('../input.png')
    
    start_time = time.time()
    
    if args.filter == 'g':
        apply_grayscale_parallel(pixels_array, width, height)

    
    elif args.filter == 'hsv':
        apply_hsv_parallel(pixels_array, width, height)
    
    end_time = time.time()
    print(f"Vrijeme izvođenja: {end_time - start_time:.4f} s")

   