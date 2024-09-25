import os
import glob

pattern = './apps/*/migrations/*.py'
pattern2 = './apps/*/migrations/__pycache__/*.pyc'
pattern3 = './apps/*/migrations/__pycache__'

for fname in glob.glob(pattern, recursive=True):
    if os.path.isfile(fname) and not "__init__.py" in fname:
        print(fname)
        os.remove(fname)
    

for fname2 in glob.glob(pattern2, recursive=True):
    if os.path.isfile(fname2) and not "__init__.cpython-310.pyc" in fname2:
        print(fname2)
        os.remove(fname2)


for fname3 in glob.glob(pattern3, recursive=True):
    if os.path.isdir(fname3):
        print(fname3)
        os.remove(fname3)

# allResults = glob.glob(pattern, recursive=True)
# filteredResults = [r for r in allResults if not "__init__" in r]
# print(filteredResults)