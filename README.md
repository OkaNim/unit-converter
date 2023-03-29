# unit-converter


## Requirements
Python 3


## How to use
Please use as described in test.py in /src.<br>
<br>
After importing src_206_unit_convertor_230324.py, a CCU file name, a value, and a list putting text are given to convert the value to the desitination unit. If there are some text in where an unit may be written, please put all of them in the list. Check whether an unit is described in order (If recognized, stop checking there.)
<br>
<br>
If test.py is run, the result (type: dict) will be returned as follows:<br>
<br>
	*{'power_10': '10-5 (in value)', 'value_cl': '9.200000E-05', 'unit': 'mS/m', 'value_cv': '9.200000E-10', 'unit_cv': 'S cm-1', 'factor': '1.000000E-05', 'use_power_10': 'use as recognized', 'CCU_file': 'electric-conductivity_CCU.txt'}<br>
<br>
power_10: power of 10<br>
value_cl: cleaned value<br>
unit: recognized unit<br>
value_cv: converted value to the destination unit<br>
unit_cv: destination unit (describe in a ccu_file)<br>
factor: conversion factor<br>
use_power_10: how to use a power of 10 recognized in other than value (specify in a ccu_file)<br>
CCU_file: used CCU file name.<br>
<br>
<br>


## How to prepare CCU files
CCU denotes combination of component units.
CCU files are necessary to convert values.
Some CCU files have been put in /src/199_file/CCU.
But, if there is no CCU file for applicable material properties, it is necessary to prepare the CCU files in advance.
Show how to prepare the CCU file for thermal conductivity as an example, below.


A CCU file includes the following three terms:<br>
-- combination of component units --<br>
-- destination –-<br>
-- + or - sign for power of 10 in text other than value --<br>
<br>
<br>
In -- combination of component units --, register CCUs using names of component units, e.g, power for watt (W) and length for centimeter (cm) (The names can be confirmed in used-comp-unit.dat in /src/199_file).
For thermal conductivity, register the following two CCUs:<br>
*power [/length /temperature]<br>
*energy [/time /length /temperature]<br>
<br>
The unit of thermal conductivity is notated by the component units of power, length, and temperature (e.g. W/cm K), or energy, time, length, and temperature (e.g. J/s cm K).
Therefore, it is necessary to register the two (two or more can be registered, if needed).
Based on the combinations, a variery of unit notations for thermal conductivity are generated using symbols of component units, e.g. W (watt) and cm (centimeter) and recognized the unit in text.
(Symbols are registerd in the files in /src/199_file/component-unit and in symbol-variant.txt in /src/199_file/other-necessaries).
It is neccessary to prefix * or / to names to denote the numerator and denominator parts, respectively.
Additionally, it is necessary to describe the components units in the order usually written in text.
However, the order is not always fixed such as 'W/cm K' and 'W/K cm' (the order is not fixed frequently for multiple component units in the denominator part).
For such cases, square brackets ([ ]) are used.
In square brackets, combination of all orders is automatically generated.
However, if square brackets are unnecessary, it is better not to use because of less time to execute.<br>
<br>
<br>
In -- destination –-, the destination unit users would like to use is described such as 'W m-1 K-1'.
It is necessary to use negative exponents for component units in the denominator part, not slash (/).
Even if two or more CCUs are registered in -- combination of component units --, one destination unit should be registered.<br>
<br>
<br>
In -- + or - sign for power of 10 in places other than value --, how to use powers of ten recognized in text other than value is specified using 0, 1, or 2.
These numbers denote as follows:<br>
0: use as recognized<br>
1: use always positive<br>
2: use always negative<br>
<br>
Incorrect powers of ten are occasionally written in text.
If the order of magnitude for values is clear, it is better to specify 1 or 2.
For 1, if '10-5' is recognized, 100,000 will be multipied by the value to give the cleaned value (value_cl).<br>
<br>
<br>
After registering the three, save the CCU file in /src/199_file/CCU.
The filename can be anything, but must end with '_CCU.txt'.

