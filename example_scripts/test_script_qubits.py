# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 18:01:38 2022

@author: Theo
"""
import os
import numpy as np

os.chdir(r'C:\Users\Theo\Documents\GitHub\MaskMaker')

from mask import Chip, ChipBorder

from junction import junction

from cpw.CPWStraight import CPWStraight
from qubits.example_qubit import ExampleQubit

# from DrawCodes.CAD_codes.cpw.CPWLinearTaper import CPWLinearTaper

chip = Chip(7000)

straight1 = CPWStraight(chip,settings={'length':600},startjunc=junction((0,0),45))
QR = ExampleQubit(chip,settings={'refjunc':straight1.cxns['in']})
QL = ExampleQubit(chip,settings={'refjunc':straight1.cxns['out']})

#save
saveDir = r'C:\Users\Theo\Documents\Kollar Lab Files\CAD'
filename = 'qubits_test.dxf'
chip.drawing.saveas(os.path.join(saveDir,filename))