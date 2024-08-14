# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 11:19:49 2022

@author: Kollarlab
"""

import os
import numpy as np

# replace with MaskMaker filepath
# os.chdir(r"C:\Users\KollarLab\Documents\GitHub\MaskMaker")

from mask import Chip, ChipBorder

from bondpad import Bondpad
from junction import Junction
from couplers.coupling_tee import CouplingStraight
from cpw.CPWBend import CPWBend
from cpw.CPWStraight import CPWStraight

# from DrawCodes.CAD_codes.cpw.CPWLinearTaper import CPWLinearTaper

pinw_Z0 = 20
gapw_Z0 = 8.372

defaults = {}
defaults['pinw'] = pinw_Z0
defaults['gapw'] = gapw_Z0
defaults['radius'] = 100

chip = Chip(7000)
chip.defaults = defaults

ChipBorder(chip)

# feedline could be optimized into another Component, with cxns at each hanger
feedline_start = Junction((1200,1800),90)
coupling_straight_length = CouplingStraight._defaults['length']
feedline_height = 4100
feedline_width = 4560
feedline_straight_length_nom = ((feedline_height-100)/4 - coupling_straight_length)/2
cstraight = []

def feedline_unit(lr,ud):
    CPWStraight(chip,settings={'length':feedline_straight_length_nom-200})
    cstraight.append(CouplingStraight(chip,settings={'leftright':lr,'updown':ud}))
    CPWStraight(chip,settings={'length':feedline_straight_length_nom+200})
    
bondpad_in = Bondpad(chip,startjunc=feedline_start)

for _ in range(4):
    feedline_unit('right','down')

CPWBend(chip,settings={'turn_angle':-90})
CPWStraight(chip,settings={'length':feedline_width-200})
CPWBend(chip,settings={'turn_angle':-90})

for _ in range(4):
    feedline_unit('right','up')

bondpad_out = Bondpad(chip)

# this is the much faster bit
resonator_ns = [8, 1, 5, 4, 7, 2, 6, 3]
for i in range(len(cstraight)):
    startjunc = cstraight[i].cxns['hanger']
    CPWStraight(chip,startjunc=startjunc,settings={'length':1000+1000*resonator_ns[i]/8})
# if the line above this was replaced by a call to a resonator Component that
# took some index to determine its parameters, you can see how this would save
# a lot of time

saveDir = r'Z:\Users\Theo\CAD'
filename = 'example_resonator_chip.dxf'
chip.saveas(os.path.join(saveDir,filename))