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
    subdirs = []
    if config['recurse']:
        for path in paths:
            for root, dirs, _ in os.walk(path):
                for name in dirs:
                    subdirs.append(os.path.join(root, name))
    paths += subdirs
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
    parser = argparse.ArgumentParser(
        prog="imagedups",
        description="""Find/Delete duplicated images
    
  imagedups [options] -p DIRECTORY...
        """,
        epilog="""
  inspire by fdupes
    """, formatter_class=argparse.RawDescriptionHelpFormatter)
    
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

    if args is not None:
        config = vars(parser.parse_args(args))
    else:
        config = vars(parser.parse_args())
    
    dupes(config)
    
if __name__ == '__main__':
    main()