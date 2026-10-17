from PIL import Image
import numpy as np

im = Image.open("assets/front.png").convert("RGB")
arr = np.array(im)

# Let us print the bounding boxes of borders
# A border pixel is close to (218, 221, 216)
is_border = (np.abs(arr[:, :, 0] - 218) < 10) & (np.abs(arr[:, :, 1] - 221) < 10) & (np.abs(arr[:, :, 2] - 216) < 10)

# Check horizontal lines of border
border_rows = np.where(np.sum(is_border, axis=1) > 500)[0]
print("Border rows (horizontal lines across screen):", border_rows)
