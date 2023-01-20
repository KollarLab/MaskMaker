# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 18:01:38 2022

@author: Theo
"""
import os
import numpy as np

from mask import Chip

from junction import junction

from cpw.CPWStraight import CPWStraight
from qubits.example_qubit import ExampleQubit
from qubits.digitated_qubit import DigitatedQubit
from qubits.notch import QubitNotchFromJunc

chip = Chip(7000)

straight1 = CPWStraight(chip,settings={'length':2000},startjunc=junction((0,-1500),0))
QR = QubitNotchFromJunc(chip,settings={'refjunc':straight1.cxns['in'],'offset':20})
QL = QubitNotchFromJunc(chip,settings={'refjunc':straight1.cxns['out'],'offset':20})

straight2 = CPWStraight(chip,settings={'length':2000},startjunc=junction((0,0),0))
QR = ExampleQubit(chip,settings={'refjunc':straight2.cxns['in'],'offset':20})
QL = ExampleQubit(chip,settings={'refjunc':straight2.cxns['out'],'offset':20})

straight3 = CPWStraight(chip,settings={'length':2000},startjunc=junction((0,1500),0))
QR = DigitatedQubit(chip,settings={'refjunc':straight3.cxns['in'],'offset':20})
QL = DigitatedQubit(chip,settings={'refjunc':straight3.cxns['out'],'offset':20})

#save
# saveDir = r'Z:\Users\Theo\CAD'
filename = 'qubits_test.dxf'
chip.saveas(os.path.join(saveDir,filename))