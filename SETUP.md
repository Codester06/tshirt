# Complete Setup Guide

## Prerequisites

- Git
- Python 3.8+
- ComfyUI installed locally (for testing)
- GitHub account (for automation)

## Step 1: Local Setup for Testing

### 1.1 Install ComfyUI

```bash
# Clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Install dependencies
pip install -r requirements.txt

# Download models (SDXL)
# Visit https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
# Place in: ComfyUI/models/checkpoints/
```

### 1.2 Clone this Repository

```bash
git clone https://github.com/yourusername/tshirt-automation.git
cd tshirt-automation
```

### 1.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 1.4 Create Your Workflow

1. **Start ComfyUI:**
   ```bash
   cd ../ComfyUI
   python main.py
   ```
   Open http://localhost:8188 in your browser

2. **Build your workflow:**
   - Add "Load Checkpoint" node → select SDXL model
   - Add "CLIP Text Encode (Positive)" → connect to checkpoint
   - Add "CLIP Text Encode (Negative)" → connect to checkpoint
   - Add "KSampler" → connect encoders and checkpoint
   - Add "Empty Latent Image" → connect to sampler
   - Add "VAE Decode" → connect sampler output
   - Add "Save Image" → connect VAE output
   - Add "Preview Image" → optional

3. **Test with a sample prompt:**
   - Update the positive prompt to: "minimalist vintage tiger, screen print style"
   - Click "Queue Prompt"
   - Wait for generation

4. **Export workflow:**
   - Use right-click menu or use button: "Save (API Format)"
   - Replace `workflow.json` in this repo with your exported file

## Step 2: Run Locally

```bash
# Test with dry-run
python run.py --dry-run

# Generate designs (ComfyUI must be running)
python run.py

# Process and create archive
python batch_process.py --zip
```

## Step 3: GitHub Setup

### 3.1 Create Repository

1. Create new repository on GitHub: `tshirt-automation`
2. Initialize locally:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: T-shirt automation workflow"
   git branch -M main
   git remote add origin https://github.com/yourusername/tshirt-automation.git
   git push -u origin main
   ```

### 3.2 Enable GitHub Actions

1. Go to repository → Settings → Actions
2. Enable "Allow all actions"

### 3.3 Configure Workflow

The `.github/workflows/build.yml` is pre-configured to:
- Use Comfy-Action to run ComfyUI
- Generate designs
- Upload artifacts as ZIP
- Create releases automatically

### 3.4 Customize Prompts

Edit `prompts.txt` with your design ideas:
```
your custom design prompt 1
your custom design prompt 2
your custom design prompt 3
```

## Step 4: Run on GitHub Actions

1. Go to repository → Actions
2. Select "Generate T-Shirt Designs" workflow
3. Click "Run workflow" → Choose branch (main)
4. Monitor execution
5. Download artifacts when complete

## Customization Guide

### Modify Workflow Nodes

Edit `workflow.json`:
- Change checkpoint model
- Adjust sampling steps (higher = better quality, slower)
- Change CFG scale (7.5 is balanced)
- Modify image dimensions

Example:
```json
{
  "4": {
    "inputs": {
      "steps": 40,        // Increase for better quality
      "cfg": 8.5,        // Increase for more prompt adherence
      ...
    }
  }
}
```

### Add Custom Nodes for Post-Processing

Popular ComfyUI custom nodes:
- **Background Removal:** `rembg-python` node
- **Upscaling:** ESRGAN or Real-ESRGAN
- **Color Correction:** Various filter nodes
- **Text Overlay:** For branding

### Adjust run.py for Your Workflow

The `run.py` script injects prompts into the workflow. Update the node numbers if needed:

```python
# Find the correct node IDs in your workflow.json
# Update the inject_prompt() function to match your structure
if node_id in ["2", "3"]:  # Your text encode node IDs
    inputs["text"] = positive_prompt
```

## Troubleshooting

### Issue: "Cannot connect to ComfyUI"
- Ensure ComfyUI is running: `python main.py`
- Check server is accessible: http://localhost:8188
- Verify `run.py` has correct COMFY_SERVER URL

### Issue: "Model not found"
- Download model file and place in `ComfyUI/models/checkpoints/`
- Update model name in `workflow.json` and checkpoint loader

### Issue: "Out of memory"
- Reduce image dimensions (1024×1024 instead of 2048×2048)
- Reduce batch size
- Use a smaller model (SD 1.5 instead of SDXL)

### Issue: GitHub Actions timeout
- Reduce number of prompts
- Use GitHub runners with GPU (paid)
- Run generation locally, use GitHub only for storage

## Performance Optimization

### For Local Generation
```bash
# Generate in parallel (adjust worker count)
python run.py  # Single process (safest)
```

### For GitHub Actions
- Free runners: ~5-15 min per design (without GPU)
- Consider using local PC + GitHub storage
- Alternative: Use cloud GPU services (RunPod, Lambda Labs)

## Deployment to Print-on-Demand

### Etsy
1. Convert designs to PNG with transparent background
2. Upload to Etsy shop
3. Set up print-on-demand integration

### Redbubble
1. Upload PNG files
2. Add mockups and descriptions
3. Set pricing and margins

### Merch by Amazon
1. Apply for Merch by Amazon program
2. Upload designs (max 100 per day)
3. Assign to products
4. Amazon handles production

## Resources

- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [Comfy-Action](https://github.com/comfy-org/comfy-action)
- [SDXL Models](https://huggingface.co/stabilityai)
- [Custom Nodes](https://github.com/comfyanonymous/ComfyUI/wiki/Custom-Nodes)

## License

This project is provided as-is for educational and personal use.
