# -*- coding: utf-8 -*-
# Convert from Yomi to Dic for Julius

import subprocess

subprocess.call(["sudo sh -c 'iconv -f utf8 -t eucjp julius.yomi | /home/pi/dictation-kit-v4.4/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl > julius.dic'"], shell=True)
