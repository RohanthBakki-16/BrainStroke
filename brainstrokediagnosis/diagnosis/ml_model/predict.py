import numpy as np
from PIL import Image
import random
import os


def preprocess_image(image_path, target_size=(256, 256)):
    """Preprocess image for model input: resize and normalize."""
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize(target_size)
        img_array = np.array(img)
        img_normalized = img_array / 255.0
        return img_normalized
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {str(e)}")


def generate_mock_segmentation(original_image_path):
    """Generate a mock segmented image (placeholder for actual U-Net output)."""
    try:
        img = Image.open(original_image_path).convert('RGB')
        img = img.resize((256, 256))
        img_array = np.array(img)
        
        height, width = img_array.shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)
        
        center_y, center_x = height // 2, width // 2
        radius = random.randint(30, 80)
        y, x = np.ogrid[:height, :width]
        mask_circle = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
        mask[mask_circle] = 255
        
        segmented = img_array.copy()
        segmented[mask == 0] = np.clip(segmented[mask == 0] * 0.3, 0, 255).astype(np.uint8)
        
        highlight = np.random.randint(200, 255, size=(height, width, 3), dtype=np.uint8)
        segmented[mask == 255] = ((segmented[mask == 255] * 0.5 + highlight[mask == 255] * 0.5)).astype(np.uint8)
        
        return segmented
    except Exception as e:
        raise ValueError(f"Error generating segmentation: {str(e)}")


def predict_stroke(image_path, scan_type='MRI'):
    """
    Mock prediction function simulating U-Net model output.
    Returns realistic predictions for demonstration.
    
    Args:
        image_path: Path to the input MRI/CT image
        scan_type: Type of scan (MRI or CT)
    
    Returns:
        dict: Prediction results containing:
            - stroke_detected: Boolean indicating if stroke was detected
            - stroke_type: Type of stroke (Ischemic/Hemorrhagic/None)
            - confidence_score: Confidence score (0-100)
            - segmented_image: Processed segmentation mask
    """
    try:
        preprocessed = preprocess_image(image_path)
        
        scan_hash = hash(image_path) % 100
        if scan_hash < 35:
            stroke_detected = True
            stroke_type = 'Ischemic' if random.random() < 0.6 else 'Hemorrhagic'
            confidence = random.uniform(75.0, 95.0)
        elif scan_hash < 45:
            stroke_detected = True
            stroke_type = 'Hemorrhagic'
            confidence = random.uniform(70.0, 90.0)
        else:
            stroke_detected = False
            stroke_type = 'None'
            confidence = random.uniform(55.0, 85.0)
        
        segmented_array = generate_mock_segmentation(image_path)
        
        return {
            'stroke_detected': stroke_detected,
            'stroke_type': stroke_type,
            'confidence_score': round(confidence, 2),
            'segmented_image': segmented_array
        }
    except Exception as e:
        return {
            'stroke_detected': False,
            'stroke_type': 'Error',
            'confidence_score': 0.0,
            'segmented_image': None,
            'error': str(e)
        }


def load_model():
    """Placeholder for loading actual trained model."""
    print("Loading mock U-Net model...")
    return None


def predict_batch(image_paths, scan_type='MRI'):
    """Process multiple images."""
    results = []
    for path in image_paths:
        result = predict_stroke(path, scan_type)
        results.append(result)
    return results