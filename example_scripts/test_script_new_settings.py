# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:49:17 2022

@author: Kollarlab
"""
import os
import numpy as np

# replace with MaskMaker filepath
os.chdir(r'Z:\MaskMaker') # is this the right way to do this

from mask import Chip, ChipBorder

from bondpad import Bondpad
from junction import junction
from couplers.coupling_tee import CouplingStraight
from couplers.finger_cap import FingerCap
from couplers.gap_cap import GapCap
from couplers.tapered_cap import TaperedCap
from couplers.three_way_coupler import ThreeWayCoupler

from cpw.CPWBend import CPWBend
from cpw.CPWStraight import CPWStraight

# from DrawCodes.CAD_codes.cpw.CPWLinearTaper import CPWLinearTaper

def startjunction(n):
    buffer = 1000
    spacing = 2500
    size = 7000
    N = (size - 2*buffer)/spacing + 1
    i_x = n % N
    i_y = np.floor(n/N).astype(int)
    # print([i_x,i_y])
    return junction((buffer+i_x*spacing,buffer+i_y*spacing),90)

def addStraights(structure,component):
    for key in component.cxns:
        CPWStraight(structure,settings = {'length':400}, startjunc = component.cxns[key])

pinw_Z0 = 20
gapw_Z0 = 8.372

defaults = {}
defaults['pinw'] = pinw_Z0
defaults['gapw'] = gapw_Z0
defaults['radius'] = 100

chip = Chip(7000)
chip.defaults = defaults

ChipBorder(chip)

startjunc = startjunction(0)
bondpad1 = Bondpad(chip,startjunc=startjunc)
addStraights(chip,bondpad1)

startjunc = startjunction(1)
cstraight1 = CouplingStraight(chip,startjunc=startjunc)
addStraights(chip,cstraight1)

startjunc = startjunction(2)
fcap1 = FingerCap(chip,startjunc=startjunc)
addStraights(chip,fcap1)

startjunc = startjunction(3)
gcap1 = GapCap(chip,startjunc=startjunc)
addStraights(chip,gcap1)

startjunc = startjunction(4)
tcap1 = TaperedCap(chip,startjunc=startjunc)
addStraights(chip,tcap1)

startjunc = startjunction(5)
twc1 = ThreeWayCoupler(chip,startjunc=startjunc)
addStraights(chip,twc1)

startjunc = startjunction(6)
cstraight2 = CouplingStraight(chip,startjunc=startjunc,settings={'coupling_gap':3*gapw_Z0,'updown':'up','leftright':'right'})
addStraights(chip,cstraight2)


#save
saveDir = r'Z:\Users\Theo\CAD'
filename = 'MM_settings_test.dxf'
chip.drawing.saveas(os.path.join(saveDir,filename))