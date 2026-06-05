# T-Shirt Design Automation with ComfyUI

Automatically generate hundreds of T-shirt designs using ComfyUI and GitHub Actions. This workflow takes design prompts, generates artwork, removes backgrounds, upscales images, and packages them for print-on-demand platforms.

## Workflow Overview

```
prompts.txt → GitHub Action → ComfyUI Workflow → Generate Artwork → 
Remove Background → Upscale → Transparent PNG → Download ZIP
```

## Setup Instructions

### 1. Local Setup (for testing)

```bash
# Clone this repo
git clone https://github.com/yourusername/tshirt-automation.git
cd tshirt-automation

# Install dependencies
pip install -r requirements.txt

# Place your ComfyUI installation path in run.py
# Run locally with your GPU
python run.py
```

### 2. GitHub Setup

1. Fork or create this repository
2. Enable GitHub Actions in repository settings
3. Add your ComfyUI workflow (export from ComfyUI UI as `workflow.json`)
4. Edit `prompts.txt` with your design ideas
5. Trigger workflow manually or via schedule

### 3. Customize

- **workflow.json**: Export from ComfyUI after creating your node-based workflow
- **prompts.txt**: One design prompt per line
- **run.py**: Adjust API endpoint, model settings, output paths
- **.github/workflows/build.yml**: Configure GitHub Actions runner and artifact settings

## Output

- Generated images in `output/` directory
- Background-removed transparent PNGs
- Upscaled to 4500x5400px (print-ready)
- Automatically packaged as ZIP for download

## Recommended Workflow Nodes

- Checkpoint Loader (SDXL or Flux)
- CLIP Text Encode (Positive & Negative)
- KSampler
- VAE Decode
- Image Upscale (ESRGAN 4x)
- Remove Background (custom node)
- Save Image PNG

## Platforms Supported

- Etsy
- Redbubble
- Merch by Amazon
- Print-on-demand resellers

## Notes

- GitHub runners have limited GPU resources; recommend running generation locally
- For batch processing 100+ designs, use a local PC or cloud GPU
- GitHub Actions is best for orchestration and artifact management
