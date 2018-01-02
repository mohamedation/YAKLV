```python
██╗   ██╗ █████╗ ██╗  ██╗██╗    ██╗   ██╗
╚██╗ ██╔╝██╔══██╗██║ ██╔╝██║    ██║   ██║
 ╚████╔╝ ███████║█████╔╝ ██║    ██║   ██║
  ╚██╔╝  ██╔══██║██╔═██╗ ██║    ╚██╗ ██╔╝
   ██║   ██║  ██║██║  ██╗███████╗╚████╔╝
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═══╝
Create a readable summary of Kismet XML files
```
<p align="left">
<img src="https://img.shields.io/badge/Python-2-yellow.svg"></a>
</p>

# Yet Another Kismet Log Viewer
+ Accepts one or more Kismet XML log file(s) in a directory.
+ Outputs Human-Readable HTML and/or CVS file(s).
+ Displays ESSID, Channel, BSSID, AP Manufacturer based on BSSID, Minimum, and Maximum Signal dbm.
+ Can be easily configured to parse and output more data from Kismet XML.
+ Outputs both HTML and CSV by default with option to output only one of them.
+ Output Files are timestamped (Doesn't overwrite old files) and You can change the prefix.
+ OUi file (BSSID Manufacturers) is updated and smaller in size.

### Improved HTML output
+ Dark style.
+ Improved overall HTML code.
<img src="https://github.com/mohamedation/YAKLV/blob/master/yaklv-html.png">

### Usage
#### Requirements
* Python 2
* One or more Kismet .netxml log file(s)

```python
./yaklv [argument(s)] [path to log file(s) directory]
```

-h, --help          show help

-o {html,csv,both}  Output format (default: both)

-n N                Prefix for the output file(s).(default: Kismet-Log-Summary)

### Credits (legacy):
#### KLV V3
Website: http://klv.professionallyevil.com (offline)

KLV v2 Tool Released > post https://goo.gl/fMHhyR

Author:  Nathan Sweaney - nathan@sweaney.com

Date:   July 9, 2013

#### KLV v3
Website: https://github.com/illegalPointer

Author: @IllegalPointer

Date: Jun, 1, 2015
