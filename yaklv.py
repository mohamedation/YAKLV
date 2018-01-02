#!/usr/bin/python2
# coding=utf-8
############################################################################
#                                                                          #
#  Name:             Yet Another Kismet Log Viewer (YAKLV)                 #
#                                                                          #
#  Description:      YKLV accepts one or more Kismet XML log file(s) in a  #
#                    directory, and outputs human-readable HTML and/or CVS #
#                    file.                                                 #
#                    YKLV displays ESSID, Channel, BSSID, AP Manufacturer, #
#                    Minimum and Maximum Signal dbm.                       #
#                                                                          #
#  Usage:            ./yaklv.py -h                                         #
#                    ./yaklv.py /root/kismet-logs/                         #
#                    ./yaklv.py -o csv /root/kismet-logs/                  #
#                    ./yaklv.py -o html /root/kismet-logs/                 #
#                                                                          #
#  Requirements:     Python                                                #
#                    one or more Kismet .netxml log file(s)                #
#                                                                          #
#                                                                          #
#  Credits (legacy):                                                       #
#                    KLV V3                                                #
#                    Website: http://klv.professionallyevil.com (offline)  #
#                    KLV v2 Tool Released > post https://goo.gl/fMHhyR     #
#                    Author:  Nathan Sweaney - nathan@sweaney.com          #
#                    Date:   July 9, 2013                                  #
#                                                                          #
#                    KLV v3                                                #
#                    Website: https://github.com/illegalPointer            #
#                    Author: IllegalPointer                                #
#                    Date: Jun, 1, 2015                                    #
#                                                                          #
#  Credits:                                                                #
#                    YAKLV                                                 #
#                    Website: https://github.com/xxxxxxxxxxxxxx            #
#                    Author: Mohamedation                                  #
#                    Date: Jan, 1, 2018                                    #
#                                                                          #
############################################################################

import os
import sys
import datetime
import xml.etree.ElementTree as ET
import argparse
from argparse import RawTextHelpFormatter

#   useless junk that makes me feel good about myself
banner = """
    ██╗   ██╗ █████╗ ██╗  ██╗██╗    ██╗   ██╗
    ╚██╗ ██╔╝██╔══██╗██║ ██╔╝██║    ██║   ██║
     ╚████╔╝ ███████║█████╔╝ ██║    ██║   ██║
      ╚██╔╝  ██╔══██║██╔═██╗ ██║    ╚██╗ ██╔╝
       ██║   ██║  ██║██║  ██╗███████╗╚████╔╝
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═══╝
------------------------------------------------------"""
desc = """
Yet Another Kismet Log Viewer
Create a readable summary of Kismet XML files.

"""
#   variables
oui_file = open('oui.txt')
network_matrix = []
bssid_list = []
log_file_list = []
#   used on the HTML page output and file naming
now = datetime.datetime.now()
timestamp = now.strftime("%m-%d-%Y %H:%M:%S")

#   process command-line arguments
parser = argparse.ArgumentParser(description=banner + desc, formatter_class=RawTextHelpFormatter)
parser.add_argument('log_file_path', metavar='LogFilePath',
                   help='A directory containing one or more Kismet .netxml log files. KLV will process all .netxml files in the directory but will ignore all other files.')
parser.add_argument('-o', default="both", choices=['html', 'csv', 'both'],
                   help='Output format (default: both)')
parser.add_argument('-n', default="Kismet-Log-Summary",
                   help='Prefix for the output file(s).(default: Kismet-Log-Summary)')
args = parser.parse_args()
output_format = args.o
summaryFilename = args.n

#   add the ending slash in case it was left off
if args.log_file_path[-1:] <> "/":
   args.log_file_path = args.log_file_path + "/"

def main():
    print banner
#   cycle through each file in the directory
    files_in_dir = os.listdir(args.log_file_path)
    for file_in_dir in files_in_dir:
      if file_in_dir[-7:] == ".netxml":
         print "Adding log file(s): ", file_in_dir
         log_file_list.append(file_in_dir)
         xml_tree = ET.parse(args.log_file_path + file_in_dir)
         xml_root = xml_tree.getroot()
         # loop through each XML node of type "wireless-network"
         for network in xml_root.findall('wireless-network'):
            network_type = network.get('type')
#           ignoring probes right now
            if network_type <> 'probe':
               network_essid = ""
               network_encryption = ""
               network_bssid = ""
               network_manufacturer = ""
               network_min_signal_dbm = ""
               network_max_signal_dbm = ""
               network_min_signal_rssi = ""
               network_max_signal_rssi = ""
               network_oui = ""
               for network_detail in network:
#                 ESSID Info parsing
                  if network_detail.tag == 'SSID':
                     for child_network in network_detail:
                        if child_network.tag == 'essid':
                           if child_network.attrib.get("cloaked") == "true":
                              cloaked = "cloaked"
                           else:
                              cloaked = ""
                           if child_network.text is None:
                              network_essid = "" + cloaked
                           else:
                              network_essid = child_network.text + cloaked
#                       Encryption Info parsing
                        if child_network.tag == 'encryption':
                           network_encryption += child_network.text + '\n'
#                 BSSID Info parsing and matching with oui.txt
                  if network_detail.tag == 'BSSID':
                     network_bssid = network_detail.text
                     network_oui = network_bssid[0:2] + "-" + network_bssid[3:5] + "-" + network_bssid[6:8]
                     oui_file.seek(0)
                     for line in oui_file:
                        if network_oui in line:
                           network_manufacturer = line[18:]
                           break
