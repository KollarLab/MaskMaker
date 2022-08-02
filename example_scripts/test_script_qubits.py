# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 18:01:38 2022

@author: Theo
"""
import os
import numpy as np

# os.chdir(r'C:\Users\Theo\Documents\GitHub\MaskMaker')

from mask import Chip, ChipBorder

from junction import junction

from cpw.CPWStraight import CPWStraight
from qubits.example_qubit import ExampleQubit
from qubits.sawtooth_qubit import SawtoothQubit

# from DrawCodes.CAD_codes.cpw.CPWLinearTaper import CPWLinearTaper

chip = Chip(7000)

straight1 = CPWStraight(chip,settings={'length':600},startjunc=junction((0,0),45))
QR = ExampleQubit(chip,settings={'refjunc':straight1.cxns['in']})
QL = ExampleQubit(chip,settings={'refjunc':straight1.cxns['out']})

straight1 = CPWStraight(chip,settings={'length':2000},startjunc=junction((0,500),45))
QR = SawtoothQubit(chip,settings={'refjunc':straight1.cxns['in']})
QL = SawtoothQubit(chip,settings={'refjunc':straight1.cxns['out']})
"""
general structure for adding qubits:

 -- name each straight, perhaps prepare in a list?
 -- add a qubit to each straight ? this seems ugly

"""
#save
saveDir = r'Z:\Users\Theo\CAD'
filename = 'qubits_test.dxf'
chip.drawing.saveas(os.path.join(saveDir,filename))