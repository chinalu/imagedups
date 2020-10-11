# imagedups
查找/删除相同的图片文件

## 开发背景

在进行图片分类的机器学习时，收集整理数据是一个必不可少的步骤。但是在使用fdupes进行文件去重时，发现很多看起来一样的图片，实际上二进制文件是不一样的。所以开发一个小程序，根据imagehash，计算图片的average_hash是否一致。如果一致，则认为文件是相同的。 

## 安装 
python setup.py install

## 使用方法

1. 仅显示重复的图片:

   ```shell
   imagedups -p /path/to/image/folder1  
   ```

   [+]开头的文件是保留的文件；

   [-]开头的文件是可以清理的文件。

2. 递归查找文件：

   ```shell
   imagedups -r -p /path/to/image/folder
   ```

3. 查找并删除文件:

   ```shell
   imagedups -r -d -p /path/to/image/folder
   ```

4. 删除文件是不进行确认:

   ```shell
   imagedups -r -d -N -p /path/to/image/folder
   ```

   请做好数据备份
