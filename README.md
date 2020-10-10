# imagedups
Find/Delete duplicated images

## Install 
python setup.py install

## Usage

1. Show duplicated files:

   ```shell
   imagedups -p /path/to/image/folder
   ```

2. Recursively show duplicated files, use param -r:

   ```shell
   imagedups -r -p /path/to/image/folder
   ```

3. Delete duplicated file with prompt, use param -d:

   ```shell
   imagedups -r -d -p /path/to/image/folder
   ```

4. Delete duplicated file without prompt, add param `-N`:

   ```shell
   imagedups -r -d -N -p /path/to/image/folder
   ```
   
   Caution: *You should backup files incase data loss*


