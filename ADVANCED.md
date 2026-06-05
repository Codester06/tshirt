# Advanced Customization Guide

## Custom ComfyUI Nodes

### Add Background Removal

1. **Install the custom node:**
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/AIGODLIKE/AIGODLIKE-ComfyUI-Translation.git
   # Or use a specific rembg node package
   ```

2. **Update workflow.json:**
   ```json
   {
     "11": {
       "inputs": {
         "model": "u2net",
         "images": ["6", 0]
       },
       "class_type": "RemoveBackground",
       "_meta": {
         "title": "Remove Background"
       }
     }
   }
   ```

3. **Connect to previous node and update save image:**
   ```json
   {
     "9": {
       "inputs": {
         "images": ["11", 0]  // Changed from "6" to "11"
       }
     }
   }
   ```

### Add Color Correction

```json
{
  "12": {
    "inputs": {
      "brightness": 1.0,
      "contrast": 1.1,
      "saturation": 1.2,
      "images": ["6", 0]
    },
    "class_type": "ColorCorrect",
    "_meta": {
      "title": "Color Correction"
    }
  }
}
```

## Prompt Engineering

### Template System

Create `prompts_templates.json`:
```json
{
  "templates": {
    "vintage": "vintage {subject}, retro {style}, {decade} aesthetic, worn texture, classic design",
    "modern": "modern {subject}, minimalist {style}, clean lines, contemporary design",
    "artistic": "artistic {subject}, {artist_style} style, {color_palette}, detailed illustration"
  },
  "subjects": ["tiger", "motorcycle", "cat", "skull", "dragon"],
  "styles": ["screen print", "vector", "line art", "watercolor"],
  "colors": ["monochrome", "pastel", "vibrant", "earth tones"]
}
```

Generate prompts with Python:
```python
import json
import itertools

with open("prompts_templates.json") as f:
    data = json.load(f)

templates = data["templates"]
subjects = data["subjects"]
styles = data["styles"]

# Generate combinations
prompts = []
for template_name, template in templates.items():
    for subject, style in itertools.product(subjects[:3], styles[:2]):
        prompt = template.format(
            subject=subject,
            style=style,
            decade="1980s",
            artist_style="minimalist",
            color_palette="monochrome"
        )
        prompts.append(prompt)

with open("prompts_generated.txt", "w") as f:
    f.write("\n".join(prompts))
```

## Workflow Optimization

### Multi-Seed Generation (Variations)

```json
{
  "4": {
    "inputs": {
      "seed": 0,  // Set to 0 for random
      "steps": 25,
      "cfg": 7.5,
      ...
    }
  }
}
```

Each run will generate a different variation.

### Batch Processing Multiple Designs Per Prompt

```python
def generate_variations(prompt: str, count: int = 3):
    """Generate multiple variations of same prompt"""
    for i in range(count):
        workflow = load_workflow(WORKFLOW_FILE)
        workflow["4"]["inputs"]["seed"] = i  # Different seed
        queue_prompt(workflow)
```

### Quality vs. Speed Trade-offs

```json
{
  "fast": {
    "steps": 15,
    "scheduler": "karras"
  },
  "balanced": {
    "steps": 25,
    "scheduler": "normal"
  },
  "high_quality": {
    "steps": 40,
    "scheduler": "karras"
  }
}
```

## API Integration

### Using run.py with External APIs

```python
def submit_to_api(prompt: str, webhook_url: str):
    """Submit design request to external service"""
    payload = {
        "prompt": prompt,
        "callback": webhook_url,
        "model": "sdxl",
        "steps": 25
    }
    response = requests.post("http://localhost:8188/api/design", json=payload)
    return response.json()
```

### Integrate with Web Service

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt")
    
    workflow = load_workflow(WORKFLOW_FILE)
    workflow = inject_prompt(workflow, prompt)
    prompt_id = queue_prompt(workflow)
    
    return jsonify({"prompt_id": prompt_id, "status": "queued"})

@app.route("/api/status/<prompt_id>")
def status(prompt_id):
    # Check ComfyUI status
    return jsonify({"status": "processing"})
```

## Database Integration

### Track Generated Designs

```python
import sqlite3
from datetime import datetime

def log_generation(prompt: str, image_path: str, duration: float):
    """Log generation to database"""
    conn = sqlite3.connect("designs.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO designs (prompt, image_path, generated_at, duration)
        VALUES (?, ?, ?, ?)
    """, (prompt, image_path, datetime.now().isoformat(), duration))
    
    conn.commit()
    conn.close()
```

Create database schema:
```sql
CREATE TABLE IF NOT EXISTS designs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt TEXT NOT NULL,
    image_path TEXT NOT NULL,
    generated_at TIMESTAMP,
    duration REAL,
    rating INTEGER,
    platform TEXT
);
```

## Cloud Deployment

### RunPod Serverless

1. Create API endpoint on RunPod
2. Configure ComfyUI container
3. Update COMFY_SERVER URL:
   ```python
   COMFY_SERVER = "https://api.runpod.io/your-endpoint-id"
   ```

### Lambda Labs

```bash
# SSH into instance
ssh -i key.pem user@instance.lambdalabs.com

# Clone repo
git clone https://github.com/yourusername/tshirt-automation.git
cd tshirt-automation

# Run generation
python run.py --server http://localhost:8188
```

## Monitoring and Analytics

### Track Performance

```python
import time
import csv
from datetime import datetime

class GenerationMetrics:
    def __init__(self):
        self.metrics = []
    
    def record(self, prompt: str, status: str, duration: float):
        self.metrics.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "status": status,
            "duration": duration
        })
    
    def save(self, filename: str = "metrics.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "prompt", "status", "duration"])
            writer.writeheader()
            writer.writerows(self.metrics)

metrics = GenerationMetrics()

# Use in generation loop
start = time.time()
success = generate_design(prompt)
duration = time.time() - start
metrics.record(prompt, "success" if success else "failed", duration)
```

## Error Handling and Retry Logic

```python
import time
from typing import Callable

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    backoff_factor: float = 2.0
):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = backoff_factor ** attempt
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
            time.sleep(wait_time)

# Usage
def generate_with_retry(prompt: str):
    def _generate():
        workflow = load_workflow(WORKFLOW_FILE)
        workflow = inject_prompt(workflow, prompt)
        return queue_prompt(workflow)
    
    return retry_with_backoff(_generate)
```

## CI/CD Pipeline Enhancement

### Automated Testing

```yaml
name: Test and Validate

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/
```

Create `tests/test_workflow.py`:
```python
import json
import pytest

def test_workflow_valid():
    with open("workflow.json") as f:
        workflow = json.load(f)
    
    assert "1" in workflow, "Checkpoint loader required"
    assert "4" in workflow, "KSampler required"
    assert "6" in workflow, "VAE Decode required"

def test_prompts_file():
    with open("prompts.txt") as f:
        prompts = [line.strip() for line in f if line.strip()]
    
    assert len(prompts) > 0, "At least one prompt required"
    assert all(len(p) > 10 for p in prompts), "Prompts too short"
```

## Resources

- [ComfyUI Custom Nodes](https://github.com/comfyanonymous/ComfyUI/wiki/Custom-Nodes)
- [SDXL Fine-tuning](https://github.com/kohya-ss/sd-scripts)
- [Prompt Engineering Tips](https://openart.ai/discovery)
- [RunPod Documentation](https://docs.runpod.io/)
