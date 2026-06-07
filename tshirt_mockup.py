#!/usr/bin/env python3
"""
T-Shirt Mockup Generator
Overlays design images onto t-shirt templates
"""

from PIL import Image
from pathlib import Path
import os

TSHIRT_TEMPLATE = "input/tshirt_template.png"

def create_tshirt_mockup(design_path: str, output_path: str) -> bool:
    """
    Create a t-shirt mockup by overlaying design on template
    """
    try:
        # Load template
        if not Path(TSHIRT_TEMPLATE).exists():
            print(f"✗ Template not found: {TSHIRT_TEMPLATE}")
            return False
        
        template = Image.open(TSHIRT_TEMPLATE).convert("RGBA")
        template_width, template_height = template.size
        
        # Load design image
        design = Image.open(design_path).convert("RGBA")
        
        # Resize design to fit on t-shirt front (approximately 60% of template size)
        design_size = int(template_width * 0.6)
        design_resized = design.resize((design_size, design_size), Image.Resampling.LANCZOS)
        
        # Position design in center of t-shirt
        x_pos = (template_width - design_size) // 2
        y_pos = int(template_height * 0.35)  # Center area of t-shirt
        
        # Paste design onto template
        template.paste(design_resized, (x_pos, y_pos), design_resized)
        
        # Convert to RGB for saving as JPG
        template_rgb = Image.new("RGB", template.size, (255, 255, 255))
        template_rgb.paste(template, mask=template.split()[3] if template.mode == 'RGBA' else None)
        
        # Save mockup
        template_rgb.save(output_path, quality=95)
        print(f"✓ T-shirt mockup created: {Path(output_path).name}")
        return True
        
    except Exception as e:
        print(f"✗ Error creating mockup: {e}")
        import traceback
        traceback.print_exc()
        return False


def batch_create_mockups(input_dir: str = "output", output_dir: str = "output/mockups"):
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
    print(f"Designs found: {len(designs)}\n")
    
    successful = 0
    for design_file in designs:
        mockup_name = f"mockup_{design_file.stem.replace('design_', '')}.png"
        mockup_path = output_path / mockup_name
        
        print(f"Creating: {mockup_name}...", end=" ")
        if create_tshirt_mockup(str(design_file), str(mockup_path)):
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
    parser.add_argument("--input", default="output", help="Input directory with designs")
    parser.add_argument("--output", default="output/mockups", help="Output directory for mockups")
    
    args = parser.parse_args()
    
    batch_create_mockups(args.input, args.output)
