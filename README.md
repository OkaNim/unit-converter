# unit-converter


## Requirements
Python 3


## How to use
Please run test.py in /src.<br>
<br>
--- test.py ---<br>

import src_206_unit_convertor_230324 as src_206<br>
<br>
ccu_file = "electric-conductivity_CCU.txt"<br>
value = "9.2 × 10-5"<br>
text = ["electric conductivity (mS/m)", "Results of the obtained physical values"]<br>
<br>
result = src_206.main(ccu_file, value, text)<br>
print(result)<br>

---------------<br>
<br>
After running, the results will be printed in the dict form on screen as follow:<br>
<br>
{'power_10': '10-5 (in value)', 'value_cl': '9.200000E-05', 'unit': 'mS/m', 'value_cv': '9.200000E-10', 'unit_cv': 'S cm-1', 'factor': '1.000000E-05', 'use_power_10': 'use as recognized', 'CCU_file': 'electric-conductivity_CCU.txt'}<br>
<br>
power_10: recognized power of ten<br>
value_cl: cleaned value<br>
unit: recognized unit<br>
value_cv: value converted to a destination unit<br>
unit_cv: destination unit<br>
factor: conversion factor<br>
use_power_10: how to use a power of ten recognized in text other than value<br>
CCU_file: used CCU file name.<br>
<br>
Underscores(_) in dict_values denote that a value or a power of ten could not be recognized or cleaned or converted.<br>
<br>
<br>
A unit in input text or value is recognized and then convert an input value for a destination unit.<br>
(If a unit is written in value and text is unnecessary, please set text=[].) <br>
A CCU file (CCU: combination of component units) is neccessary to recognize a unit and convert a value.<br>
A destination unit is registered in the file in advance.<br>
Additionally, how to use a power of ten recognized in text other than value is specified in the file in advance  (please see '???' below).<br>
The CCU files for some material propertie are put in /src/199_file/CCU.<br>
If there is no file for desirable material property, please create yourself by seeing 'How to prepare CCU files' below. <br>
<br>
An input value is cleaned in the int or float type before converting (the unnecessary characters are deleted). <br>
At this time, if a power of ten is included, it will be recogninzed and incorporated with the cleaned value.<br>
It is the same for a power of ten in text. <br>
If only cleaning value is necessary, please set ccu_file="" or use unitless_CCU.txt.<br>
<br>
If there are multiple text in which an unit may be written, put all of them in the list.<br>
Check whether an unit is written in order (if recognized, stop checking there.)<br>
<br>
<br>
<br>
### How to prepare CCU files
Show how to prepare the CCU file (CCU: combination of component units) for thermal conductivity as an example here.
<br>
<br>
A CCU file includes the following three terms:<br>
-- combination of component units --<br>
-- destination –-<br>
-- + or - sign for power of 10 in text other than value --<br>
<br>
<br>
In -- combination of component units --, register CCUs.<br>
For thermal conductivity, register the following two CCUs:<br>
*power [/length /temperature]<br>
*energy [/time /length /temperature]<br>
<br>
Use names of component units, e.g, power for watt (symbol: W) and length for centimeter (cm) (Names and symbols can be confirmed in used-comp-unit.dat in /src/199_file).<br>
The unit of thermal conductivity composes of the units for power, length, and temperature (e.g. W/cm K), or the units for energy, time, length, and temperature (e.g. J/s cm K).<br>
Therefore, it is necessary to register two combinations (two or more can be registered, if needed).<br>
In the registration, it is neccessary to prefix * or / to names to denote the numerator and denominator parts, respectively.<br>
Additionally, it is necessary to describe the component units in the order usually written.<br>
However, the order is not always fixed such as 'W/cm K' and 'W/K cm' (For multiple component units in the denominator part, the order is not frequently fixed).<br>
If there is a part which the order is unclear, use square brackets ([ ]) for the part.<br>
In square brackets, combinations for all orders are automatically generated.<br>
However, if the order is clear, that is, unneccessary to use square brackets, it is better not to use them because of less time to execute.<br>
Based on the registered CCUs, a variery of unit notations for thermal conductivity and a conversion factor for each notation are generated using symbols of component units to recognize a unit and to convert a value, respectively.<br>
Symbols used can be confirmed in used-comp-unit.dat in /src/199_file.<br>
Symbols are registered in the files in /src/199_file/component-unit and symbol-variant.txt in /src/199_file/other-necessaries and inputted from these.<br>
If there is no appreciable symbol, it is neccessary to register it or to create a new component unit file by seeing 'How to create a component unit file' below.
<br>
<br>
In -- destination –-, a destination unit is registerd such as 'W m-1 K-1'.<br>
In the registration, it is necessary to use negative exponents, not slash (/), for component units in the denominator part.<br>
Even if two or more combinations are registered in -- combination of component units --, one destination unit should be registered.<br>
<br>
<br>
In -- + or - sign for power of 10 in text other than value --, specify how to use powers of ten recognized in text other than value using 0, 1, or 2.<br>
These numbers denote as follows:<br>
0: use as recognized<br>
1: use always positive<br>
2: use always negative<br>
<br>
Incorrect powers of ten are occasionally written in text from scientific articles.<br>
If the order of magnitude for values is clear, it is better to specify 1 or 2.<br>
<br>
<br>
After registering the three, save the CCU file in /src/199_file/CCU.<br>
The filename can be anything, if the end is '_CCU.txt'.<br>


