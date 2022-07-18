# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 17:19:21 2022

@author: Kollarlab
"""

class Component:
    """
    
    base class for all components
    
    Component:
        Arguments:
            structure: Chip to which Component belongs to
            comp_key: string key for Chip.defaults corresponding to the component (ex:'Bondpad')
            global_keys: list of string keys for Chip.defaults to replace object_keys
            object_keys: list of string keys for Component._settings corresponding to global_keys
            settings: dictionary of custom settings for Component instance
        Attributes:
            _defaults: dictionary of component-level defaults
    
    Subclass level (not required):
        Arguments:
            startjunc: starting position and direction, a junction
            cxn_names: array of names for connection points
        Attributes:
            cxns: dictionary of connection points to object
    
    There are four levels of defaults, as seen in the line where
    self.settings is assigned. In order of precedence, where the Bondpad
    class is used as an example:
        (1) settings passed in a dictionary as an argument of
            Component.__init__
        (2) mask level defaults for the component set in a dictionary at 
            Chip.defaults['<Component_name>']
        (3) mask level defaults for all components set in
            Chip.defaults[global_keys[n]].     
                -- value of Component.settings[object_keys[n]]] is replaced by
                   value of Chip.defaults[global_keys[n]]
                -- mask level defaults (entries of global_keys) include
                   ['pinw'.'gapw','radius']
        (4) Component level defaults stored in Component._defaults
        
    Any settings not found in (1) will be filled in by (2), and then any
    settings still missing will be filled in by (3), and then by (4).
    
    """
    def __init__(self,structure,comp_key,global_keys,object_keys,settings):
        
        s = structure
        
        global_defaults = {}
        for n in range(len(global_keys)):
            if global_keys[n] in s.defaults:
                global_defaults[object_keys[n]] = s.defaults[global_keys[n]]
        
        if comp_key in s.defaults:
            chip_defaults = s.defaults[comp_key]
        else:
            chip_defaults = {}
            
        """                     (4)                (3)              (2)            (1)                     """                    
        self.settings = {**self._defaults, **global_defaults, **chip_defaults, **settings} # fill in defaults
       
        self.set_settings()
        
    def set_settings(self):
        for key in self.settings.keys():
            self.__setattr__(key, self.settings[key])