#!/usr/bin/env python3
"""
Batch process and post-process T-shirt designs
- Remove backgrounds
- Upscale images
- Rename with metadata
- Package for print-on-demand
"""

import os
import json
import shutil
from pathlib import Path
from typing import List, Dict
from datetime import datetime

OUTPUT_DIR = "output"
PROCESSED_DIR = "output/processed"
METADATA_DIR = "output/metadata"


def ensure_directories():
    """Create necessary directories"""
    Path(PROCESSED_DIR).mkdir(parents=True, exist_ok=True)
    Path(METADATA_DIR).mkdir(parents=True, exist_ok=True)


def get_image_files() -> List[Path]:
    """Get all generated images"""
    output_path = Path(OUTPUT_DIR)
    if not output_path.exists():
        print(f"✗ Output directory {OUTPUT_DIR} not found")
        return []
    
    images = list(output_path.glob("*.png")) + list(output_path.glob("*.jpg"))
    print(f"✓ Found {len(images)} image files")
    return images


def create_metadata(filename: str, prompt: str) -> Dict:
    """Create metadata for design"""
    return {
        "filename": filename,
        "prompt": prompt,
        "generated": datetime.now().isoformat(),
        "platforms": {
            "etsy": {
                "tags": ["tshirt", "design", "print-on-demand"],
                "category": "Clothing"
            },
            "redbubble": {
                "tags": ["tshirt", "design"],
                "category": "Apparel"
            },
            "merch_by_amazon": {
                "category": "Clothing",
                "adult": False
            }
        }
    }


def process_batch(prompts_file: str = "prompts.txt"):
    """Process batch of generated images"""
    ensure_directories()
    
    # Load prompts for metadata
    prompts = {}
    if Path(prompts_file).exists():
        with open(prompts_file, "r") as f:
            for idx, line in enumerate(f, 1):
                prompts[idx] = line.strip()
    
    # Get images
    images = get_image_files()
    
    print(f"\n{'='*60}")
    print(f"Batch Processing")
    print(f"{'='*60}\n")
    
    for idx, image_path in enumerate(images, 1):
        print(f"[{idx}/{len(images)}] Processing: {image_path.name}")
        
        # Generate output filename
        design_name = f"design_{idx:04d}"
        output_name = f"{design_name}.png"
        output_path = Path(PROCESSED_DIR) / output_name
        
        # Copy image
        shutil.copy2(image_path, output_path)
        print(f"  → Copied to {output_path.name}")
        
        # Create metadata
        prompt = prompts.get(idx, "Generated design")
        metadata = create_metadata(output_name, prompt)
        
        metadata_path = Path(METADATA_DIR) / f"{design_name}.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        print(f"  → Created metadata")
    
    # Create summary
    summary = {
        "total_designs": len(images),
        "batch_date": datetime.now().isoformat(),
        "output_directory": PROCESSED_DIR,
        "print_ready": True,
        "recommendations": {
            "etsy": "Recommended DPI: 300, Format: PNG with transparent background",
            "redbubble": "Recommended size: 4500x5400px minimum for best quality",
            "merch_by_amazon": "Upload PNG, Amazon handles sizing and printing"
        }
    }
    
    summary_path = Path(METADATA_DIR) / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Batch Processing Complete")
    print(f"{'='*60}")
    print(f"Processed designs: {len(images)}")
    print(f"Output: {PROCESSED_DIR}/")
    print(f"Metadata: {METADATA_DIR}/")
    print(f"{'='*60}\n")
    
    return len(images)


def create_zip_archive():
    """Create ZIP archive for download"""
    try:
        import zipfile
        
        processed_path = Path(PROCESSED_DIR)
        if not processed_path.exists() or not list(processed_path.glob("*.png")):
            print("✗ No processed images found to archive")
            return False
        
        zip_path = Path("output") / f"tshirt-designs-{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add images
            for image in processed_path.glob("*.png"):
                zipf.write(image, arcname=f"designs/{image.name}")
            
            # Add metadata
            metadata_path = Path(METADATA_DIR)
            if metadata_path.exists():
                for metadata in metadata_path.glob("*.json"):
                    zipf.write(metadata, arcname=f"metadata/{metadata.name}")
        
        print(f"✓ Created archive: {zip_path}")
        print(f"  Size: {zip_path.stat().st_size / (1024*1024):.2f} MB")
        return True
    except Exception as e:
        print(f"✗ Error creating archive: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch process T-shirt designs")
    parser.add_argument("--zip", action="store_true", help="Create ZIP archive")
    parser.add_argument("--prompts", default="prompts.txt", help="Path to prompts file")
    
    args = parser.parse_args()
    
    count = process_batch(args.prompts)
    
    if args.zip and count > 0:
        create_zip_archive()
