import cv2
import numpy as np
from PIL import Image

def analyze_skin_tone(image: Image.Image):
    """
    Analyzes an uploaded image (Hand or Full body) to extract skin color & undertone.
    """
    img_np = np.array(image)
    if len(img_np.shape) == 2:
        img_rgb = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
    elif img_np.shape[2] == 4:
        img_rgb = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
    else:
        img_rgb = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
    
    img_resized = cv2.resize(img_rgb, (100, 100))
    mean_r, mean_g, mean_b = img_resized[:, :, 0].mean(), img_resized[:, :, 1].mean(), img_resized[:, :, 2].mean()
    
    brightness = (0.299 * mean_r + 0.587 * mean_g + 0.114 * mean_b)
    
    if brightness > 170:
        tone = "Fair / Light"
        suggested_palette = "Pastels, Soft Pinks, Muted Blues, Emerald Green, Deep Reds"
    elif brightness > 120:
        tone = "Medium / Wheatish (Medium Warm)"
        suggested_palette = "Warm Yellows, Olive Green, Teal, Rust, Mustard, Earthy Browns"
    else:
        tone = "Deep / Tan"
        suggested_palette = "Bright Jewel Tones, Magenta, Royal Blue, Pure White, Crimson"

    undertone = "Warm (Yellow/Golden)" if mean_r > mean_b else "Cool (Pink/Blueish)"

    return {
        "skin_tone": tone,
        "undertone": undertone,
        "best_colors": suggested_palette,
        "avg_rgb": (int(mean_r), int(mean_g), int(mean_b))
    }