#!/usr/bin/env python3
"""
Thread Art Generator

Creates thread art YAML files with nails arranged in geometric shapes.
Supports circle and square shapes with evenly distributed nails.
The shapes are maximized within the unit square (0..1).
"""

import yaml
import math
import argparse
import sys
from pathlib import Path


def generate_circle_nails(num_nails):
    """Generate nail positions evenly distributed on a circle."""
    nails = []
    # Circle centered at (0.5, 0.5) with radius 0.5 to maximize within unit square
    center_x, center_y = 0.5, 0.5
    radius = 0.5
    
    for i in range(num_nails):
        # Evenly distribute nails around the circle
        angle = 2 * math.pi * i / num_nails
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        nails.append([round(x, 6), round(y, 6)])
    
    return nails


def generate_square_nails(num_nails):
    """Generate nail positions evenly distributed on a square perimeter."""
    nails = []
    
    if num_nails < 4:
        raise ValueError("Square shape requires at least 4 nails")
    
    # Square from (0, 0) to (1, 1) to maximize within unit square
    perimeter = 4.0  # Total perimeter length
    spacing = perimeter / num_nails  # Distance between nails
    
    current_pos = 0.0
    
    for i in range(num_nails):
        pos_on_perimeter = (current_pos) % perimeter
        
        if pos_on_perimeter <= 1.0:
            # Bottom edge: (0,0) to (1,0)
            x = pos_on_perimeter
            y = 0.0
        elif pos_on_perimeter <= 2.0:
            # Right edge: (1,0) to (1,1)
            x = 1.0
            y = pos_on_perimeter - 1.0
        elif pos_on_perimeter <= 3.0:
            # Top edge: (1,1) to (0,1)
            x = 1.0 - (pos_on_perimeter - 2.0)
            y = 1.0
        else:
            # Left edge: (0,1) to (0,0)
            x = 0.0
            y = 1.0 - (pos_on_perimeter - 3.0)
        
        nails.append([round(x, 6), round(y, 6)])
        current_pos += spacing
    
    return nails


def create_thread_art_file(num_nails, shape, output_path):
    """Create a thread art YAML file with the specified parameters."""
    
    # Generate nails based on shape
    if shape.lower() == 'circle':
        nails = generate_circle_nails(num_nails)
    elif shape.lower() == 'square':
        nails = generate_square_nails(num_nails)
    else:
        raise ValueError(f"Unsupported shape: {shape}. Use 'circle' or 'square'.")
    
    # Create thread art data structure
    thread_art_data = {
        'nails': nails,
        'thread': []  # Empty thread as requested
    }
    
    # Add metadata as comments in the YAML
    yaml_content = f"""# Thread Art File
# Generated with {num_nails} nails in {shape} shape
# Shape maximized within unit square (0..1)
# Thread path is empty - ready for manual editing

nails:
"""
    
    # Add nails with comments showing their index
    for i, nail in enumerate(nails):
        yaml_content += f"  - [{nail[0]}, {nail[1]}]    # nail {i}\n"
    
    yaml_content += "\nthread: []\n"
    
    # Write to file
    try:
        with open(output_path, 'w') as f:
            f.write(yaml_content)
        print(f"Thread art file created: {output_path}")
        print(f"  - Shape: {shape}")
        print(f"  - Nails: {num_nails}")
        print(f"  - Thread: empty (ready for editing)")
    except IOError as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Generate thread art YAML files with geometric nail arrangements')
    parser.add_argument('num_nails', type=int, help='Number of nails to generate')
    parser.add_argument('shape', choices=['circle', 'square'], help='Shape to arrange nails in')
    parser.add_argument('-o', '--output', help='Output YAML file path', 
                       default='generated_thread_art.yml')
    
    args = parser.parse_args()
    
    # Validate input
    if args.num_nails <= 0:
        print("Error: Number of nails must be positive")
        sys.exit(1)
    
    if args.shape.lower() == 'square' and args.num_nails < 4:
        print("Error: Square shape requires at least 4 nails")
        sys.exit(1)
    
    # Generate the thread art file
    try:
        create_thread_art_file(args.num_nails, args.shape, args.output)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
