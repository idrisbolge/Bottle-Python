#!/usr/bin/env python
# -*-coding:utf-8-*-

import subprocess


def Runcommand(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    p = p.decode("utf-8")
    return p


def DiskUsage():
    mesaj = Runcommand("df -h").replace("Bağlanılan yer", "bağlanılanyer").split()
    tablo = ""
    sonuc = int(len(mesaj) / 6)
    i = 0
    while i <= sonuc - 1:
        tablo += "<tr><th>%s</th>   <th>%s</th> <th>%s</th> <th>%s</th> <th>%s</th> <th>%s</th> </tr>" \
                 % (mesaj[i * 6 + 0], mesaj[i * 6 + 1], mesaj[i * 6 + 2], mesaj[i * 6 + 3], mesaj[i * 6 + 4],
                    mesaj[i * 6 + 5])
        i += 1
    return tablo


def routeTable():
    mesaj = Runcommand("route -n").replace("Kernel IP routing table", "").split()
    tablo = ""
    sonuc = int(len(mesaj) / 8)
    i = 0
    while i < sonuc:
        tablo += "<tr><th>%s</th>   <th>%s</th> <th>%s</th> <th>%s</th> <th>%s</th> <th>%s</th> <th>%s</th> <th>%s</th></tr>" \
                 % (mesaj[i * 8 + 0], mesaj[i * 8 + 1], mesaj[i * 8 + 2], mesaj[i * 8 + 3], mesaj[i * 8 + 4],
                    mesaj[i * 8 + 5], mesaj[i * 8 + 6], mesaj[i * 8 + 7])
        i += 1
    return tablo


ModemStats = [
    {'Name': 'uptime', 'result': Runcommand('uptime')},
    {'Name': 'ip', 'result': Runcommand("ifconfig wlp2s0 | grep netmask | awk '{ print $2}'")},
    {'Name': 'disk usage', 'result': DiskUsage()},
    {'Name': 'route table', 'result': routeTable()},
    {'Name': 'imei', 'result': "imei"},
    {'Name': 'signalStraght', 'result': "Signal Straght"},
    {'Name': 'lacinfo', 'result': "Lac Info"},
    {'Name': 'DataUsage', 'result': Runcommand("ifconfig |grep -i rx")}
]
