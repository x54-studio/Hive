#!/usr/bin/env python3

import math
from PIL import Image, ImageDraw, ImageFilter

def generate_hex_favicon(
    size=64,
    fill_color=(255, 204, 0),        # "Honey" fill color
    border_color=(153, 102, 0),      # Darker "honey" for the border
    border_width=3,
    corner_softness=1.0,
    ico_filename="favicon.ico"
):
    """
    Generate a hexagonal favicon with a slightly rounded effect by blurring the mask.

    :param size:            Width/height of the favicon in pixels.
    :param fill_color:      RGBA or RGB color for the hex fill.
    :param border_color:    RGBA or RGB color for the hex border.
    :param border_width:    Thickness of the hex border in pixels.
    :param corner_softness: Gaussian blur radius for softening corners.
    :param ico_filename:    Output .ico filename.
    """

    # 1) Create blank RGBA image with transparent background
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_im = ImageDraw.Draw(im)

    # 2) Define the hexagon corners (centered)
    cx, cy = size // 2, size // 2
    # Radius so the hex fits well
    r = int(size * 0.4)

    # We offset the angle by 30 degrees so the top/bottom edges are flat
    # If you want a corner at the top, remove the +30
    corners = []
    for i in range(6):
        angle_deg = 60 * i + 30
        angle_rad = math.radians(angle_deg)
        x = cx + r * math.cos(angle_rad)
        y = cy + r * math.sin(angle_rad)
        corners.append((x, y))

    # 3) Create a mask for the filled hex shape
    mask_filled = Image.new("L", (size, size), 0)  # Single-channel "L" for mask
    draw_mask_filled = ImageDraw.Draw(mask_filled)
    draw_mask_filled.polygon(corners, fill=255)
    # Slight blur to soften the sharp polygon edges ("rounded" feel)
    if corner_softness > 0:
        mask_filled = mask_filled.filter(ImageFilter.GaussianBlur(corner_softness))

    # 4) Create a mask for the border (outline). We draw the same polygon outline.
    mask_border = Image.new("L", (size, size), 0)
    draw_mask_border = ImageDraw.Draw(mask_border)
    # PIL's polygon outline uses an integer 'width' parameter for thickness
    draw_mask_border.polygon(corners, outline=255, width=border_width)
    if corner_softness > 0:
        mask_border = mask_border.filter(ImageFilter.GaussianBlur(corner_softness))

    # 5) Construct the filled shape image using the filled mask
    fill_image = Image.new("RGBA", (size, size), fill_color)
    fill_image.putalpha(mask_filled)  # apply the alpha mask

    # 6) Construct the border image using the border mask
    border_image = Image.new("RGBA", (size, size), border_color)
    border_image.putalpha(mask_border)

    # 7) Combine (alpha-composite) the border on top of the fill
    final_im = Image.alpha_composite(fill_image, border_image)

    # 8) Paste the final image onto the original transparent background
    #    (In many cases, alpha_composite on top of a blank RGBA is not strictly needed—
    #     we already have final_im as RGBA with proper transparency.)
    im.paste(final_im, (0, 0))

    # 9) Save as ICO (favicon format)
    im.save(ico_filename, format="ICO", sizes=[(16,16), (32,32), (64,64)])

def main():
    # Customize parameters here if desired
    generate_hex_favicon(
        size=64,
        fill_color=(255, 204, 0, 255),    # "honey" color
        border_color=(153, 102, 0, 255),  # darker honey color
        border_width=3,
        corner_softness=1.0,
        ico_filename="favicon.ico"
    )
    print("favicon.ico generated successfully.")

if __name__ == "__main__":
    main()
