# tile_and_stitch

### 1. Clone the repo:

```
https://github.com/danrustia11/tile_and_stitch
```

### 2. Data preparation

Prepares images with cut borders (fit for tiling) and tiled images. Labels are also retranslated based on the tiled output images.

Script name: 1_data_preparation.py <br>
Args: <br>
--dir [string] <br>
Source image directory <br>
--split [list] <br>
Percentage of train, validation, and test <br>
--tile [int] <br>
Tiliing size <br>
--padding [int] <br>
Padding size (overlap) <br>
--verbose [int] <br>
To print system messages or not (0 or 1) <br>
--density [string] <br>
Divides the images into low, medium, and high counts. Does not work if no input is provided. <br>
Example: 10,30 (divides the images into LOW: c<10, MEDIUM: 10>=c>=30, HIGH: 30>c, where c is the count) <br>

<b>If without labels:</b><br>

`python 1_data_preparation.py --dir [directory_name] --tile 1200 --padding 200`

<b>If with labels:</b><br>

[With density splitting]<br>
`python 1_data_preparation.py --dir [directory_name] --tile 1200 --padding 200 --density 10,30`

[Without density splitting]<br>
`python 1_data_preparation.py --dir [directory_name] --tile 1200 --padding 200`