#                 Channel Info parsing
                  elif network_detail.tag == 'channel':
                    network_channel = network_detail.text
#                 Signal Info parsing
                  if network_detail.tag == 'snr-info':
                     for child_network in network_detail:
                        if child_network.tag == 'min_signal_dbm':
                            network_min_signal_dbm += child_network.text
                        if child_network.tag == 'max_signal_dbm':
                            network_max_signal_dbm += child_network.text
               if network_bssid not in bssid_list:
                  bssid_list.append(network_bssid)
                  network_matrix.append([network_essid, network_channel, network_encryption, network_bssid, network_manufacturer, network_min_signal_dbm, network_max_signal_dbm])

    if output_format == 'both':
     create_html_file(network_matrix)
     create_csv_file(network_matrix)
     print "HTML and CSV Files Were Created Successfully."
    elif output_format == 'html':
     create_html_file(network_matrix)
     print "HTML File was Created Successfully."
    elif output_format == 'csv':
     create_csv_file(network_matrix)
     print "CSV File Was Created Successfully."

#  output to CSV
def create_csv_file(network_matrix):
   summary_file = open(summaryFilename+ '-' + timestamp + '.csv','w')
   summary_file.write("ESSID,Channel,Security,BSSID,Manufacturer,Min. DBM,Max. DBM\n")
   for network in network_matrix:
      summary_file.write(network[0] + ',' +network[1] + ',' +network[2].replace('\n', ' ') + ',' + network[3] +  ',' + '\"'  + network[4].replace('\n','') + '\"' + ',' + network[5] + ',' + network[6] + '\n')
   summary_file.close()

#  output to HTML
def create_html_file(network_matrix):
   summary_file = open(summaryFilename+ '-' + timestamp + '.html','w')

#  print header
   summary_file.write('<!DOCTYPE html>\n')
   summary_file.write('<html>\n')
   summary_file.write('  <head>\n')
   summary_file.write('    <title>Kismet Log Summary</title>\n')
   summary_file.write('  <style>\n')
   summary_file.write('  body {background-color: #010101; font-family: "sans-serif"; color: white;}\n')
   summary_file.write('  table {background-color: #010101; font-size: 0.75em; border: 0; width:100%;} th, td {padding: 5px; text-align: center;} tr:nth-child(even) {background-color: #0a0a0a;} tr:hover {background-color:#010f19;} #t-header {text-align: left; font-size: 1.25em; color: white; font-weight: 500; } #timestamp {text-align: right;} #footer {text-align: center; color: white; font-size: 0.65em;} #footer a, #footer a:visited {text-decoration: none; color: #4DB8FF;} \n')
   summary_file.write('  </style>\n')
   summary_file.write('  </head>\n')
   summary_file.write('  <body>\n')
   summary_file.write('    <table>\n')
   summary_file.write('      <tr>\n')
   summary_file.write('        <td id="t-header" colspan=6>Kismet Log Summary</td>\n')
   summary_file.write('        <td id="timestamp" colspan=2>Created: ' + timestamp + '</font></td>\n')
   summary_file.write('      </tr>\n')
   summary_file.write('      <tr>\n')
   summary_file.write('        <th></th>\n')
   summary_file.write('        <th>Name (ESSID)</th>\n')
   summary_file.write('        <th>Channel</th>\n')
   summary_file.write('        <th>Security</th>\n')
   summary_file.write('        <th>BSSID</th>\n')
   summary_file.write('        <th>Manufacturer</th>\n')
   summary_file.write('        <th>Min. DBM</th>\n')
   summary_file.write('        <th>Max. DBM</th>\n')
   summary_file.write('      </tr>\n')

#  print kismet data
   row_toggle = 1
   row = 1
   for network in network_matrix:
      summary_file.write('        <td>' + str(row) + '</td>\n')
      summary_file.write('        <td>' + network[0] + '</td>\n')
      summary_file.write('        <td>' + network[1] + '</td>\n')
      summary_file.write('        <td>' + network[2] + '</td>\n')
      summary_file.write('        <td>' + network[3] + '</td>\n')
      summary_file.write('        <td>' + network[4] + '</td>\n')
      summary_file.write('        <td>' + network[5] + '<br /></td>\n')
      summary_file.write('        <td>' + network[6] + '<br /></td>\n')
      summary_file.write('      </tr>\n')
      row += 1
   summary_file.write('    </table>\n')
   summary_file.write('<br />\n')

   # print list of log files
   summary_file.write('    <table>\n')
   summary_file.write('      <tr>\n')
   summary_file.write('        <td>Log files included:</td>\n')
   summary_file.write('      </tr>\n')
   row_toggle = 1
   for log_file in log_file_list:
     summary_file.write('        <td>' + log_file + '</td>\n')
   summary_file.write('    </table>\n')

   # print footer
   summary_file.write('<br />\n')
   summary_file.write('    <div id="footer">\n')
   summary_file.write('        Yet Another Kismet Log Viewr - written by <a href="https://twitter.com/mohamedation">mohamedation</a>\n')
   summary_file.write('    </div>\n')
   summary_file.write('  </body>\n')
   summary_file.write('</html>\n')
   summary_file.close()


main()


"""
Todo:
* add client data
  - To start, just summarize the number of clients for each network.
* add packet data
  - Count of packets seen on each network
* add options for sorting
* allow input of specific files, not just a folder
* gracefully handle missing oui.txt file
* gracefully handle no .netxml files
* download updated oui.txt file?
"""
