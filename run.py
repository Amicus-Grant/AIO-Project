import cv2
import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import os
from tkinter import Tk, filedialog
import webbrowser

# Function to convert RGB color to Hex format
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

# Function to process the image and extract its color palette
def extract_color_palette(image_path, n_colors=5):
    try:
        # Load the image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Reshape the image into a 2D array of pixels and 3 color values (RGB)
        pixels = image.reshape(-1, 3)

        # Use K-Means clustering to find dominant colors
        kmeans = KMeans(n_clusters=n_colors, random_state=42)
        kmeans.fit(pixels)

        # Get the cluster centers (the dominant colors)
        colors = kmeans.cluster_centers_.astype(int)

        # Return colors
        return colors
    except Exception as e:
        print(f"Error processing the image {image_path}: {e}")
        return None

# Function to allow user to select images dynamically
def select_images():
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.webp")]
    )
    return list(file_paths)

# Let the user select images
image_paths = select_images()

# Process selected images and store results
all_colors = {}
for path in image_paths:
    colors = extract_color_palette(path)
    if colors is not None:
        all_colors[path] = colors

# Create a Plotly figure for interactive visualization
fig = go.Figure()

for i, (image_path, colors) in enumerate(all_colors.items()):
    hex_colors = [rgb_to_hex(color) for color in colors]

    # Add a row for each image's palette
    for j, color in enumerate(colors):
        fig.add_trace(go.Scatter(
            x=[j],  # Position each swatch horizontally
            y=[-i],  # Position each row vertically
            mode="markers+text",
            marker=dict(size=60, color=rgb_to_hex(color)),
            text=hex_colors[j],  # Add hex code as text
            textposition="top center",
            showlegend=False
        ))

    # Add the file name as a label for the row
    fig.add_trace(go.Scatter(
        x=[-1],  # Position file name outside the palette row
        y=[-i],
        mode="text",
        text=[os.path.basename(image_path)],
        textposition="middle left",
        showlegend=False
    ))

# Adjust layout for better visualization
fig.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor="white",
    margin=dict(l=100, r=50, t=50, b=50),
    height=200 * len(all_colors),  # Adjust height based on the number of palettes
    title="Color Palettes Extracted"
)

# Save the figure as an HTML file and open in the browser
output_file = "color_palettes.html"
fig.write_html(output_file)
print(f"Color palettes saved to {output_file}")

# Open in default browser
webbrowser.open(f"file://{os.path.abspath(output_file)}")
