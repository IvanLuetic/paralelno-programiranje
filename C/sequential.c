#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

void apply_grayscale(unsigned char* data, int width, int height) {
    int total_pixels = width * height;
    
    for (int i = 0; i < total_pixels; i++) {
        int idx = i * 3;
        unsigned char gray = (unsigned char)(0.299f * data[idx] + 0.587f * data[idx + 1] + 0.114f * data[idx + 2]);
        data[idx] = data[idx + 1] = data[idx + 2] = gray;
    }
    
    stbi_write_bmp("grayscale.bmp", width, height, 3, data);
    
}

void apply_hsv(unsigned char* data, int width, int height) {
    int total_pixels = width * height;
    int data_size = total_pixels * 3;
    
    unsigned char* hue_data = malloc(data_size);
    unsigned char* sat_data = malloc(data_size);
    unsigned char* val_data = malloc(data_size);
    
    if (!hue_data || !sat_data || !val_data) {
        printf("Greska sa alokacijom memorije\n");
        return;
    }
    
    for (int i = 0; i < total_pixels; i++) {
        int idx = i * 3;
        
        float r = data[idx] / 255.0f;
        float g = data[idx + 1] / 255.0f;
        float b = data[idx + 2] / 255.0f;
        
        float cmax = fmaxf(fmaxf(r, g), b);
        float cmin = fminf(fminf(r, g), b);
        float delta = cmax - cmin;
        
        // Value
        unsigned char v = (unsigned char)(cmax * 255);
        
        // Saturation
        unsigned char s = (unsigned char)(cmax != 0 ? (delta / cmax * 255) : 0);
        
        // Hue
        float h = 0;
        if (delta != 0) {
            if (cmax == r) {
                h = 60 * fmodf((g - b) / delta, 6);
            } else if (cmax == g) {
                h = 60 * (((b - r) / delta) + 2);
            } else {
                h = 60 * (((r - g) / delta) + 4);
            }
            if (h < 0) h += 360;
        }
        unsigned char h_value = (unsigned char)((h / 360) * 255);
        
        hue_data[idx] = hue_data[idx + 1] = hue_data[idx + 2] = h_value;
        sat_data[idx] = sat_data[idx + 1] = sat_data[idx + 2] = s;
        val_data[idx] = val_data[idx + 1] = val_data[idx + 2] = v;
    }
    
    stbi_write_bmp("hue.bmp", width, height, 3, hue_data);
    stbi_write_bmp("saturation.bmp", width, height, 3, sat_data);
    stbi_write_bmp("value.bmp", width, height, 3, val_data);
    
    free(hue_data);
    free(sat_data);
    free(val_data);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Pravilno koristenje: %s -filter\n", argv[0]);
        return 1;
    }
    
    char *arg = argv[1];
    char filter = '\0';
    if (arg[0] == '-' && strlen(arg) == 2) {
        filter = arg[1];
    } else {
        printf("Nepravilan format. Pravilno koristenje: -filter\n");
        return 1;
    }
    
    if (filter != 'g' && filter != 'h') {
        printf("Nepostojeci filter. Moguci filteri su -g, -h\n");
        return 1;
    }
    
    const char* input_file = "../input.bmp";
    
    int width, height, channels;
    unsigned char* data = stbi_load(input_file, &width, &height, &channels, 3);
    if (!data) {
        printf("Greska sa ucitavanjem slike: %s\n", input_file);
        return 1;
    }
    
    switch (filter) {
        case 'g':
        {
            clock_t start = clock();
            apply_grayscale(data, width, height);
            double duration = (double)(clock() - start) / CLOCKS_PER_SEC;
            printf("Vrijeme obrade grayscale sekvencijalno: %.4f s\n", duration);
            
        }
        break;
        
        case 'h':
        {
            clock_t start = clock();
            apply_hsv(data, width, height);
            double duration = (double)(clock() - start) / CLOCKS_PER_SEC;
            printf("Vrijeme obrade hsv sekvencijalno: %.4f sekundi\n", duration);
        }
        break;
    }
   
    stbi_image_free(data);
    return 0;
}