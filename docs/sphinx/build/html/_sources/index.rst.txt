=======================
MaskMaker documentation
=======================
This site contains the documentation for Kollar Lab's scripts used to create and simulate chips.

Source Files
============
The following four directories, **couplers**, **cpw**, **qubits**, and **resonators** contain all of the basic building blocks
of a chip. Each directory contains several variations of each component, all with different use cases. 


.. autosummary::
   :toctree: couplers
   :template: custom_module.rst 
   :recursive:

   couplers

.. autosummary::
   :toctree: cpw
   :template: custom_module.rst 
   :recursive:

   cpw

.. autosummary::
   :toctree: qubits
   :template: custom_module.rst 
   :recursive:

   qubits

.. autosummary::
   :toctree: resonators
   :template: custom_module.rst 
   :recursive:

   resonators

Examples 
+++++++++
This folder contains a few simple tests of the MaskMaker scripts. Useful for getting started!

.. autosummary::
   :toctree: example_scripts
   :template: custom_module.rst 
   :recursive:

   example_scripts

Basics
+++++++
This section contains the files in the root repository folder. 
Some of them are standard component templates or operations, while others work on
the importation of files.

.. autosummary::
   :toctree: miscellaneous
   :caption: Basics
   :template: custom_module.rst 
   :recursive:
   
   alphanum
   bondpad
   component
   import_dxf
   junction
   mask
   pt_operations
   sdxf

   

   

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`





