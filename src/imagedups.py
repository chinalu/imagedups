#!python
import argparse
from PIL import Image
import os
import sys
import imagehash
import progressbar


def dupes(config):
    hmap = {}
    paths = config['paths']
    allpaths = []
    if config['recurse']:
        for path in paths:
            for root, dirs, _ in os.walk(path):
                for name in dirs:
                    allpaths.append(os.path.join(root, name))
    paths += allpaths
    files = []
    for path in paths:
        fs = os.listdir(path)
        for f in fs:
            fpath = os.path.join(path, f)
            if os.path.isdir(fpath):
                continue
            files.append(fpath)
    file_num = len(files)
    pbar = progressbar.ProgressBar(max_value=file_num)
    for i, fpath in enumerate(files):
        try:
            pbar.update(i)
            h = imagehash.average_hash(Image.open(fpath))
            h = "%s" % h
            sims = hmap.get(h, [])
            sims.append(fpath)
            hmap[h] = sims
        except Exception as e:
            # print(e)
            pass
    pbar.finish()
    
    for k, v in hmap.items():
        if len(v) == 1:
            continue
        for idx, fpath in enumerate(v):
            if idx == 0:
                if not config['quiet']:
                    print("[+]", fpath, os.path.getsize(fpath))
            else:
                if not config['quiet']:
                    print("[-]", fpath, os.path.getsize(fpath))

                confirm = config['noprompt']
                if not config['noprompt'] and config['delete']:
                    print("Delete %s? [y/n]")
                    confirm = sys.stdin.readline().strip() == 'y'
                if config['delete'] and confirm:
                    os.unlink(fpath)
        if not config['quiet']:            
            print()

    

def main(args=None):
    '''
    Usage: fdupes [options] DIRECTORY...

 -r --recurse            for every directory given follow subdirectories
                         encountered within
 -R --recurse:           for each directory given after this option follow
                         subdirectories encountered within (note the ':' at the
                         end of the option, manpage for more details)
 -s --symlinks           follow symlinks
 -H --hardlinks          normally, when two or more files point to the same
                         disk area they are treated as non-duplicates; this
                         option will change this behavior
 -G --minsize=SIZE       consider only files greater than or equal to SIZE bytes
 -L --maxsize=SIZE       consider only files less than or equal to SIZE bytes
 -n --noempty            exclude zero-length files from consideration
 -A --nohidden           exclude hidden files from consideration
 -f --omitfirst          omit the first file in each set of matches
 -1 --sameline           list each set of matches on a single line
 -S --size               show size of duplicate files
 -t --time               show modification time of duplicate files
 -m --summarize          summarize dupe information
 -q --quiet              hide progress indicator
 -d --delete             prompt user for files to preserve and delete all
                         others; important: under particular circumstances,
                         data may be lost when using this option together
                         with -s or --symlinks, or when specifying a
                         particular directory more than once; refer to the
                         fdupes documentation for additional information
 -P --plain              with --delete, use line-based prompt (as with older
                         versions of fdupes) instead of screen-mode interface
 -N --noprompt           together with --delete, preserve the first file in
                         each set of duplicates and delete the rest without
                         prompting the user
 -I --immediate          delete duplicates as they are encountered, without
                         grouping into sets; implies --noprompt
 -p --permissions        don't consider files with different owner/group or
                         permission bits as duplicates
 -o --order=BY           select sort order for output and deleting; by file
                         modification time (BY='time'; default), status
                         change time (BY='ctime'), or filename (BY='name')
 -l --log=LOGFILE        log file deletion choices to LOGFILE
 -v --version            display fdupes version
 -h --help               display this help message

    '''
    parser = argparse.ArgumentParser(
        prog="imagedups",
        description="""Find/Delete duplicated images
    
  imagedups [options] -p DIRECTORY...
        """,
        epilog="""
  inspire by fdupes
    """, formatter_class=argparse.RawDescriptionHelpFormatter)
    
    # submain = parser.add_argument_group('Usage: imagedups [options] DIRECTORY...')
    parser.add_argument('-d', '--delete', dest='delete', default=False, action='store_true', 
                            help='Delete duplicated files, keep one image only')
    parser.add_argument('-r', '--recurse', dest='recurse', default=False, action='store_true', 
                            help='For every directory given follow subdirectories encountered within')
    parser.add_argument('-N', '--noprompt', dest='noprompt', default=False, action='store_true', 
                            help='''Together with --delete, preserve the first file in
each set of duplicates and delete the rest without
prompting the user
                            ''')
    parser.add_argument('-q', '--quiet', dest='quiet', default=False, action='store_true', 
                            help='Hide progress indicator')
    parser.add_argument('--minsize', dest='minsize', type=int,
                            help='Consider only files greater than or equal to SIZE bytes')
    parser.add_argument('--maxsize', dest='maxsize', type=int,
                            help='Consider only files less than or equal to SIZE bytes')
    parser.add_argument('-p', '--path', dest='paths', nargs='+', type=str, required=True)

    # submain.add_argument('--image_dim', dest='image_dim', type=int,
                            # help="The square dimension of the model's input shape")
    if args is not None:
        config = vars(parser.parse_args(args))
    else:
        config = vars(parser.parse_args())
    
    dupes(config)
    # if config['image_source'] is None or not exists(config['image_source']):
    # 	raise ValueError("image_source must be a valid directory with images or a single image to classify.")
    


if __name__ == '__main__':
    main()

