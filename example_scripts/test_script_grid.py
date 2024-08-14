# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:49:17 2022

@author: Kollarlab
"""
import os
import numpy as np

# replace with MaskMaker filepath
# os.chdir(r'C:\Users\Kollarlab\Documents\GitHub\MaskMaker') # is this the right way to do this

from mask import Chip, ChipBorder

from bondpad import Bondpad
from junction import Junction
from couplers.coupling_tee import CouplingStraight
from couplers.finger_cap import FingerCap
from couplers.gap_cap import GapCap
from couplers.tapered_cap import TaperedCap
from couplers.three_way_coupler import ThreeWayCoupler

from cpw.CPWBend import CPWBend
from cpw.CPWBendTaper import CPWBendTaper
from cpw.CPWStraight import CPWStraight

from resonators.lobed_ring import LobedRing

# from DrawCodes.CAD_codes.cpw.CPWLinearTaper import CPWLinearTaper

def startjunction(n):
    buffer = 1000
    spacing = 2500
    size = 7000
    N = (size - 2*buffer)/spacing + 1
    i_x = n % N
    i_y = np.floor(n/N).astype(int)
    # print([i_x,i_y])
    return Junction((buffer+i_x*spacing,buffer+i_y*spacing),90)

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

startjunc = startjunction(7)
cstraight3 = CouplingStraight(chip,startjunc=startjunc,settings={'coupling_gap':5*gapw_Z0,'updown':'up','leftright':'right'})
addStraights(chip,cstraight3)

startjunc = startjunction(8)
cstraight4 = CouplingStraight(chip,startjunc=startjunc,settings={'coupling_gap':5*gapw_Z0,'updown':'up','leftright':'left'})
addStraights(chip,cstraight4)

startjunc = startjunction(9)
cstraight5 = CouplingStraight(chip,startjunc=startjunc,settings={'coupling_gap':5*gapw_Z0,'updown':'down','leftright':'right'})
addStraights(chip,cstraight5)

startjunc = startjunction(10)
cstraight6 = CouplingStraight(chip,startjunc=startjunc,settings={'coupling_gap':5*gapw_Z0,'updown':'down','leftright':'left'})
addStraights(chip,cstraight6)

angle = 60
radius = 300
startjunc = startjunction(11)
taperbend1 = CPWBendTaper(chip,startjunc=startjunc,settings={'turn_angle':angle,'radius':radius,'stop_pinw':2*pinw_Z0,'stop_gapw':2*gapw_Z0})
CPWBend(chip,settings={'turn_angle':180-2*angle,'radius':radius,'pinw':2*pinw_Z0,'gapw':2*gapw_Z0})
taperbend2 = CPWBendTaper(chip,settings={'turn_angle':angle,'radius':radius,'start_pinw':2*pinw_Z0,'start_gapw':2*gapw_Z0})
CPWStraight(chip,settings = {'length':400}, startjunc = taperbend1.cxns['in'])
CPWStraight(chip,settings = {'length':400}, startjunc = taperbend2.cxns['out'])

startjunc = startjunction(15)
lobedring1 = LobedRing(chip,startjunc=startjunc)

#save
saveDir = r'Z:\Users\Theo\CAD'
filename = 'MM_settings_test.dxf'
chip.saveas(os.path.join(saveDir,filename))