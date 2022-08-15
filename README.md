# tile_and_stitch

### 1. Clone the repo:

```
https://github.com/danrustia11/tile_and_stitch
```

### 2. Data preparation

Prepares images with cut borders (fit for tiling) and tiled images. Labels are also retranslated based on the tiled output images.

Script name: 1_data_preparation.py
Args:
--dir <string>
Source image directory
--split <list>
Percentage of train, validation, and test
--tile <int>
Tiliing size
--padding <int>
Padding size (overlap)
--verbose <int>
To print system messages or not (0 or 1)
--density <string>
Divides the images into low, medium, and high counts. Does not work if no input is provided.
Example: 10,30 (divides the images into LOW: c<10, MEDIUM: 10>=c>=30, HIGH: 30>c, where c is the count)

# If without labels:

`python 1_data_preparation.py --dir E:\Research_data\2022_WA\base --tile 1200 --padding 200`

# If with labels:

[With density splitting]
`python 1_data_preparation.py --dir "E:\Research_data\2022_CEA_B\base\train and validation" --tile 1200 --padding 200 --density 10,30`

[Without density splitting]
`python 1_data_preparation.py --dir "E:\Research_data\2022_CEA_B\base\train and validation" --tile 1200 --padding 200`
