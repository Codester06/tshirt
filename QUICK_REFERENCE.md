# Quick Reference Card

## 🚀 Get Started in 3 Steps

### Step 1: Setup (5 min)
```bash
cd tshirt-automation
bash quick-start.sh
source venv/bin/activate  # Activate virtual environment
```

### Step 2: Customize (5 min)
1. Export ComfyUI workflow as `workflow.json`
2. Edit `prompts.txt` with your designs
3. Adjust `config.json` if needed

### Step 3: Generate (varies)
```bash
python run.py                    # Generate all prompts
python batch_process.py --zip   # Create ZIP archive
```

---

## 🎨 Common Commands

### Generation
```bash
# Preview what would generate
python run.py --dry-run

# Generate designs (ComfyUI must be running)
python run.py

# Use custom server
python run.py --server http://192.168.1.100:8188

# Use custom prompts file
python run.py --prompts my_prompts.txt
```

### Post-Processing
```bash
# Process generated images
python batch_process.py

# Process and create ZIP
python batch_process.py --zip

# Use custom prompts for metadata
python batch_process.py --prompts my_prompts.txt
```

### GitHub
```bash
# Push to GitHub
git add .
git commit -m "Add designs"
git push

# Trigger workflow manually
# Go to: GitHub → Actions → "Generate T-Shirt Designs" → Run workflow
```

---

## 📁 File Quick Reference

| File | Edit? | Purpose |
|------|-------|---------|
| `workflow.json` | ✅ YES | Your ComfyUI workflow - **REQUIRED** |
| `prompts.txt` | ✅ YES | Your design prompts - **REQUIRED** |
| `config.json` | ⚠️ MAYBE | Fine-tune settings |
| `run.py` | ❌ NO | Generation script |
| `batch_process.py` | ❌ NO | Post-processing |
| `.github/workflows/build.yml` | ⚠️ MAYBE | GitHub automation |
| `README.md` | ❌ NO | Documentation |

---

## ⚙️ Configuration Cheat Sheet

### Generation Speed vs. Quality
```json
{
  "fast": {
    "steps": 15,      // Quick, lower quality
    "cfg": 7.0
  },
  "balanced": {
    "steps": 25,      // Default
    "cfg": 7.5
  },
  "high_quality": {
    "steps": 40,      // Slow, best quality
    "cfg": 8.0
  }
}
```

### Image Dimensions
```json
{
  "fast_preview": { "width": 512, "height": 512 },
  "standard": { "width": 1024, "height": 1024 },     // Default
  "print_ready": { "width": 2048, "height": 2048 },
  "etsy_ready": { "width": 4500, "height": 5400 }    // Upscaled
}
```

---

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "Cannot connect to ComfyUI" | Start ComfyUI: `cd ComfyUI && python main.py` |
| "Model not found" | Download to `ComfyUI/models/checkpoints/` |
| "Out of memory" | Reduce dimensions or steps in config |
| "Workflow JSON invalid" | Re-export from ComfyUI UI |
| "GitHub Actions timeout" | Use fewer prompts or cloud GPU |
| "No output generated" | Check ComfyUI logs and workflow connections |

---

## 📝 Prompt Writing Tips

### Good Prompts
```
minimalist vintage tiger, screen print style, vector art, 
black background, t-shirt design, high detail

retro motorcycle, 1970s aesthetic, worn texture, 
classic design, badges, road trip
```

### Avoid
```
❌ Too vague: "tiger"
❌ Too long: "a very detailed image of..."
❌ Contradictory: "photorealistic vector art"
✅ Right: "minimalist geometric tiger, vector style"
```

### Templates (fill in blanks)
```
[adjective] [subject], [style], [color], [mood], t-shirt design

Examples:
- minimalist tiger, line art, black, vintage, t-shirt design
- cosmic dragon, vector, neon, surreal, t-shirt design
- retro sunset, watercolor, warm, nostalgic, t-shirt design
```

---

## 🔗 Integration Checklist

- [ ] ComfyUI installed and running locally
- [ ] Python 3.8+ installed
- [ ] `pip install -r requirements.txt` completed
- [ ] Custom `workflow.json` exported from ComfyUI
- [ ] `prompts.txt` filled with your designs
- [ ] `python run.py --dry-run` works
- [ ] At least 1 design generated successfully
- [ ] GitHub repository created
- [ ] `.github/workflows/build.yml` configured
- [ ] GitHub Actions enabled in repository settings

---

## 📊 Performance Benchmarks

### Local Generation (with GPU)
- SDXL 25 steps: 2-3 min per design
- SD 1.5 25 steps: 30-60 sec per design
- With upscaling: +30-60 sec per design

### Cloud Generation (RunPod)
- SDXL 25 steps: 60-90 sec per design
- Batch 100 designs: 2-3 hours

### GitHub Actions (free tier)
- No GPU available, not recommended
- Best for orchestration and storage

---

## 💾 File Storage Requirements

| Item | Size |
|------|------|
| ComfyUI models | 5-20 GB |
| 100 generated images | 500 MB - 2 GB |
| ZIP archive | 200 MB - 1 GB |
| GitHub repository | <100 MB |

---

## 🔑 Essential Environment Variables

```bash
# Optional - set custom server
export COMFY_SERVER=http://127.0.0.1:8188

# For cloud deployment
export COMFY_SERVER=https://api.runpod.io/your-endpoint
```

---

## 📦 Deployment Paths

### Path 1: Local Only
ComfyUI (PC) → Generate → Download → Upload to platform

### Path 2: GitHub + Local
ComfyUI (PC) → GitHub (push) → Manual trigger → Download

### Path 3: Cloud GPU
RunPod/Lambda → GitHub Actions → Auto-generate → Download

### Path 4: Full Automation
ComfyUI (RunPod) → Scheduled GitHub Actions → Auto-upload to Etsy/Redbubble

---

## 🆘 Quick Help

```bash
# View script help
python run.py --help
python batch_process.py --help

# Check Python version
python3 --version

# Check if requests installed
python -c "import requests; print(requests.__version__)"

# View generated files
ls -lh output/
```

---

## 📖 Where to Find Things

| Topic | File |
|-------|------|
| Complete setup | `SETUP.md` |
| Advanced options | `ADVANCED.md` |
| Project layout | `PROJECT_STRUCTURE.md` |
| Implementation details | `IMPLEMENTATION_SUMMARY.md` |
| Overview | `README.md` |

---

## 🎯 Success Checklist

Before uploading to print-on-demand:
- [ ] All 100+ images generated
- [ ] All images are PNG with transparent background
- [ ] Images are at least 4500x5400px
- [ ] Metadata created for each design
- [ ] Archive created successfully
- [ ] Local testing complete
- [ ] No watermarks or artifacts
- [ ] Quality meets your standards

---

## ⏱️ Typical Timeline

| Stage | Time |
|-------|------|
| Setup | 5-10 min |
| ComfyUI setup | 30-60 min |
| Generate 10 designs | 20-30 min |
| Generate 100 designs | 3-6 hours |
| Post-processing | 5-10 min |
| Upload to platforms | 1-2 hours |
| **Total (100 designs)** | **4-8 hours** |

---

**Pro Tip:** Start with 10-20 designs to test, then scale to 100+

**Next Step:** Read SETUP.md for detailed instructions
