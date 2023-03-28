# unit-converter


## Requirements
Python 3


## How to use
Please use as described in test.py in src folder.<br>
If test.py is run, the result of unit conversion is displayed as follows:<br>
<br>
{'power_10': '10-5 (in value)', 'value_cl': '9.200000E-05', 'unit': 'mS/m', 'value_cv': '9.200000E-10', 'unit_cv': 'S cm-1', 'factor': '1.000000E-05', 'use_power_10': 'use as recognized', 'CCU_file': 'electric-conductivity_CCU.txt'}<br>
<br>
power_10:&#009;recognized powewr of 10<br>
value_cl:&#009;recognized powewr of 10<br>
cleaned value<br>
unit: recognized unit<br>
value_cv: converted value to the destination unit<br>
unit_cv: destination unit<br>
factor: conversion factor<br>
use_power_10: how to use power of 10 recognized in other than value (specify in a ccu_file)<br>

value_cv is the convertd value. unit and unit_cv are the recognized and destination units, respectively.  


{'power_10': '_', 'value_cl': '9.200000E+00', 'unit': '_', 'value_cv': '9.200000E+00', 'unit_cv': '_', 'factor': '_', 'use_power_10': 'use as recognized', 'CCU_file': 'thermal-condutivity_CCU.txt'}
<br>
<br>
The result is dict-type.


After importing src_206_unit_convertor_230324.py, the ccu_file name, value, and a list including text are given to convert the value to the desitination unit.
If there are some text in where an unit may be described, please put all of them in the list.

Before doing this, it is necessary to use a ccu_file for each property.  
Unit conversion is performed according to the ccu_file.

python 159_01_unit-converter_github_211223.py [DATA file] [UNITLIST file]<br>
<br>

***<br>
It is necessary to put "src_002_value_clean_211028.py" in the same folder.<br>
The trial data are in the data folder.<br>
The program can be used with or without the correct answer data (CA).<br>
If you create data with CA, the data for the terms of "ca-power-of-ten-in-value/others", "ca-unit", "ca-value-clean", "ca-value-convert", are needed, in contrast, and the data for "ca-coeff" and "ca-location-describing-unit" are not.<br>	
Please try to create your data with refferring the trial data.<br>

The modified table data extractor was put in the below URL (v2 branch).<br>
https://github.com/OkaNim/table-polymer-data-extractor/tree/v2<br>
***<br>

