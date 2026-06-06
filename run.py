#!/usr/bin/env python3
"""
ComfyUI T-Shirt Design Generator
Reads prompts, injects them into workflow, and generates designs
"""

import json
import os
import sys
import requests
import time
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
COMFY_SERVER = os.getenv("COMFY_SERVER", "http://127.0.0.1:8188")
WORKFLOW_FILE = "workflow.json"
PROMPTS_FILE = "prompts.txt"
OUTPUT_DIR = "output"
INPUT_DIR = "input"

# Ensure output directory exists
Path(OUTPUT_DIR).mkdir(exist_ok=True)
Path(INPUT_DIR).mkdir(exist_ok=True)


def load_prompts(filepath: str) -> List[str]:
    """Load prompts from text file, one per line"""
    try:
        with open(filepath, "r") as f:
            prompts = [line.strip() for line in f if line.strip()]
        print(f"✓ Loaded {len(prompts)} prompts from {filepath}")
        return prompts
    except FileNotFoundError:
        print(f"✗ Error: {filepath} not found")
        sys.exit(1)


def load_workflow(filepath: str) -> Dict:
    """Load ComfyUI workflow JSON"""
    try:
        with open(filepath, "r") as f:
            workflow = json.load(f)
        print(f"✓ Loaded workflow from {filepath}")
        return workflow
    except FileNotFoundError:
        print(f"✗ Error: {filepath} not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"✗ Error: Invalid JSON in {filepath}")
        sys.exit(1)


def inject_prompt(workflow: Dict, positive_prompt: str, negative_prompt: str = "") -> Dict:
    """
    Inject prompt into workflow
    Finds CLIP Text Encode nodes and updates them
    Adjust node numbers based on your workflow structure
    """
    workflow_copy = json.loads(json.dumps(workflow))
    
    # Default negative prompt for better results
    if not negative_prompt:
        negative_prompt = "blurry, low quality, distorted, ugly, bad anatomy, watermark"
    
    # Iterate through workflow nodes to find text encode nodes
    for node_id, node in workflow_copy.items():
        if isinstance(node, dict):
            class_name = node.get("class_type", "")
            
            # Update positive CLIP Text Encode
            if "CLIPTextEncode" in class_name or "text_encode" in class_name.lower():
                inputs = node.get("inputs", {})
                # Check if this is the positive prompt node
                if "text" in inputs:
                    # You may need to adjust this based on your workflow structure
                    if isinstance(inputs.get("text"), str):
                        # If there's a pattern, update it
                        if "positive" in node_id.lower() or node_id in ["4", "5", "6"]:
                            inputs["text"] = positive_prompt
    
    return workflow_copy


def queue_prompt(workflow: Dict) -> Optional[str]:
    """Queue a prompt to ComfyUI server"""
    try:
        payload = {"prompt": workflow}
        response = requests.post(
            f"{COMFY_SERVER}/prompt",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        prompt_id = result.get("prompt_id")
        print(f"  → Queued with prompt_id: {prompt_id}")
        return prompt_id
    except requests.exceptions.ConnectionError:
        print(f"✗ Error: Cannot connect to ComfyUI at {COMFY_SERVER}")
        print("  Make sure ComfyUI is running: python main.py")
        return None
    except Exception as e:
        print(f"✗ Error queuing prompt: {e}")
        return None


def wait_for_completion(prompt_id: str, timeout: int = 600) -> bool:
    """Poll server until prompt completes"""
    start_time = time.time()
    last_status = None
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(
                f"{COMFY_SERVER}/prompt",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Check if prompt is still queued or executing
            if prompt_id in data.get("queue_pending", []):
                status = "Queued"
            elif prompt_id in data.get("queue_running", {}):
                status = "Running"
            else:
                # Prompt completed
                return True
            
            if status != last_status:
                print(f"  → Status: {status}")
                last_status = status
            
            time.sleep(2)
        except Exception as e:
            print(f"  ⚠ Error checking status: {e}")
            time.sleep(2)
    
    print(f"✗ Timeout: Prompt did not complete within {timeout} seconds")
    return False


def generate_designs(prompts: List[str], dry_run: bool = False) -> None:
    """Generate designs from prompts"""
    workflow = load_workflow(WORKFLOW_FILE)
    
    print(f"\n{'='*60}")
    print(f"T-Shirt Design Generation")
    print(f"{'='*60}")
    print(f"Total designs to generate: {len(prompts)}")
    print(f"ComfyUI Server: {COMFY_SERVER}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"{'='*60}\n")
    
    if dry_run:
        print("DRY RUN MODE - No designs will be generated")
        print("Sample prompts:")
        for i, prompt in enumerate(prompts[:3], 1):
            print(f"  {i}. {prompt}")
        return
    
    successful = 0
    failed = 0
    
    for idx, prompt in enumerate(prompts, 1):
        print(f"[{idx}/{len(prompts)}] Generating: {prompt[:50]}...")
        
        # Inject prompt into workflow
        updated_workflow = inject_prompt(workflow, prompt)
        
        # Queue to ComfyUI
        prompt_id = queue_prompt(updated_workflow)
        if not prompt_id:
            failed += 1
            continue
        
        # Wait for completion
        if wait_for_completion(prompt_id):
            successful += 1
            print(f"  ✓ Design {idx} complete")
        else:
            failed += 1
            print(f"  ✗ Design {idx} failed")
        
        time.sleep(1)  # Brief delay between generations
    
    print(f"\n{'='*60}")
    print(f"Generation Summary")
    print(f"{'='*60}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(prompts)}")
    print(f"Output: {OUTPUT_DIR}/")
    print(f"{'='*60}\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate T-shirt designs using ComfyUI"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without running"
    )
    parser.add_argument(
        "--server",
        default=COMFY_SERVER,
        help="ComfyUI server URL (default: http://127.0.0.1:8188)"
    )
    parser.add_argument(
        "--prompts",
        default=PROMPTS_FILE,
        help="Path to prompts file (default: prompts.txt)"
    )
    
    args = parser.parse_args()
    
    # Override server if provided
    globals()["COMFY_SERVER"] = args.server
    
    # Load and generate
    prompts = load_prompts(args.prompts)
    generate_designs(prompts, dry_run=args.dry_run)


def create_archive_after_generation():
    """Create ZIP archive after generation completes"""
    try:
        import zipfile
        from datetime import datetime
        
        output_path = Path(OUTPUT_DIR)
        if not output_path.exists():
            return False
        
        # Find PNG files
        images = list(output_path.glob("*.png")) + list(output_path.glob("*.jpg"))
        if not images:
            print("No images found to archive")
            return False
        
        zip_filename = f"tshirt-designs-{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = output_path / zip_filename
        
        print(f"\n📦 Creating archive: {zip_filename}")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for image in images:
                zipf.write(image, arcname=image.name)
        
        size_mb = zip_path.stat().st_size / (1024*1024)
        print(f"✓ Archive created: {zip_filename}")
        print(f"  Size: {size_mb:.2f} MB")
        print(f"  Location: {zip_path}")
        return True
    except Exception as e:
        print(f"⚠ Could not create archive: {e}")
        return False


if __name__ == "__main__":
    main()
    
    # Automatically create archive after generation
    print("\nAutomatically creating archive...")
    create_archive_after_generation()
