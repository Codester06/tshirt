# Project Structure

```
tshirt-automation/
├── README.md                          # Project overview
├── SETUP.md                          # Step-by-step setup guide
├── ADVANCED.md                       # Advanced customization
├── PROJECT_STRUCTURE.md              # This file
│
├── requirements.txt                  # Python dependencies
├── config.json                       # Configuration settings
├── quick-start.sh                    # Quick setup script
│
├── workflow.json                     # ComfyUI workflow (customize this)
├── prompts.txt                       # Design prompts (edit to customize)
│
├── run.py                            # Main generation script
├── batch_process.py                  # Post-processing script
│
├── .github/
│   └── workflows/
│       └── build.yml                 # GitHub Actions workflow
│
├── .gitignore                        # Git ignore rules
│
├── output/                           # Generated designs
│   ├── processed/                    # Post-processed images
│   └── metadata/                     # Design metadata
│
├── input/                            # Input files (if needed)
│
└── docs/                             # Additional documentation (optional)
    ├── prompts_templates.json        # Prompt templates
    ├── workflows/                    # Alternative workflows
    └── examples/                     # Example designs
```

## File Descriptions

### Core Files

| File | Purpose |
|------|---------|
| `workflow.json` | ComfyUI workflow - CUSTOMIZE THIS with your own setup |
| `prompts.txt` | Design prompts, one per line - EDIT to add your designs |
| `run.py` | Python script to generate designs from prompts |
| `batch_process.py` | Post-processing: cleanup, archive, metadata |
| `config.json` | Global configuration for generation settings |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Quick overview and usage |
| `SETUP.md` | Detailed setup instructions (local + GitHub) |
| `ADVANCED.md` | Advanced customization and integration |
| `PROJECT_STRUCTURE.md` | This file |

### GitHub Actions

| File | Purpose |
|------|---------|
| `.github/workflows/build.yml` | GitHub Actions workflow for automation |

### Supporting Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies (requests, Pillow) |
| `quick-start.sh` | Automated setup script |
| `.gitignore` | Git ignore patterns |

### Directories

| Directory | Purpose |
|-----------|---------|
| `output/` | Generated designs and metadata |
| `output/processed/` | Post-processed designs |
| `output/metadata/` | Design metadata JSON files |
| `input/` | Input files (for future use) |

## Usage Workflow

### Local Development
```
1. Run quick-start.sh          # Initial setup
2. Customize workflow.json     # Export from ComfyUI
3. Edit prompts.txt            # Your design ideas
4. python run.py --dry-run    # Preview
5. python run.py              # Generate
6. python batch_process.py    # Post-process
```

### GitHub Automation
```
1. Push to GitHub
2. Trigger workflow manually or on schedule
3. Download artifacts
4. Upload to print-on-demand platforms
```

## Customization Points

### Essential Customization
1. **workflow.json** - Replace with your ComfyUI workflow
2. **prompts.txt** - Replace with your design prompts
3. **config.json** - Adjust generation parameters

### Optional Customization
1. **.github/workflows/build.yml** - Adjust GitHub Actions settings
2. **run.py** - Modify prompt injection logic
3. **batch_process.py** - Add custom post-processing

## Key Scripts

### run.py
```bash
# Test without generating
python run.py --dry-run

# Generate designs (ComfyUI must be running)
python run.py

# Use custom server
python run.py --server http://your-server:8188

# Use custom prompts file
python run.py --prompts custom_prompts.txt
```

### batch_process.py
```bash
# Process generated images
python batch_process.py

# Process and create ZIP archive
python batch_process.py --zip

# Use custom prompts for metadata
python batch_process.py --prompts custom_prompts.txt
```

### quick-start.sh
```bash
# Run setup
bash quick-start.sh
```

## Configuration Options

### config.json Settings

**generation**: Image generation parameters
- width/height: Image dimensions
- steps: Sampling steps (higher = better, slower)
- cfg_scale: Guidance scale (higher = more prompt adherence)
- sampler: Sampling algorithm

**upscaling**: Upscale settings
- enabled: Whether to upscale images
- scale_factor: Upscale multiplier (4x = 4 times larger)
- target dimensions: Final image size

**output**: Output settings
- directory: Where to save images
- format: Image format (png, jpg)
- quality: Output quality

**batch_processing**: Post-processing
- create_metadata: Generate JSON metadata
- create_archive: Package as ZIP

## Integration Points

### External Services
- ComfyUI API (localhost:8188)
- GitHub API (for releases)
- Print-on-demand platforms (Etsy, Redbubble, etc.)

### Cloud Services
- GitHub Actions (orchestration)
- RunPod (GPU acceleration)
- Lambda Labs (GPU instances)
- Cloud storage (S3, GCS)

## Troubleshooting Files

- Check `output/` for generation errors
- Check `output/metadata/summary.json` for batch results
- Review `.github/workflows/build.yml` logs in GitHub Actions
- Check `run.py` logs for API connection issues

## Next Steps

1. **Local Testing**: Follow SETUP.md step 1-2
2. **GitHub Setup**: Follow SETUP.md step 3
3. **Advanced Features**: Check ADVANCED.md
4. **Production Deployment**: Use RunPod or Lambda Labs

## Support Resources

- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **Models**: https://huggingface.co/stabilityai
- **Custom Nodes**: https://github.com/comfyanonymous/ComfyUI/wiki/Custom-Nodes
- **GitHub Actions**: https://docs.github.com/en/actions
