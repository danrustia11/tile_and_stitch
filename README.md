# tile_and_stitch

### 1. Clone the repo:

```
https://github.com/danrustia11/tile_and_stitch
```

### 2. Data preparation

Prepares images with cut borders (fit for tiling) and tiled images. Labels are also retranslated based on the tiled output images.

# If without labels:

`python 1_data_preparation.py --dir E:\Research_data\2022_WA\base --tile 1200 --padding 200`

# If with labels:

# [With density splitting]

`python 1_data_preparation.py --dir "E:\Research_data\2022_CEA_B\base\train and validation" --tile 1200 --padding 200 --density 10,30`

# [Without density splitting]

`python 1_data_preparation.py --dir "E:\Research_data\2022_CEA_B\base\train and validation" --tile 1200 --padding 200`
