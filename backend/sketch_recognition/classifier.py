import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os
import numpy as np

class SketchClassifier:
    def __init__(self, asset_dir="assets"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        # Use ResNet18 for feature extraction
        self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        # Remove the final classification layer (fc) to get the feature embeddings
        self.model.fc = nn.Identity()
        self.model = self.model.to(self.device)
        self.model.eval()

        # Standard ImageNet normalization
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        self.asset_dir = asset_dir
        self.asset_embeddings = {}
        self.load_assets()

    def load_assets(self):
        """Loads all images from the assets directory and precomputes their embeddings."""
        print(f"Loading assets from {self.asset_dir}...")
        self.asset_embeddings = {}
        if not os.path.exists(self.asset_dir):
            os.makedirs(self.asset_dir)
            print("Asset directory created.")
            return

        count = 0
        for filename in os.listdir(self.asset_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                path = os.path.join(self.asset_dir, filename)
                try:
                    img = Image.open(path)
                    img = self._ensure_rgb(img)
                    emb = self._get_embedding(img)
                    self.asset_embeddings[filename] = emb
                    count += 1
                except Exception as e:
                    print(f"Error loading asset {filename}: {e}")
        print(f"Loaded {count} assets.")

    def _ensure_rgb(self, image):
        """Converts image to RGB. Handles RGBA by compositing over white."""
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            return background
        elif image.mode != 'RGB':
            return image.convert('RGB')
        return image

    def _get_embedding(self, image):
        """Generates embedding vector for a single PIL image."""
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.model(input_tensor)
        return embedding.cpu().squeeze().numpy()

    def predict(self, sketch_image, threshold=0.5):
        """
        Finds the closest asset to the given sketch image.
        Returns (best_match_filename, similarity_score).
        Returns (None, best_score) if no match above threshold.
        """
        if not self.asset_embeddings:
            return None, 0.0

        sketch_image = self._ensure_rgb(sketch_image)
        sketch_emb = self._get_embedding(sketch_image)
        
        best_match = None
        highest_score = -1.0
        
        sketch_norm = np.linalg.norm(sketch_emb)
        
        for name, asset_emb in self.asset_embeddings.items():
            # Cosine similarity
            asset_norm = np.linalg.norm(asset_emb)
            if sketch_norm == 0 or asset_norm == 0:
                similarity = 0
            else:
                similarity = np.dot(sketch_emb, asset_emb) / (sketch_norm * asset_norm)
            
            if similarity > highest_score:
                highest_score = similarity
                best_match = name
        
        # Convert numpy float to python float
        highest_score = float(highest_score)

        if highest_score < threshold:
            return None, highest_score
            
        return best_match, highest_score
