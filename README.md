Hobbyking LiPo Compare
======================

Parses all the LiPo batteries available on Hobbyking, either from the Global or US (West) Warehouse
Works with both python 2 and 3

## Dependencies
python requests (http://docs.python-requests.org/)
python lxml (http://lxml.de/)
### On Debian (or variants)
#### Python 2
```Shell
sudo aptitude update
sudo aptitude install python-requests python-lxml
```
#### Python 3
```Shell
sudo aptitude update
sudo aptitude install python3-requests python3-lxml
```

## Usage
1. Download however you would like, git clone, zip, etc
2. `cd` into the directory
3. Run with `./lipoCompare.py` or `python3 lipoCompare.py`\`python2 lipoCompare.py`

It will print out the top 20 Wh/$ batteries, to change this the `processData()` function would need to be tweaked

Running without the `getData()` function call commented out will fetch and save all of the data into a python shelve.  Subsequent runs can have `getData()` commented out with just `processData()` to display everything, unless Hobbyking's listings have changed then you will want to refetch all of the battery data with `getData()`

Setting `us=True` to `us=False` will cause this to get the Global Warehouse prices, which are cheaper but shipping is usually more.
