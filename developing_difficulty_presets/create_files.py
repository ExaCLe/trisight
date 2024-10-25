from PIL import Image, ImageDraw
import math
import os
import random


def rotate_point(x, y, cx, cy, angle):
    angle_rad = math.radians(angle)
    cos_theta = math.cos(angle_rad)
    sin_theta = math.sin(angle_rad)
    dx = x - cx
    dy = y - cy
    x_new = dx * cos_theta - dy * sin_theta + cx
    y_new = dx * sin_theta + dy * cos_theta + cy
    return (x_new, y_new)


def get_triangle_points(center_x, center_y, side_length, orientation):
    h = side_length * (math.sqrt(3) / 2)  # Height of the equilateral triangle

    # Base triangle pointing 'north'
    points = [
        (center_x, center_y - h * 2 / 3),  # Top vertex
        (center_x - side_length / 2, center_y + h / 3),  # Bottom-left vertex
        (center_x + side_length / 2, center_y + h / 3),  # Bottom-right vertex
    ]

    # Random rotation angle based on orientation
    orientation_angles = {"north": 0, "east": 90, "south": 180, "west": 270}

    angle = orientation_angles.get(orientation, 0)

    # Rotate each point around the center
    rotated_points = [rotate_point(x, y, center_x, center_y, angle) for x, y in points]

    return rotated_points


def relative_luminance(rgb):
    """Calculate the relative luminance of a color in sRGB space."""

    def linearize(c):
        c = c / 255.0
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    R, G, B = rgb
    R_lin = linearize(R)
    G_lin = linearize(G)
    B_lin = linearize(B)
    return 0.2126 * R_lin + 0.7152 * G_lin + 0.0722 * B_lin


def contrast_ratio(L1, L2):
    """Calculate the contrast ratio between two luminance values."""
    if L1 > L2:
        return (L1 + 0.05) / (L2 + 0.05)
    else:
        return (L2 + 0.05) / (L1 + 0.05)


def find_color_with_luminance(target_luminance):
    """Find an RGB color that has the specified relative luminance."""
    # For simplicity, we'll use grayscale colors
    # So R = G = B
    for gray in range(256):
        rgb = (gray, gray, gray)
        L = relative_luminance(rgb)
        if abs(L - target_luminance) < 0.005:
            return rgb
    # If not found, return the closest match
    return None


def generate_colors_with_contrast_ratio(desired_contrast_ratio):
    """Generate a pair of grayscale colors with the desired contrast ratio."""
    # We'll generate colors in grayscale for simplicity
    # Try luminance values from 0 to 1
    luminance_values = [i / 100.0 for i in range(1, 100)]
    random.shuffle(luminance_values)  # Shuffle to introduce randomness
    for L1 in luminance_values:
        # Calculate possible L2 values based on the contrast ratio formula
        C = desired_contrast_ratio
        possible_L2 = [
            (L1 + 0.05) / C - 0.05,  # L2 when L1 > L2
            C * (L1 + 0.05) - 0.05,  # L2 when L2 > L1
        ]
        for L2 in possible_L2:
            if 0 <= L2 <= 1:
                # Find RGB colors for L1 and L2
                rgb1 = find_color_with_luminance(L1)
                rgb2 = find_color_with_luminance(L2)
                if rgb1 and rgb2:
                    return rgb1, rgb2
    # If not found, return None
    return None, None


def generate_triangle_circle_image(
    image_size,
    circle_color,
    triangle_color,
    triangle_size_ratio,
    orientation,
    save_path,
):
    # Create a white background image
    image = Image.new("RGB", (image_size, image_size), "white")
    draw = ImageDraw.Draw(image)

    # Define circle properties
    circle_radius = image_size * 0.45  # 90% of half the image size
    center_x = image_size / 2
    center_y = image_size / 2
    circle_bbox = [
        (center_x - circle_radius, center_y - circle_radius),
        (center_x + circle_radius, center_y + circle_radius),
    ]
    draw.ellipse(circle_bbox, fill=circle_color)

    # Define triangle properties
    triangle_side_length = (
        circle_radius * triangle_size_ratio * 2
    )  # Multiply by 2 to scale within the circle
    triangle_points = get_triangle_points(
        center_x, center_y, triangle_side_length, orientation
    )
    draw.polygon(triangle_points, fill=triangle_color)

    # Save the image
    image.save(save_path)


# Parameters
image_size = 500
orientations = ["north", "east", "south", "west"]  # All possible orientations
triangle_size_ratio = 0.05  # Small triangle

# Contrast ratios to test, starting from 2.0 and decreasing in steps of 0.1
contrast_ratios = [1.1 - i * 0.01 for i in range(10)]  # [2.0, 1.9, ..., 1.1]
print(contrast_ratios)

# Create output directory
output_dir = "contrast_experiment"
os.makedirs(output_dir, exist_ok=True)

for cr in contrast_ratios:
    cr_str = str(cr)
    for i in range(5):  # Generate 5 images per contrast ratio
        # Generate colors with the specified contrast ratio
        rgb1, rgb2 = generate_colors_with_contrast_ratio(cr)
        if rgb1 is None or rgb2 is None:
            print(f"Could not find colors with contrast ratio {cr}")
            continue
        # Randomly assign circle and triangle colors
        if random.choice([True, False]):
            circle_color = rgb1
            triangle_color = rgb2
        else:
            circle_color = rgb2
            triangle_color = rgb1
        # Random orientation
        orientation = random.choice(orientations)
        # File name includes contrast ratio
        file_name = f"cr_{cr_str}_img_{i+1}_{orientation}.png"
        save_path = os.path.join(output_dir, file_name)
        # Generate and save the image
        generate_triangle_circle_image(
            image_size,
            circle_color,
            triangle_color,
            triangle_size_ratio,
            orientation,
            save_path,
        )
