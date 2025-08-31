import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;

public class sequential {
    
    private static class ImageData {
        BufferedImage image;
        int width;
        int height;
        
        ImageData(BufferedImage image) {
            this.image = image;
            this.width = image.getWidth();
            this.height = image.getHeight();
        }
    }
    
    public static ImageData loadImage(String filepath) {
        try {
            File file = new File(filepath);
            BufferedImage image = ImageIO.read(file);
            return new ImageData(image);
        } catch (Exception e) {
            System.err.println("Greška sa učitavanjem slike: " + e.getMessage());
            return null;
        }
    }
    
    public static void applyGrayscale(ImageData imageData) {
        BufferedImage originalImage = imageData.image;
        int width = imageData.width;
        int height = imageData.height;
        
        BufferedImage result = new BufferedImage(width, height, BufferedImage.TYPE_BYTE_GRAY);
        
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int rgb = originalImage.getRGB(x, y);
                
                int r = (rgb >> 16) & 0xFF;
                int g = (rgb >> 8) & 0xFF;
                int b = rgb & 0xFF;
                
                int gray = (int) (0.299 * r + 0.587 * g + 0.114 * b);
                
                int grayRgb = (gray << 16) | (gray << 8) | gray;
                result.setRGB(x, y, grayRgb);
            }
        }
        
        saveImage(result, "grayscale.bmp");
    }
    
    public static void applyHsv(ImageData imageData) {
        BufferedImage originalImage = imageData.image;
        int width = imageData.width;
        int height = imageData.height;
        
        BufferedImage hueImg = new BufferedImage(width, height, BufferedImage.TYPE_BYTE_GRAY);
        BufferedImage satImg = new BufferedImage(width, height, BufferedImage.TYPE_BYTE_GRAY);
        BufferedImage valImg = new BufferedImage(width, height, BufferedImage.TYPE_BYTE_GRAY);
        
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int rgb = originalImage.getRGB(x, y);
                
                int r = (rgb >> 16) & 0xFF;
                int g = (rgb >> 8) & 0xFF;
                int b = rgb & 0xFF;
                
                double rNorm = r / 255.0;
                double gNorm = g / 255.0;
                double bNorm = b / 255.0;
                
                double cmax = Math.max(Math.max(rNorm, gNorm), bNorm);
                double cmin = Math.min(Math.min(rNorm, gNorm), bNorm);
                double delta = cmax - cmin;
                
                // Value
                int v = (int) (cmax * 255);
                
                // Saturation
                int s = (int) (cmax != 0 ? (delta / cmax * 255) : 0);
                
                // Hue
                double h;
                if (delta == 0) {
                    h = 0;
                } else {
                    if (cmax == rNorm) {
                        h = 60 * (((gNorm - bNorm) / delta) % 6);
                    } else if (cmax == gNorm) {
                        h = 60 * (((bNorm - rNorm) / delta) + 2);
                    } else {
                        h = 60 * (((rNorm - gNorm) / delta) + 4);
                    }
                    if (h < 0) {
                        h += 360;
                    }
                }
                int hValue = (int) ((h / 360) * 255);
                
                // Set pixels
                int hueRgb = (hValue << 16) | (hValue << 8) | hValue;
                int satRgb = (s << 16) | (s << 8) | s;
                int valRgb = (v << 16) | (v << 8) | v;
                
                hueImg.setRGB(x, y, hueRgb);
                satImg.setRGB(x, y, satRgb);
                valImg.setRGB(x, y, valRgb);
            }
        }
        
        saveImage(hueImg, "hue.bmp");
        saveImage(satImg, "saturation.bmp");
        saveImage(valImg, "value.bmp");
    }
    
    private static void saveImage(BufferedImage image, String outputPath) {
        try {
            String format = "bmp";
            ImageIO.write(image, format, new File(outputPath));
        } catch (IOException e) {
            System.err.println("Greška pri spremanju slike: " + e.getMessage());
        }
    }
    
    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Filter: g za grayscale, hsv za HSV");
            System.exit(1);
        }
        
        String filter = args[0];
        
        if (!filter.equals("g") && !filter.equals("hsv")) {
            System.err.println("Pogresan argument");
            System.exit(1);
        }
        
        ImageData imageData = loadImage("../input.bmp");
        if (imageData == null) {
            System.exit(1);
        }
        
        long startTime = System.nanoTime();
        
        if (filter.equals("g")) {
            applyGrayscale(imageData);
        } else if (filter.equals("hsv")) {
            applyHsv(imageData);
        }
        
        long endTime = System.nanoTime();
        double duration = (endTime - startTime) / 1_000_000_000.0;
        System.out.printf("Vrijeme izvođenja: %.4f s%n", duration);
    }
}