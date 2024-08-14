# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 15:16:25 2023

@author: Kollarlab
"""
import os

from qubits.custom_qubit import CustomQubit
from cpw.CPWStraight import CPWStraight
from junction import Junction
from mask import Chip
from import_dxf import ImportedDXF

chip = Chip(7000)


straight1 = CPWStraight(chip,settings={'length':2000},startjunc=Junction((0,-500),0))

martin_path = r'Z:\Users\Theo\CAD\martins_stolen_qubit.dxf'
round_path = r'Z:\Users\Theo\CAD\rounded_qubit.dxf'

qubit_h = 52
qubit_l = 548
qubit_settings = {}
qubit_settings['height'] = 80
qubit_settings['taper_angle'] = 60 # (0-90]
qubit_settings['length'] = 700
qubit_settings['leftright'] = 'right'
qubit_settings['notch_offset'] = 20
qubit_settings['import_offset'] = (qubit_settings['length']-qubit_l)/2

qubit_settings['qubit_path'] = martin_path


qubit_settings['refjunc'] = straight1.cxns['in']
QR = CustomQubit(chip,settings=qubit_settings)

qubit_settings['refjunc'] = straight1.cxns['out']
QL = CustomQubit(chip,settings=qubit_settings)

ImportedDXF(chip,settings={'dxf_path':round_path,'offset':(100,0)})
ImportedDXF(chip,settings={'dxf_path':round_path,'offset':(-100,0),'xscale':-1})
ImportedDXF(chip,settings={'dxf_path':round_path,'offset':(0,100),'xscale':10,'yscale':10,'rotation':15})

saveDir = r'Z:\Users\Theo\CAD'
filename = 'custom_qubits.dxf'
chip.saveas(os.path.join(saveDir,filename))