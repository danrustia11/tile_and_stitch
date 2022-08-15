# tile_and_stitch

### Clone the repo

```
https://github.com/danrustia11/tile_and_stitch
```

### Sample usage

```
import tools.image_tiler as tl
import cv2

# Define a tiler object

tiler = tl.tiler(TILING_SIZE, PADDING)

# Open an image

image = cv2.imread([filename])

# Remove the borders from the image to make it fit for tiling

no_border_image = tiler.remove_borders(image)

# Apply tiling

tiled_images = tiler.tile_image(no_border_image)
```

### Preparing data using the library

Prepares images with cut borders (fit for tiling) and tiled images. Labels are also retranslated based on the tiled output images.

Script name: <br><b>1_data_preparation.py</b> <br><br>

| Arg       | Input  | Description                                                                           |
| --------- | ------ | ------------------------------------------------------------------------------------- |
| --dir     | string | Source image directory                                                                |
| --split   | string | Percentage of train, validation, and test                                             |
| --tile    | int    | Tiliing size                                                                          |
| --padding | int    | Padding size (overlap)                                                                |
| --verbose | int    | To print system messages or not (0 or 1)                                              |
| --density | string | Divides the images into low, medium, and high counts; ignored if no input is provided |

<b>If without labels:</b><br>

<code>python 1_data_preparation.py --dir [directory_name] --tile 1200 --padding 200</code>

<b>If with labels:</b><br>

[With density splitting]<br>
`python 1_data_preparation.py --dir [directory_name] --tile 1200 --padding 200 --density 10,30`

[Without density splitting]<br>
`python 1_data_preparation.py --dir [directory_name] --tile 1200 --padding 200`
