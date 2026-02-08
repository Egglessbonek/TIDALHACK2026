from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import io
from PIL import Image
from classifier import SketchClassifier
import os

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize classifier
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
classifier = SketchClassifier(asset_dir=ASSET_DIR)

# Mount assets directory to serve matched images
if not os.path.exists(ASSET_DIR):
    os.makedirs(ASSET_DIR)
app.mount("/assets", StaticFiles(directory=ASSET_DIR), name="assets")

@app.get("/")
def read_root():
    return {"message": "Sketch Classification API is running. Upload a sketch to /predict to find the closest asset."}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Receives an image file (sketch), converts it, and finds the closest matching asset.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Predict
        match, score = classifier.predict(image, threshold=0.4) # Slightly lower threshold for sketches
        
        return {
            "match": match,
            "score": score,
            "match_url": f"/assets/{match}" if match else None
        }
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reload-assets")
def reload_assets():
    """
    Reloads the assets from the assets directory. Call this after adding new images.
    """
    classifier.load_assets()
    return {"message": f"Assets reloaded. Total assets: {len(classifier.asset_embeddings)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
