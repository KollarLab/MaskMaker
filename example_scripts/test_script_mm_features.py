# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:49:17 2022

@author: Kollarlab
"""
import os

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

pinw_Z0 = 20
gapw_Z0 = 8.372

defaults = {}
defaults['pinw'] = pinw_Z0
defaults['gapw'] = gapw_Z0
defaults['radius'] = 100

defaults['FingerCap']['finger_length'] = 200

chip = Chip(7000)
chip.defaults = defaults

ChipBorder(chip)

startjunc1 = junction((1000,1000),0)

bondpad1 = Bondpad(chip, startjunc = startjunc1)
gapcap1 = GapCap(chip)
bondpad2 = Bondpad(chip, settings = {'bond_pad_length':700})

startjunc2 = junction((1000,2000),0)

bondpad3 = Bondpad(chip,startjunc=startjunc2)
tcap1 = TaperedCap(chip)
cstraight1 = CouplingStraight(chip)
threewaycap1 = ThreeWayCoupler(chip)

startjunc3 = threewaycap1.cxns['connC']
CPWStraight(chip,settings={'length':300},startjunc=startjunc3)
CPWBend(chip,settings={'turn_angle':90})
CPWStraight(chip,settings={'length':300})

startjunc4 = cstraight1.cxns['hanger']

CPWBend(chip,settings={'turn_angle':30},startjunc=startjunc4)
CPWStraight(chip,settings={'length':300})

startjunc5 = threewaycap1.cxns['connB']

CPWStraight(chip,settings={'length':300},startjunc=startjunc5)
fingercap1 = FingerCap(chip)
CPWStraight(chip,settings={'length':300})

#save
# saveDir = r'Z:\Users\Theo\CAD'
filename = 'mmv1_test.dxf'
chip.drawing.saveas(os.path.join(saveDir,filename))