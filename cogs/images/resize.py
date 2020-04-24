import os
import cv2


def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # Grab the image size and initialize dimensions
    dim = None
    (h, w) = image.shape[:2]

    # Return original image if no need to resize
    if width is None and height is None:
        return image

    # We are resizing height if width is none
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # We are resizing width if height is none
    else:
        # Calculate the ratio of the width and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Return the resized image
    return cv2.resize(image, dim, interpolation=inter)


for file in os.listdir("/Users/leonbowie/Documents/Obsidion/cogs/images/effect"):
    if file.endswith(".png"):
        # Resizes a image and maintains aspect ratio
        image = cv2.imread(
            f"/Users/leonbowie/Documents/Obsidion/cogs/images/effect/{file}"
        )
        image = maintain_aspect_ratio_resize(image, width=512)
        cv2.imwrite(
            f"/Users/leonbowie/Documents/Obsidion/cogs/images/effect/{file}", image
        )
