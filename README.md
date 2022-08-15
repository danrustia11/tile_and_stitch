# tile_and_stitch

### 1. Clone the repo:

```
https://github.com/danrustia11/tile_and_stitch
```

### 2. Data preparation

Prepares images with cut borders (fit for tiling) and tiled images. Labels are also retranslated based on the tiled output images.

Script name: <br><b>1_data_preparation.py</b> <br><br>

| Arg       | Input  | Description                                                                           |
| --------- | ------ | ------------------------------------------------------------------------------------- |
| --dir     | string | Source image directory                                                                |
| --split   | string | Percentage of train, validation, and test                                             |
| --tile    | string | Tiliing size                                                                          |
| --padding | string | Padding size (overlap)                                                                |
| --verbose | string | To print system messages or not (0 or 1)                                              |
| --density | string | Divides the images into low, medium, and high counts; ignored if no input is provided |

<b>If without labels:</b><br>

`python 1_data_preparation.py --dir [directory_name] --tile 1200 --padding 200`

<b>If with labels:</b><br>

[With density splitting]<br>
`python 1_data_preparation.py --dir [directory_name] --tile 1200 --padding 200 --density 10,30`

[Without density splitting]<br>
`python 1_data_preparation.py --dir [directory_name] --tile 1200 --padding 200`
