# Ghoul-Craver
Simple Python file carver that recovers any file type you give as example.

### Features
- Universal: feed it one file → it learns start/end signatures → recovers all identical files
- Pure Python, no dependencies
- Fast block-by-block scan

### Usage
```bash

🞈 python gh0ulcarver.py
Usage:
 python gh0ulcarver.py --select               # interactive menu
 python gh0ulcarver.py --demo                 # show signature and carve that filetype
 python gh0ulcarver.py --help                 # show this help

Recommended to run: python gh0ulcarver.py --demo
```
### Quick Example

```bash
🞈 sudo python gh0ulcarver.py --demo
Gimme an example file to recover: /home/cyb3rgh0u1/Downloads/Frame-G3.png

Detected: PNG
        start: b'\x89PNG\r\n\x1a\n'
        end:   b'\x60\x82'

Enter the drive or image path to scan: /dev/sdb
Enter the output folder (must end with /): /home/cyb3rgh0u1/Public/Temp/


=============== Found PNG at location:0xf20000 ===============
=============== Wrote PNG to location: 0.png ===============

=============== Found PNG at location:0xf392c8 ===============
=============== Wrote PNG to location: 1.png ===============

=============== Found PNG at location:0xf4efc0 ===============
=============== Wrote PNG to location: 2.png ===============
```
### Requirements

- Python 3
- sudo for raw devices (/dev/sd*)

Feed it a file, watch it rise from the dead.


