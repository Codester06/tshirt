#!/usr/bin/env python3
"""
Real-time T-Shirt Design Generation Monitor
Starts ComfyUI and monitors generation progress live
"""

import os
import subprocess
import time
import threading
from pathlib import Path
from datetime import datetime
import sys

OUTPUT_DIR = "output"
COMFY_DIR = "../ComfyUI"


def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def start_comfyui():
    """Start ComfyUI in background"""
    print_header("Starting ComfyUI")
    
    try:
        os.chdir(COMFY_DIR)
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        os.chdir("..")
        print("✓ ComfyUI process started (PID: {})".format(process.pid))
        return process
    except Exception as e:
        print(f"✗ Failed to start ComfyUI: {e}")
        return None


def wait_for_server(timeout=30):
    """Wait for ComfyUI server to be ready"""
    print("⏳ Waiting for ComfyUI server to start...")
    
    import requests
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://127.0.0.1:8188/system/stats", timeout=2)
            if response.status_code == 200:
                print("✓ ComfyUI server is ready!\n")
                return True
        except:
            pass
        
        time.sleep(1)
    
    print("✗ ComfyUI server failed to start within timeout")
    return False


def monitor_generation():
    """Monitor generation progress in real-time"""
    print_header("Real-Time Generation Monitor")
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    
    last_count = 0
    start_time = time.time()
    
    while True:
        # Count generated images
        pngs = len(list(output_path.glob("*.png")))
        jpgs = len(list(output_path.glob("*.jpg")))
        current_count = pngs + jpgs
        
        if current_count > last_count or current_time == time.time():
            elapsed = time.time() - start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📸 Generated: {current_count} designs | "
                  f"⏱️ Elapsed: {hours:02d}:{minutes:02d}:{seconds:02d}")
            
            last_count = current_count
        
        time.sleep(2)


def run_generation():
    """Run the generation script"""
    print_header("Starting T-Shirt Design Generation")
    
    try:
        # Check if prompts.txt exists
        if not Path("prompts.txt").exists():
            print("✗ prompts.txt not found!")
            return False
        
        # Count prompts
        with open("prompts.txt") as f:
            prompts = [line.strip() for line in f if line.strip()]
        
        print(f"✓ Loaded {len(prompts)} prompts")
        print(f"✓ Starting generation...\n")
        
        # Run generation
        result = subprocess.run(
            [sys.executable, "run.py"],
            capture_output=False
        )
        
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Generation failed: {e}")
        return False


def show_results():
    """Show final results"""
    print_header("Generation Complete!")
    
    output_path = Path(OUTPUT_DIR)
    
    pngs = list(output_path.glob("*.png"))
    jpgs = list(output_path.glob("*.jpg"))
    zips = list(output_path.glob("*.zip"))
    
    total_images = len(pngs) + len(jpgs)
    
    print(f"✓ Total designs generated: {total_images}")
    print(f"✓ PNG files: {len(pngs)}")
    print(f"✓ JPG files: {len(jpgs)}")
    
    if zips:
        print(f"\n✓ Archive created:")
        for z in zips:
            size_mb = z.stat().st_size / (1024*1024)
            print(f"  📦 {z.name} ({size_mb:.2f} MB)")
    
    if pngs or jpgs:
        print(f"\n✓ Generated files:")
        for img in (pngs + jpgs)[:5]:  # Show first 5
            size_kb = img.stat().st_size / 1024
            print(f"  🖼️ {img.name} ({size_kb:.0f} KB)")
        
        if len(pngs + jpgs) > 5:
            print(f"  ... and {len(pngs + jpgs) - 5} more files")
    
    print(f"\n{'='*60}")
    print(f"Output directory: {OUTPUT_DIR}/")
    print(f"{'='*60}\n")


def stop_comfyui(process):
    """Stop ComfyUI gracefully"""
    if process:
        print("\n⏹️ Stopping ComfyUI...")
        process.terminate()
        try:
            process.wait(timeout=5)
            print("✓ ComfyUI stopped")
        except subprocess.TimeoutExpired:
            process.kill()
            print("✓ ComfyUI killed")


def main():
    """Main orchestration"""
    print("\n" + "="*60)
    print("  T-SHIRT DESIGN GENERATION - REAL-TIME MONITOR")
    print("="*60)
    
    comfyui_process = None
    
    try:
        # Step 1: Start ComfyUI
        comfyui_process = start_comfyui()
        if not comfyui_process:
            return
        
        # Step 2: Wait for server
        if not wait_for_server():
            return
        
        # Step 3: Start monitoring in background thread
        monitor_thread = threading.Thread(target=monitor_generation, daemon=True)
        monitor_thread.start()
        
        # Step 4: Run generation
        success = run_generation()
        
        # Step 5: Show results
        if success:
            show_results()
        else:
            print("✗ Generation failed")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
    finally:
        # Cleanup
        stop_comfyui(comfyui_process)


if __name__ == "__main__":
    main()
