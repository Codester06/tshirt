# Kaggle Setup & Usage Guide

## Why Kaggle?
- **Stable GPU**: T4 GPU (15GB VRAM) is consistent
- **No random crashes**: Unlike Colab's frequent disconnects
- **Persistent storage**: Your notebooks and outputs stay available
- **Better performance**: ComfyUI runs more reliably

## Quick Setup (2 minutes)

### Cell 1: Clone Repository
```python
import subprocess
import os

# Clone the repo
subprocess.run(["git", "clone", "https://github.com/Codester06/tshirt.git"], check=True)
os.chdir("tshirt-automation")

print("✓ Repository cloned")
```

### Cell 2: Install Dependencies
```python
import subprocess
import sys

# Install required packages
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "requests", "pillow"], check=True)

print("✓ Dependencies installed")
```

### Cell 3: Download Model
```python
import subprocess
from pathlib import Path

# Create models directory
Path("ComfyUI/models/checkpoints").mkdir(parents=True, exist_ok=True)

# Download SD 1.5 model
print("📥 Downloading Stable Diffusion 1.5 model...")
print("   This is ~4GB and takes 2-3 minutes...")

model_path = "ComfyUI/models/checkpoints/v1-5-pruned-emaonly.safetensors"

if not Path(model_path).exists():
    subprocess.run([
        "wget",
        "-q",
        "--show-progress",
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors",
        "-O",
        model_path
    ], check=False)
    
    if Path(model_path).exists():
        print(f"✓ Model downloaded: {Path(model_path).stat().st_size / (1024**3):.2f} GB")
    else:
        print("✗ Download failed - try manual download or huggingface-hub")
else:
    print("✓ Model already exists")
```

### Cell 4: Update Prompts (Optional)
```python
# Edit your prompts here - one per line
prompts = """iron man suit, red and gold armor, glowing arc reactor, minimalist vector art, tshirt design, superhero, high detail
thor god of thunder, hammer mjolnir, lightning bolts, Norse mythology, golden armor, epic warrior, comic book style
spiderman hero, red blue costume, web slinger pose, action packed, urban background, spider symbol, dynamic illustration
programmer coder, laptop screen, code matrix, tech life, funny design, minimal style, digital art, tshirt print
groot forest guardian, tree creature, "I am Groot", leaves and branches, nature inspired, comic book art, green character"""

with open("prompts.txt", "w") as f:
    f.write(prompts)

print("✓ Prompts updated:")
for i, line in enumerate(prompts.strip().split("\n"), 1):
    print(f"  {i}. {line[:50]}...")
```

### Cell 5: Generate Designs
```python
import subprocess
import sys

# Run generation
print("🎨 Starting T-shirt design generation...\n")
subprocess.run([sys.executable, "colab_generate.py"], check=True)

# Show results
from pathlib import Path
output = Path("output")
pngs = list(output.glob("*.png"))

print(f"\n✓ Generated {len(pngs)} designs")
print(f"  Location: output/")
```

## Troubleshooting

### "No images found in ComfyUI output"
- **Check**: Is the model downloaded? (4GB required)
- **Fix**: Run Cell 3 again to download the model
- **Verify**: Check `ComfyUI/models/checkpoints/` folder

### "400 Bad Request error"
- **Cause**: Workflow using wrong model type
- **Fix**: Make sure you have latest code: `!git pull origin main`
- **Check**: Model is `v1-5-pruned-emaonly.safetensors` (NOT SDXL)

### ComfyUI crashes after 30 seconds
- **Normal**: Takes time to initialize
- **Wait**: Let it run for full duration (usually completes in 5-10 min for 5 prompts)
- **GPU Memory**: T4 GPU should handle this - check with `nvidia-smi`

### Out of Memory errors
- **Reduce**: Image size in workflow.json (currently 512x512)
- **Or**: Run fewer prompts at a time
- **Check**: `nvidia-smi` to see GPU usage

## Getting Results

After Cell 5 completes, your designs are in `output/`:
- `design_0001.png` - Iron Man
- `design_0002.png` - Thor
- `design_0003.png` - Spider-Man
- `design_0004.png` - Programmer
- `design_0005.png` - Groot

Plus a ZIP archive: `tshirt-designs-YYYYMMDD_HHMMSS.zip`

Download and use for your t-shirt designs!

## Pro Tips

1. **Batch processing**: Modify `prompts.txt` and run Cell 5 multiple times
2. **Custom prompts**: Edit Cell 4 to add your own prompt ideas
3. **Better quality**: Increase `steps` in workflow.json from 20 to 30-50 (slower but better)
4. **Download everything**: Kaggle lets you download the full output folder

## References
- Model source: [Hugging Face](https://huggingface.co/runwayml/stable-diffusion-v1-5)
- GitHub repo: [tshirt-automation](https://github.com/Codester06/tshirt)
- ComfyUI docs: [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
