#!/usr/bin/env python3
"""
Google Colab T-Shirt Design Generator with Real-Time Monitoring
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
import threading
import time


def monitor_generation(output_path):
    """Monitor generation progress in real-time"""
    print("\n" + "="*60)
    print("  REAL-TIME GENERATION MONITOR")
    print("="*60 + "\n")
    
    last_count = 0
    start_time = time.time()
    
    while True:
        # Count generated images
        pngs = len(list(output_path.glob("*.png")))
        jpgs = len(list(output_path.glob("*.jpg")))
        current_count = pngs + jpgs
        
        if current_count != last_count:
            elapsed = time.time() - start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📸 Generated: {current_count} designs | "
                  f"⏱️ Elapsed: {hours:02d}:{minutes:02d}:{seconds:02d}")
            
            last_count = current_count
        
        time.sleep(2)


def main():
    print("\n" + "="*60)
    print("  T-SHIRT DESIGN GENERATION - COLAB (REAL-TIME)")
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
    print(f"✓ ComfyUI process started (PID: {comfyui_proc.pid})")
    
    # Wait for ComfyUI to be ready
    print("⏳ Waiting 30 seconds for ComfyUI to initialize...")
    time.sleep(30)
    
    # Setup output directory
    output_path = Path("output")
    output_path.mkdir(exist_ok=True)
    
    # Start monitoring in background thread
    monitor_thread = threading.Thread(
        target=monitor_generation,
        args=(output_path,),
        daemon=True
    )
    monitor_thread.start()
    
    # Run generation
    print("\n📸 Starting design generation...\n")
    result = subprocess.run([sys.executable, "run.py"])
    
    # Give monitor time to show final count
    time.sleep(3)
    
    # Cleanup
    print("\n⏹️ Stopping ComfyUI...")
    comfyui_proc.terminate()
    time.sleep(2)
    
    # Show final results
    pngs = list(output_path.glob("*.png"))
    zips = list(output_path.glob("*.zip"))
    
    print("\n" + "="*60)
    print("  GENERATION COMPLETE ✓")
    print("="*60)
    print(f"\n✓ Total images generated: {len(pngs)}")
    
    if zips:
        print(f"\n✓ Archives created:")
        for z in zips:
            size_mb = z.stat().st_size / (1024*1024)
            print(f"  📦 {z.name}")
            print(f"     Size: {size_mb:.1f} MB")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
