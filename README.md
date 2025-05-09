# `enpack.py`
将多个.psd按图层导出的素材分类入文件夹，或者按正则匹配的共有标题对文件进行分类入文件夹

# `label_resizer.py`

<details>
<summary>English</summary>

## Function
Resize DeepLabCut labeled datasets.  
If the `convertcsv2h5` feature is not enabled, the new dataset will be saved in the `labeled-data-resized` directory.  
If the `convertcsv2h5` feature is enabled, the original dataset will be renamed to `labeled-data-ori`, and the new dataset will be renamed to `labeled-data`.

## Usage
```
python label_resizer.py [parameters]
```

## Parameters
- `--label_path`: Path to labeled data, default is "./labeled-data"
- `--ratio`: Scaling ratio, default is 1
- `--width`: Specify width (pixels), default is -1 (not set)
- `--height`: Specify height (pixels), default is -1 (not set)
- `--dest_dir`: Output directory, default is "./labeled-data-resized"
- `--convertcsv2h5`: Whether to convert CSV to H5, options are "yes" or "no", default is "no"
- `--config_path`: DeepLabCut configuration file path, default is "./config.yaml"
<br>

- When `ratio` is specified and `width` and `height` are default: Scale images and annotation points proportionally
- When `width` is specified and `height` is default: Scale by width, height adjusts proportionally
- When `height` is specified and `width` is default: Scale by height, width adjusts proportionally
- When both `width` and `height` are specified: Scale to the specified dimensions

If you need to enable the `convertcsv2h5` feature, you must have `deeplabcut` installed in your environment.

## Warning
**Always backup your labeled data!**
</details>

## 功能
对DeepLabCut标注数据集进行尺寸缩放调整  
如果没有启用`convertcsv2h5`功能，新的数据集会保存在`labeled-data-resized`目录下  
如果启用`convertcsv2h5`功能，原来的数据集会重命名为`labeled-data-ori`，然后新的数据集会重命名为`labeled-data`

## 使用方法
```
python label_resizer.py [参数]
```

## 参数说明
- `--label_path`：标注数据路径，默认为"./labeled-data"
- `--ratio`：缩放比例，默认为1
- `--width`：指定宽度（像素），默认为-1（不设置）
- `--height`：指定高度（像素），默认为-1（不设置）
- `--dest_dir`：输出目录，默认为"./labeled-data-resized"
- `--convertcsv2h5`：是否将CSV转换为H5，可选"yes"或"no"，默认为"no"
- `--config_path`：DeepLabCut配置文件路径，默认为"./config.yaml"
<br>

- 指定`ratio`而`width`和`height`为默认值时：按比例缩放图像和标注点
- 指定`width`而`height`为默认值时：按宽度缩放，高度自动按比例调整
- 指定`height`而`width`为默认值时：按高度缩放，宽度自动按比例调整
- 同时指定`width`和`height`时：按指定尺寸缩放

如果需要启动`convertcsv2h5`功能，需要环境下安装有`deeplabcut`

## 警告
**总是备份标注好的数据！**