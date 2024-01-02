## System requirement

- Python3, pip
- google protobuf for python, six
```
pip3 install -r requirements.txt
```

### Full OTA

- ./extract.py --output_dir output/ payload.bin --partitions boot
- This will start to extract the images within the payload.bin file to the output folder you are in.

### Incremental OTA

- Copy original images (from full OTA or dumped from devices) to old folder
- ./extract.py --output_dir output/ --old_dir old/ payload.bin --partitions boot

NOTE: this has been fixed for Incremental updates.  Works as of 1/1/2024, tested on OnePlus 10 Pro.
