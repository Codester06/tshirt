#!/usr/bin/env python3
"""
T-Shirt Mockup Generator
Overlays design images onto t-shirt templates
"""

from PIL import Image, ImageDraw
from pathlib import Path
import os

def create_tshirt_mockup(design_path: str, output_path: str, tshirt_color: str = "white") -> bool:
    """
    Create a t-shirt mockup by overlaying design on template
    """
    try:
        # Load design image
        design = Image.open(design_path).convert("RGBA")
        
        # Create t-shirt template
        tshirt_width = 1000
        tshirt_height = 1200
        
        # T-shirt colors
        colors = {
            "white": (240, 240, 240),
            "black": (40, 40, 40),
            "blue": (25, 60, 120),
            "red": (180, 30, 30),
            "gray": (110, 110, 110),
        }
        
        color = colors.get(tshirt_color.lower(), colors["white"])
        
        # Create base image (light background)
        base = Image.new("RGB", (tshirt_width, tshirt_height), (200, 200, 200))
        draw = ImageDraw.Draw(base)
        
        # Draw t-shirt shape (simple rectangle with sleeves)
        # Main body
        draw.rectangle([150, 100, 850, 1100], fill=color, outline=(60, 60, 60), width=3)
        
        # Left sleeve
        draw.ellipse([20, 100, 200, 300], fill=color, outline=(60, 60, 60), width=3)
        
        # Right sleeve
        draw.ellipse([800, 100, 980, 300], fill=color, outline=(60, 60, 60), width=3)
        
        # Neck
        draw.ellipse([400, 80, 600, 200], fill=color, outline=(60, 60, 60), width=3)
        
        # Resize design to fit on t-shirt chest
        design_size = 350
        design_resized = design.resize((design_size, design_size), Image.Resampling.LANCZOS)
        
        # Position design in center of t-shirt chest
        x_pos = (tshirt_width - design_size) // 2
        y_pos = int(tshirt_height * 0.35)  # 35% from top (center of chest)
        
        # Paste design onto t-shirt
        base.paste(design_resized, (x_pos, y_pos), design_resized)
        
        # Save mockup
        base.save(output_path, quality=95)
        print(f"✓ T-shirt mockup created: {Path(output_path).name}")
        return True
        
    except Exception as e:
        print(f"✗ Error creating mockup: {e}")
        return False


def batch_create_mockups(input_dir: str = "output", output_dir: str = "output/mockups", tshirt_color: str = "white"):
    """
    Create mockups for all design images
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"✗ Input directory not found: {input_dir}")
        return
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all design images
    designs = sorted(input_path.glob("design_*.png"))
    
    if not designs:
        print("✗ No design images found")
        return
    
    print(f"\n{'='*60}")
    print(f"Creating T-Shirt Mockups")
    print(f"{'='*60}")
    print(f"T-shirt color: {tshirt_color}")
    print(f"Designs found: {len(designs)}\n")
    
    successful = 0
    for design_file in designs:
        mockup_name = f"mockup_{design_file.stem.replace('design_', '')}.png"
        mockup_path = output_path / mockup_name
        
        print(f"Creating: {mockup_name}...", end=" ")
        if create_tshirt_mockup(str(design_file), str(mockup_path), tshirt_color):
            successful += 1
            print("✓")
        else:
            print("✗")
    
    print(f"\n{'='*60}")
    print(f"Created: {successful}/{len(designs)} mockups")
    print(f"Location: {output_path}/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create t-shirt mockups from designs")
    parser.add_argument("--color", default="white", help="T-shirt color: white, black, blue, red, gray")
    parser.add_argument("--input", default="output", help="Input directory with designs")
    parser.add_argument("--output", default="output/mockups", help="Output directory for mockups")
    
    args = parser.parse_args()
    
    batch_create_mockups(args.input, args.output, args.color)
