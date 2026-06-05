# 🎨 T-Shirt Design Automation - START HERE

Welcome! You have a complete, production-ready system for generating hundreds of T-shirt designs automatically using ComfyUI and GitHub.

## What You Have

✅ **Complete GitHub repository** ready to use  
✅ **Python generation pipeline** for bulk design creation  
✅ **GitHub Actions automation** for scheduling  
✅ **Post-processing tools** for archive generation  
✅ **Comprehensive documentation** for setup and customization  

## First Time? Follow This

### 1️⃣ Read (2 min)
Start here: **QUICK_REFERENCE.md**  
→ Fast overview of all commands and options

### 2️⃣ Setup (5 min)
Run this: **quick-start.sh**
```bash
bash quick-start.sh
```

### 3️⃣ Learn (10 min)
Read: **SETUP.md**  
→ Step-by-step local + GitHub setup

### 4️⃣ Customize (10 min)
1. Export your ComfyUI workflow → **workflow.json**
2. Edit your prompts → **prompts.txt**
3. Done!

### 5️⃣ Generate (varies)
```bash
python run.py              # Generate designs
python batch_process.py --zip   # Create archive
```

## 📚 Documentation Map

```
START HERE
    ↓
QUICK_REFERENCE.md (2 min) ← Quick cheat sheet
    ↓
SETUP.md (detailed) ← Full step-by-step
    ↓
ADVANCED.md ← Advanced customization
    ↓
PROJECT_STRUCTURE.md ← How everything connects
```

## 🎯 What Each File Does

### 🔧 Files You Need to Customize

| File | What to Do | Why |
|------|-----------|-----|
| **workflow.json** | Export from ComfyUI | This is your actual design workflow |
| **prompts.txt** | Add your design ideas | These become your designs |
| **config.json** | (Optional) Tweak settings | Fine-tune quality/speed |

### 🐍 Files That Do the Work

| File | Purpose |
|------|---------|
| **run.py** | Reads prompts → generates designs |
| **batch_process.py** | Organizes outputs → creates archives |
| **build.yml** | GitHub automation (schedule runs) |

### 📖 Files That Explain

| File | Read This For |
|------|---|
| **README.md** | Project overview |
| **QUICK_REFERENCE.md** | Fast command reference |
| **SETUP.md** | Detailed setup steps |
| **ADVANCED.md** | Custom nodes, cloud GPU, etc. |

---

## ⚡ Quick Start Timeline

### First Session: 30 minutes
```
5 min  → bash quick-start.sh
10 min → Read SETUP.md (local setup section)
10 min → Export ComfyUI workflow + edit prompts.txt
5 min  → python run.py --dry-run
```

### Second Session: 1-3 hours (actual generation)
```
Setup ComfyUI locally
Run: python run.py
Watch designs generate
Run: python batch_process.py --zip
Download your archive
```

### Third Session: GitHub setup (15 min)
```
Push to GitHub
Enable Actions
Edit build.yml if needed
Click "Run workflow"
```

---

## 🚀 Three Ways to Generate

### Option 1: Local (Fastest for testing)
```bash
python run.py --dry-run    # See what would generate
python run.py              # Actually generate (ComfyUI must be running)
```
**Best for:** Testing, small batches, high quality  
**Time:** 2-3 min per design with SDXL

### Option 2: GitHub Actions (Automated)
1. Push to GitHub
2. Go to Actions → Run workflow
3. Download artifacts when done

**Best for:** Scheduled bulk generation  
**Time:** Varies (free tier has no GPU)

### Option 3: Cloud GPU (Fastest)
1. Use RunPod or Lambda Labs
2. Update COMFY_SERVER URL in run.py
3. Generate in parallel

**Best for:** 100+ designs, production  
**Cost:** $0.20-2.00 per hour

---

## 📝 Customize These 2 Files

### 1. prompts.txt
```txt
minimalist vintage tiger, screen print style, vector art, black background, tshirt design, high detail
retro motorcycle tshirt, classic badge design, worn vintage look, 1970s aesthetic
samurai skull tshirt, japanese style, minimalist line art, monochrome
[add more lines for each design]
```

