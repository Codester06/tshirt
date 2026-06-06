#!/usr/bin/env python3
"""
Google Colab T-Shirt Design Generator
Simple wrapper for Colab environment
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


def main():
    print("\n" + "="*60)
    print("  T-SHIRT DESIGN GENERATION - COLAB")
    print("="*60 + "\n")
    
    # Check if ComfyUI exists
    if not Path("ComfyUI").exists():
        print("✗ ComfyUI not found. Make sure you ran all setup cells.")
        return
    
    # Check if prompts exist
    if not Path("prompts.txt").exists():
        print("✗ prompts.txt not found")
        return
    
    # Start ComfyUI in background
    print("🚀 Starting ComfyUI...")
    os.chdir("ComfyUI")
    comfyui_proc = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    os.chdir("..")
    
    # Wait a bit longer for Colab
    import time
    print("⏳ Waiting 30 seconds for ComfyUI to be ready...")
    time.sleep(30)
    
    # Run generation
    print("\n📸 Starting design generation...\n")
    result = subprocess.run([sys.executable, "run.py"])
    
    # Cleanup
    print("\n⏹️ Stopping ComfyUI...")
    comfyui_proc.terminate()
    time.sleep(2)
    
    # Show results
    output_path = Path("output")
    pngs = list(output_path.glob("*.png"))
    zips = list(output_path.glob("*.zip"))
    
    print("\n" + "="*60)
    print("  GENERATION COMPLETE")
    print("="*60)
    print(f"✓ Generated: {len(pngs)} images")
    
    if zips:
        for z in zips:
            size_mb = z.stat().st_size / (1024*1024)
            print(f"✓ Archive: {z.name} ({size_mb:.1f} MB)")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
