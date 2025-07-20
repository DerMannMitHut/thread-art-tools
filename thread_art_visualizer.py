#!/usr/bin/env python3
"""
Thread Art Visualizer

Reads a thread art YAML file and generates a visual representation.
The YAML file should contain:
- nails: List of [x, y] coordinates in unit square (0..1)
- thread: List of nail indices defining the thread path
"""

import yaml
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
import sys
from pathlib import Path


def load_thread_art(file_path):
    """Load thread art data from YAML file."""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        if 'nails' not in data or 'thread' not in data:
            raise ValueError("YAML file must contain 'nails' and 'thread' keys")
        
        nails = data['nails']
        thread = data['thread']
        
        # Validate nails format
        for i, nail in enumerate(nails):
            if not isinstance(nail, list) or len(nail) != 2:
                raise ValueError(f"Nail {i} must be a list of 2 coordinates")
            x, y = nail
            if not (0 <= x <= 1 and 0 <= y <= 1):
                raise ValueError(f"Nail {i} coordinates must be in unit square [0,1]")
        
        # Validate thread format
        max_nail_index = len(nails) - 1
        for i, nail_idx in enumerate(thread):
            if not isinstance(nail_idx, int) or not (0 <= nail_idx <= max_nail_index):
                raise ValueError(f"Thread point {i}: nail index {nail_idx} is invalid (must be 0-{max_nail_index})")
        
        return nails, thread
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error in file format: {e}")
        sys.exit(1)


def visualize_thread_art(nails, thread, output_path, image_size=(800, 800), nail_size=50):
    """Create visualization of thread art."""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Set up the plot
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_title('Thread Art Visualization', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Draw the thread path
    thread_x = []
    thread_y = []
    
    for nail_idx in thread:
        x, y = nails[nail_idx]
        thread_x.append(x)
        thread_y.append(y)
    
    # Plot thread as connected lines
    ax.plot(thread_x, thread_y, 'b-', linewidth=1, alpha=0.7, label='Thread')
    
    # Draw nails
    for i, (x, y) in enumerate(nails):
        circle = patches.Circle((x, y), 0.015, facecolor='red', edgecolor='black', 
                               linewidth=2, zorder=10)
        ax.add_patch(circle)
        # Add nail numbers
        ax.annotate(str(i), (x, y), xytext=(5, 5), textcoords='offset points',
                   fontsize=8, fontweight='bold', color='white', ha='center', va='center')
    
    # Mark start and end points
    if thread:
        start_nail = nails[thread[0]]
        end_nail = nails[thread[-1]]
        
        ax.scatter(start_nail[0], start_nail[1], s=nail_size*2, c='green', 
                  marker='s', label='Start', zorder=15, edgecolors='black')
        ax.scatter(end_nail[0], end_nail[1], s=nail_size*2, c='orange', 
                  marker='^', label='End', zorder=15, edgecolors='black')
    
    # Add legend
    ax.legend(loc='upper right')
    
    # Add statistics
    stats_text = f"Nails: {len(nails)}\nThread segments: {len(thread)-1 if thread else 0}"
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Save the image
    plt.tight_layout()
    plt.savefig(output_path, dpi=image_size[0]//10, bbox_inches='tight')
    print(f"Thread art visualization saved to: {output_path}")
    
    # Show the plot
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Visualize thread art from YAML file')
    parser.add_argument('input', help='Input YAML file path')
    parser.add_argument('-o', '--output', help='Output image file path', 
                       default='thread_art.png')
    parser.add_argument('-s', '--size', nargs=2, type=int, default=[800, 800],
                       help='Output image size (width height)')
    
    args = parser.parse_args()
    
    # Load thread art data
    nails, thread = load_thread_art(args.input)
    
    print(f"Loaded thread art with {len(nails)} nails and {len(thread)} thread points")
    
    # Create visualization
    visualize_thread_art(nails, thread, args.output, tuple(args.size))


if __name__ == "__main__":
    main()
