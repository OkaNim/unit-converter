# unit-converter


## Requirements
Python 3


## How to use
Please run test.<br>py in /src.<br><br>
<br>
--- test.<br>py ---<br>

import src_206_unit_convertor_230324 as src_206<br>
<br>
ccu_file = "electric-conductivity_CCU.<br>txt"<br>
value = "9.<br>2 × 10-5"<br>
text = ["electric conductivity (mS/m)", "Results of the obtained physical values"]<br>
<br>
result = src_206.<br>main(ccu_file, value, text)<br>
print(result)<br>

---------------<br>
<br>
After running, the results in the dict form will be printed on screen as follow:<br>
<br>
{'power_10': '10-5 (in value)', 'value_cl': '9.<br>200000E-05', 'unit': 'mS/m', 'value_cv': '9.<br>200000E-10', 'unit_cv': 'S cm-1', 'factor': '1.<br>000000E-05', 'use_power_10': 'use as recognized', 'CCU_file': 'electric-conductivity_CCU.<br>txt'}<br>
<br>
power_10: recognized power of ten<br>
value_cl: cleaned value<br>
unit: recognized unit<br>
value_cv: value converted to a destination unit<br>
unit_cv: destination unit<br>
factor: conversion factor<br>
use_power_10: how to use a power of ten recognized in text other than value<br>
CCU_file: used CCU file name.<br><br>
<br>
Underscores(_) in dict_values denote that a value or a power of ten could not be recognized or cleaned or converted.<br><br>
<br>
<br>
A unit in input text or value is recognized and then convert an input value for a destination unit.<br><br>
(If a unit is written in value and text is unnecessary, please set text=[].<br>) <br>
A CCU file (CCU: combination of component units) is neccessary to do them.<br><br>
A destination unit is registered in the file in advance.<br><br>
Additionally, how to use a power of ten recognized in text other than value is specified in the file in advance  (please see '???' below).<br><br>
The CCU files for some material propertie are put in /src/199_file/CCU.<br><br>
If there is no file for desirable material property, please create yourself by seeing 'How to prepare CCU files' below.<br> <br>
<br>
An input value is cleaned in the int or float type before converting (the unnecessary characters are deleted).<br> <br>
At this time, if a power of ten is included, it will be recogninzed and incorporated with the cleaned value.<br><br>
It is the same for a power of ten in text.<br> <br>
If only cleaning value is necessary, please set ccu_file="" or use unitless_CCU.<br>txt.<br><br>
<br>
If there are multiple text in which an unit may be written, put all of them in the list.<br><br>
Check whether an unit is written in order or not (if recognized, stop checking there.<br>)<br>
<br>
<br>
<br>
### How to prepare CCU files
Show how to prepare the CCU file (CCU: combination of component units) for thermal conductivity as an example here.<br>
<br>
<br>
A CCU file includes the following three terms:<br>
-- combination of component units --<br>
-- destination –-<br>
-- + or - sign for power of 10 in text other than value --<br>
<br>
<br>
In -- combination of component units --, register CCUs.<br><br>
For thermal conductivity, register the following two CCUs:<br>
*power [/length /temperature]<br>
*energy [/time /length /temperature]<br>
<br>
Use names of component units, e.<br>g, power for watt (symbol: W) and length for centimeter (cm) (Names and symbols can be confirmed in used-comp-unit.<br>dat in /src/199_file).<br><br>
The unit of thermal conductivity composes of the units for power, length, and temperature (e.<br>g.<br> W/cm K), or the units for energy, time, length, and temperature (e.<br>g.<br> J/s cm K).<br><br>
Therefore, it is necessary to register the two combinations (two or more can be registered, if needed).<br><br>
In the registration, it is neccessary to prefix * or / to each name to denote which the component unit is in the numerator or denominator parts, respectively.<br><br>
Additionally, it is necessary to describe the component units in the order usually written.<br><br>
However, the order is not frequently fixed such as 'W/cm K' and 'W/K cm'.<br><br>
If there is a part which the order is unclear, use square brackets ([ ]) for the part.<br><br>
In square brackets, the notations for all orders are automatically generated.<br><br>
However, if the order is clear, it is better not to use square brackets because of less time to execute.<br><br>
Based on the registered CCUs, a variery of unit notations for thermal conductivity and a conversion factor for each notation are generated using symbols of component units to recognize a unit and to convert a value, respectively.<br><br>
Symbols used can be confirmed in used-comp-unit.<br>dat in /src/199_file.<br><br>
Typical symbols are registered in the files in /src/199_file/component-unit and symbol-variant.<br>txt in /src/199_file/other-necessaries and inputted from these.<br><br>
If there is no appreciable symbol, it is neccessary to register it or to create a new component unit file by seeing 'How to create a component unit file' below.<br>
<br>
<br>
In -- destination –-, register a destination unit such as 'W m-1 K-1'.<br><br>
In the registration, it is necessary to use negative exponents, not slash (/), for component units in the denominator part.<br><br>
Even if two or more combinations are registered in -- combination of component units --, one destination unit should be registered.<br><br>
<br>
<br>
In -- + or - sign for power of 10 in text other than value --, specify how to use powers of ten recognized in text other than value using 0, 1, or 2.<br><br>
These numbers denote as follows:<br>
0: use as recognized<br>
1: use always positive<br>
2: use always negative<br>
<br>
Incorrect powers of ten are occasionally written in text from scientific articles.<br><br>
If the order of magnitude for values is clear, it is better to specify 1 or 2.<br><br>
<br>
<br>
After registering the three, save the CCU file in /src/199_file/CCU.<br><br>
The filename can be anything, if the end is '_CCU.<br>txt'.<br><br>
<br>
<br>
<br>
### How to register variants for symbols of component units.<br><br>
There are occasionally typographycal errors in text from scientific articles, e.<br>g.<br> 'pa' for Pa (pascal).<br><br>
Such error notations can be also recognized by registering as the variants in symbol-variant.<br>txt in /src/199_file/other-necessaries.<br><br>
The file is a TSV format and consists of three columns of symbol-variant, name, and symbol.<br><br>
Register an error notation, the corresponding name and symbol for a component unit, respectively, as written in the file.<br><br>
After the registration, once the program is executed, the notation will be outputted in used-comp-unit.<br>dat in /src/199_file.<br><br>
Please confirm by the file whether the notation is used or not.<br><br>
<br>
<br>
<br>
### How to create a component unit file
If there is no appreciable symbol in the component unit files in /src/199_file/component-unit or no appreciable component unit file in the folder, it is neccessary to register or create them.<br><br>
Show how to register symbols in the component unit files with using mass.<br>txt in /src/199_file/component-unit as an example.<br>
The file is a TSV format and composes of four columns of symbol, destination, factor, and prefix-used.<br>
In mass.<br>txt, g (gram), t (ton), and lb (pound) are registered for symbol.<br>
For desitination, register a desitination unit.<br>
In the registarion, it is better to use SI units.<br>
Therefore, kg (kilogram) is registered in mass.<br>txt.<br>
The same desitination unit should be used for all regsitered symbols.<br>
In the column of factor, register a conversion factor for the desitination unit.<br>
For g (gram), 1e-3 is registered because of 1 g = 1e-3 kg.<br>
The notaions for factor can be anything (e.<br>g.<br> 0.<br>001, 1e-3) that can be used as the float type in the program.<br>
The factors for t (ton) and lb (pound) are registerd similarily.<br>
If unit prefixes can be used for the registered symbols, they can be registered in the column of prefix-used.<br>
If registered, the notations and the factors are automatically generated in the program.<br>
However, it is better not to register unnecessary ones because of less time to execute the program.<br>
For g (gram), seven unit prefixes of n (nano), µ (micro), u (micro), m (milli), k (kilo), K (kilo), M (mega) are registered.<br>
Usable unit prefixes can be confirmed in unit-prefix.<br>txt in /src/199_file/unit-prefix.<br>
For micro and kilo, 'u' and 'K' are also registered in the file as the variants for 'µ' and 'k', respectively, because they are frequently misprinted.<br>
For t (ton) and lb (pound), unit prefixes are not regsitered.<br>
If not use at all, write 'non'.<br>
Conversely, if use all unit prefixes in unit-prefix.<br>txt, write 'all'.<br>
<br>
If there is no appreciable component unit file, please create a new file as above, based on an existing file.
The finename can be anything, if the end is '.txt'.
<br>
<br>
<br>
### How to register allowable characters for unit recognition
In recognizing a unit in text or value, every 0-1 character before and after the unit and 0-3 characters between the component units are also matched by regular expression.<br>
If the matched characters other than component units are all allowable, the matching will be accepted.<br>
Else, excluded, because it is highly possiple not to be a unit.<br>
The allowable characters are registered in allowable-char.<br>txt in /src/199_file/other-necessaries (empty and blanc characters and numbers (0-9) are automatically registered in executing the program).<br>
If a unit cannot be recognize, the matching may be excluded by the characters before and after the component units.<br>
Please try to register the characters in allowable-char.txt.<br>