### 2. workflow.json
Export from ComfyUI:
1. Build your workflow in http://localhost:8188
2. Right-click empty area
3. "Save (API Format)"
4. Replace workflow.json with this file

---

## ✅ Quick Checklist

Before you start:
- [ ] Python 3.8+ installed? (`python3 --version`)
- [ ] Git installed? (`git --version`)
- [ ] Read QUICK_REFERENCE.md? (2 min)
- [ ] Run quick-start.sh? (5 min)
- [ ] Have ComfyUI ideas? (the workflow)
- [ ] Have design prompts ready? (20-100 ideas)

---

## 🎓 Learning Path

1. **Beginner**: Just generate designs
   - Run quick-start.sh
   - Use provided workflow.json
   - Edit prompts.txt
   - python run.py

2. **Intermediate**: Customize everything
   - Read SETUP.md
   - Export custom ComfyUI workflow
   - Fine-tune config.json
   - Generate and batch process

3. **Advanced**: Deploy to cloud
   - Read ADVANCED.md
   - Set up RunPod or Lambda Labs
   - Automate with GitHub Actions
   - Integrate with print-on-demand

---

## 🔍 Find What You Need

### I want to...

**...get started immediately**
→ Run: `bash quick-start.sh`

**...understand what's included**
→ Read: `QUICK_REFERENCE.md`

**...set up ComfyUI**
→ Read: `SETUP.md` (Step 1)

**...fix a problem**
→ See: `QUICK_REFERENCE.md` → Troubleshooting

**...use cloud GPU**
→ Read: `ADVANCED.md` → Cloud Deployment

**...upload to Etsy/Redbubble**
→ Read: `SETUP.md` → Step 9

**...add background removal**
→ Read: `ADVANCED.md` → Custom Nodes

**...generate 1000+ designs**
→ Read: `ADVANCED.md` → Performance Optimization

---

## 💡 Pro Tips

1. **Start Small**: Test with 5-10 prompts before 100+
2. **Quality First**: Get one perfect design, then duplicate the workflow
3. **Batch Often**: Generate designs periodically, not all at once
4. **Archive Everything**: Always create ZIP archives for backups
5. **Test Locally**: Validate workflow locally before GitHub
6. **Version Control**: Commit your prompts and config to Git

---

## 📞 Need Help?

| Topic | File |
|-------|------|
| Commands and syntax | QUICK_REFERENCE.md |
| Step-by-step setup | SETUP.md |
| Troubleshooting | QUICK_REFERENCE.md → Troubleshooting |
| Advanced features | ADVANCED.md |
| Project structure | PROJECT_STRUCTURE.md |
| All details | IMPLEMENTATION_SUMMARY.md |

---

## 🎬 Next Action

Pick one:

### ✅ I have ComfyUI running
```bash
bash quick-start.sh
python run.py --dry-run
```

### ✅ I don't have ComfyUI
```bash
read SETUP.md  # Follow Step 1
```

### ✅ I'm ready to customize
```bash
Edit workflow.json (export from ComfyUI)
Edit prompts.txt (your design ideas)
python run.py
```

---

## 🎉 What's Possible

- **10 designs**: 15 minutes (test)
- **100 designs**: 3-6 hours (bulk batch)
- **1000 designs**: 1-2 days (production)
- **Weekly automation**: GitHub Actions (scheduled)
- **Instant API**: Cloud deployment (RunPod)

---

## 📦 What You're Getting

```
Production-ready system for:
✅ Generate 100+ T-shirt designs
✅ Automate with GitHub Actions
✅ Upload to Etsy/Redbubble/Amazon
✅ Scale to cloud GPU
✅ Monitor with analytics
✅ Version control everything
```

---

## 🏃 Ready? Let's Go!

```bash
# 1. One command to setup
bash quick-start.sh

# 2. Follow the prompts (5 min)

# 3. You're ready to generate!
python run.py --dry-run
```

**Estimated time to first generated design: 15 minutes**

---

**Questions?** Check the relevant file from the Documentation Map above.

**Ready to start?** → Run `bash quick-start.sh`