### How to register variants for symbols of component units.
There are occasionally typographycal errors in text, e.g. 'pa' for Pa.
Therefore, such errors can be registered as variants for symbols of component units in symbol-variant.txt in /src/199_file/other-necessaries.
The file is a TSV format and consists of three columns of symbol-variant, name, and symbol.
Register an error notation, the corresponding name and symbol of a component unit, respectively.
For example,
symbol-variant	name	symbol<br>
<br>
pa	pressure	Pa<br>

Whether the registration can be confirmed in used-comp-unit.dat in /src/199_file.
Once execution, the notation is outputted to the file.


### How to create a component unit file
If there is no appreciable symbol in the component unit files in /src/199_file/component-unit or no appreciable component unit file in the folder, it is neccessary to register or create them.<br>
<br>
<br>
If there is appreciable component unit file and no appreciable symbol, register the symbol in the file.
The component unit file is a TSV format which composes of 4 columns of symbol, destination, factor, and prefix-used.
If see mass.txt as an example, g (gram), t (ton), and lb (pound) are registered in symbol.
In destination and factor, a desitination unit and a conversion factor are registered.
Here, must use the MKS system for desitination.
Therefore, kg (kilogram) is used in mass.txt and 1e-3 is registered for factor because of 1 g = 1e-3 kg.
In prefix-used, register neccessary unit prefixes.
For g (gram) in mass.txt, 7 unit prefixes of n (nano), µ (micro), u (micro), m (milli), k (kilo), K (kilo), M (mega) are registered.
Usable unit prefixes can be confirmed in unit-prefix.txt in /src/199_file/unit-prefix.
For micro and kilo, 'u' and 'K' are also registered as the variants for 'µ' and 'k', respectively, because they are frequently misprinted.
If unit prefixes are registered, every notation and factor, i.e. 'ng'(factor against kg： 1e-12), 'µg'(1e-9), 'ug'(1e-9), 'mg'(1e-6), 'kg'(1), 'Kg'(1), 'Mg'(1e+3), are automatically prepared.
If need all unit prefixes in unit-prefix.txt or not need at all, register 'all' or 'non', respectively.
It is better not to use unneccessary unit prefixes to avoid more time to execute.


### How to register allowable characters for unit recognition
In recognizing a unit in text, every 0-1 character before and after the unit and 0-3 characters between the component units are also matched by regular expression.
If the matched characters other than component units are all allowable ones, the matching will be accepted.
Else, excluded, because it is highly possiple not to be a unit.
The allowable characters are registered in allowable-char.txt in /src/199_file/other-necessaries (empty and blanc characters and numbers (0-9) are automatically used for allowable characters).
If the exclusion may be caused by a character which is not registerd in the file, try to execute again after registering the character.


