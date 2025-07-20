# Thread Art Tools

A collection of tools to create, edit, and visualize thread art files in YAML format.

## Tools Included

1. **Thread Art Generator** (`thread-art-generate`) - Creates thread art files with nails arranged in geometric shapes
2. **Thread Art Visualizer** (`thread-art`) - Reads and visualizes thread art files as images

## File Format

The thread art file should be in YAML format with the following structure:

```yaml
nails:
  - [x1, y1]  # Nail coordinates in unit square (0..1)
  - [x2, y2]
  - [x3, y3]
  # ... more nails

thread:
  - nail_index_1  # Index of nail (0 to N-1)
  - nail_index_2
  - nail_index_3
  # ... thread path
```

### Format Details

- **nails**: List of N nail positions as [x, y] coordinates in the unit square (0..1)
- **thread**: List of M nail indices (0..(N-1)) defining the path of the virtual thread

## Installation

### Using Poetry (Recommended)
```bash
poetry install
```

### Using pip
```bash
pip install -r requirements.txt
```

## Usage

### Thread Art Generator

Create new thread art files with nails arranged in geometric shapes:

#### Using Poetry
```bash
# Generate a circle with 12 nails
poetry run thread-art-generate 12 circle -o circle_12.yml

# Generate a square with 20 nails
poetry run thread-art-generate 20 square -o square_20.yml

# Generate with default output filename
poetry run thread-art-generate 8 circle
```

#### Using Python directly
```bash
# Generate a circle with 12 nails
python thread_art_generator.py 12 circle -o circle_12.yml

# Generate a square with 20 nails
python thread_art_generator.py 20 square -o square_20.yml
```

#### Generator Command Line Options

- `num_nails`: Number of nails to generate (required, positive integer)
- `shape`: Shape to arrange nails in (required, choices: `circle`, `square`)
- `-o, --output`: Output YAML file path (default: `generated_thread_art.yml`)

#### Shape Details

**Circle:**
- Nails are evenly distributed around a circle
- Circle is centered at (0.5, 0.5) with radius 0.5
- Maximizes the circle within the unit square
- Works with any number of nails ≥ 1

**Square:**
- Nails are evenly distributed around the square perimeter
- Square uses the full unit square from (0,0) to (1,1)
- Nails are placed starting from bottom edge, then right, top, left
- Requires at least 4 nails

### Thread Art Visualizer

Visualize existing thread art files:

#### Using Poetry
```bash
# Basic usage
poetry run thread-art example.yml

# Specify output file
poetry run thread-art example.yml -o my_thread_art.png

# Custom image size
poetry run thread-art example.yml -s 1200 1200
```

#### Using Python directly
```bash
# Basic usage
python thread_art_visualizer.py example.yml

# Specify output file
python thread_art_visualizer.py example.yml -o my_thread_art.png

# Custom image size
python thread_art_visualizer.py example.yml -s 1200 1200
```

#### Visualizer Command Line Options

- `input`: Input YAML file path (required)
- `-o, --output`: Output image file path (default: `thread_art.png`)
- `-s, --size`: Output image size as width height (default: `800 800`)

## Visualization Features

The generated image includes:
- Red circles representing nails with their index numbers
- Blue lines showing the thread path
- Green square marking the start point
- Orange triangle marking the end point
- Grid overlay for reference
- Statistics showing number of nails and thread segments

## Workflow Examples

### Creating and Visualizing Thread Art

1. **Generate a base template:**
   ```bash
   poetry run thread-art-generate 24 circle -o my_circle.yml
   ```

2. **Edit the thread path manually:**
   Open `my_circle.yml` and add nail indices to the `thread:` array:
   ```yaml
   thread:
     - 0
     - 12  # opposite nail
     - 6   # quarter turn
     - 18  # opposite of 6
     - 3   # etc...
   ```

3. **Visualize the result:**
   ```bash
   poetry run thread-art my_circle.yml -o my_circle_art.png
   ```

### Quick Test Pattern

```bash
# Generate a square with 16 nails
poetry run thread-art-generate 16 square -o test_square.yml

# Visualize the empty pattern (shows just the nails)
poetry run thread-art test_square.yml -o test_square_nails.png
```

## Example Files

- `example.yml` - Sample thread art file with 7 nails and 15 thread segments
- `circle_12.yml` - Generated circle with 12 nails (empty thread)
- `square_16.yml` - Generated square with 16 nails (empty thread)
