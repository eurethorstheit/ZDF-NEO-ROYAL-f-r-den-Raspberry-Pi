#!/usr/bin/env python3
# coding: utf8

import sys, os
import io
from subprocess import PIPE, Popen




URL = 'https://downloadzdf-a.akamaihd.net/mp4/zdf/16/12/161208_sendungroyale064vdf_nmg/2/161208_sendungroyale064vdf_nmg_476k_p9v13.mp4'

p = Popen(['wget', '--spider',URL], stderr = PIPE, stdin = PIPE, stdout = PIPE)

while p.poll() == None:
	output = p.stdout.readline()
	if output == '' and p.poll() is not None:
		break
	if output != "":
		print(output.strip())

