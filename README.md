# unit-converter


## Requirements
Python 3


## How to use
Please run test.py in /src without moving out of the folder.<br>
<br>
----- test.py -----<br>
import src_206_unit_convertor_230801 as src_206<br>
<br>
<br>
ccu_file = "density_CCU.txt"<br>
value = "9.2 × 10-4"<br>
text = ["bulk density (kg/cm3)", "(Table caption) Results of the obtained physical values"]<br>
<br>
result = src_206.main(ccu_file, value, text)<br>
<br>
print("")<br>
print(result)<br>
print("")<br>
-------------------<br>
<br>
After running, the results in the dict form will be printed on screen as follow:<br>
<br>
{'power_10': '10-4 (in value)', 'value_cl': '9.200000E-04', 'unit': 'kg/cm3', 'value_cv': '9.200000E-01', 'unit_cv': 'g cm-3', 'factor': '1.000000E+03', 'use_power_10': 'use as recognized', 'CCU_file': 'density_CCU.txt'}<br>
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
If there are underscores(_) in dict_values, they denote that a value or a power of ten could not be recognized or cleaned or converted.<br>
<br>
<br>
This program can recognize a unit in input text or value and then convert value for a destination unit.<br>
Try to use it using text and value prepared by yourself or your original script such as test.py.<br>
(If your original script is not put in /src, the folder path for /src should be specified using sys.path.append to import src_206.)<br>
A CCU file (CCU: combination of component units) is neccessary to run the program.<br>
Some CCU files for material properties are put in /src/199_file/CCU.<br>
If there is no desirable file, create it by seeing 'How to create CCU files' below.<br>
In the file, prepare for recognizing a unit and converting a value by registering CCUs, a destination unit ,etc.<br>
<br>
An input value is cleaned in the int or float type before converting for a destination unit.<br>
The unnecessary characters such as '>' and '~' in it are removed.<br>
At this time, if a power of ten is included, it will be recogninzed and used to the cleaned value.<br>
If only cleaning value is necessary (converting a value is unnecessary), set ccu_file="".<br>
<br>
If there are multiple sentences and phrases in which a unit may be written, put all of them in the list of text.<br>
Check them in order and stop checking at which a unit is recognized.<br>
At this time, checking also if a power of ten is included there.<br>
(The checking is not performed in other sentences or phrases to avoid incorrect recognition.)<br>
If a power of ten is recognized, the cleaned value will be multiplied by it.<br>
If text is unnecessary to use because of writing a unit in value, please set text=[].<br>
<br>
<br>
<br>
### How to create CCU files
Show how to create the CCU file (CCU: combination of component units) for thermal conductivity as an example.<br>
<br>
<br>
A CCU file includes the following three terms:<br>
(1) -- combination of component units --<br>
(2) -- destination –-<br>
(3) -- + or - sign for power of 10 in text other than value --<br>
<br>
<br>
In -- combination of component units --, register CCUs for unit recognition.<br>
Based on the CCUs, various unit notations are generated in the program, and a unit in an input text or value is then recognized using them.<br>
The factors for value conversion are also generated simultaneously.<br>
These are performed using the component unit files in /src/199_file/component-unit.<br>
The filename (e.g. mass.txt) includes the name ('mass') for the component unit, and symbols for the name ('g'(gram), 't'(ton), etc.), factors, and necessary unit prefixes are registered.<br>
The new files can be created by users.<br>
If necessary, create by seeing 'How to create a component unit file' below.<br>
The correspondence between names and symbols can be confirmed easier in used-comp-unit.dat in /src/199_file than in the files.<br>
<br>
For thermal conductivity, the following two CCUs are necessary to register, because there are two notation patterns such as 'W/cm K' and 'J/s cm K':<br>
*power [/length /temperature]<br>
*energy [/time /length /temperature]<br>
<br>
In the registration, use names for component units such as 'power' and 'length', and prefix * or / to each name to denote which the component unit is in the numerator or denominator parts, respectively.<br>
In the registration, a writing order of names from left is important, becasue the component units in the generated notations are ordered accoding to the order.<br>
The writing order of component units is not always fixed in scientific documents, especially in the denominator part, such as 'W/cm K' and 'W/K cm'.<br>
Therefore, if there is such a part, use square brackets in the registration.<br>
All orders of component units enclosed in them are generated in the program.<br>
However, if unnecessary, it is better not to use them because of less time to execute the program.<br>
In the two CCUs above, square brackets are used for the denominator part.<br>
<br>
In addition to square brackets, there is a case in which parentheses is necessary.<br>
The case is that it is necessary to add an exponent to a component unit.<br>
For example, for solubility parameter, the unit is generally notated such as 'MPa0.5' and 'J1/2 cm-3/2'.<br>
However, there is no component unit file for 'MPa0.5' and 'J1/2', because the creation would not be useful.<br>
In this case, use parentheses as follows:<br>
*pressure(0.5)<br>
*energy(0.5) /volume(0.5)<br>
<br>
The notations raised to the exponent of 0.5 are generated automatically in the program.<br>
If an exponent is not an integer, use decimal point in parentheses, not fraction.<br>
The fraction notations are also generated automatically.<br>
Another example is the unit for acceleration and the general notation is 'm s-2'.<br>
Since there is no component unit file for 's-2', use parentheses similarily:<br>
*length /time(2)<br>
<br>
If there is no desirable component unit file or no proper symbol in a file, create or register by seeing 'How to create a component unit file' below.<br>
Since there are various unit notaions other than typical ones, e.g. 'denier' (a unit for the thickness of fiber), create user origical files.<br>
About common typographical errors for symbols such as 'pa' for 'Pa' (pascal), they can be registed in symbol-variant.txt in /src/199_file/other-necessaries as the varinants.<br>
If necessary, regist by seeing 'How to register allowable characters for unit recognition' below.<br>
<br>
<br>
In -- destination –-, register a destination unit such as 'W m-1 K-1'.<br>
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
Incorrect powers of ten are occasionally written in scientific documents.<br>
If the order of magnitude for values is clear, it is better to specify 1 or 2.<br>
<br>
<br>
After registering the three terms, save the CCU file in /src/199_file/CCU.<br>
The filename can be anything, if the end is '_CCU.txt'.<br>
<br>
<br>
<br>
### How to register variants for symbols of component units<br>
There are occasionally typographycal errors for symbols in scientific documents, e.g. 'pa' for Pa (pascal).<br>
Such error notations can be also recognized by registering as the variants in symbol-variant.txt in /src/199_file/other-necessaries.<br>
The file is a TSV format and consists of three columns of symbol-variant, name, and symbol.<br>
Register an error notation, the corresponding name and symbol for a component unit, respectively, as written in the file.<br>
After the registration, once the program is executed, the notation will be outputted in used-comp-unit.dat in /src/199_file.<br>
Confirm in the file if the registered notation is used.<br>
<br>
<br>
<br>
### How to create a component unit file
If there is no proper symbol in the component unit files in /src/199_file/component-unit or no proper component unit file in the folder, it is neccessary to register or create them.<br>
Show how to register symbols in the component unit files using mass.txt in /src/199_file/component-unit as an example.<br>
The file is a TSV format and composes of four columns of symbol, destination, factor, and prefix-used.<br>
In mass.txt, 'g' (gram), 't' (ton), and 'lb' (pound) are registered for symbol.<br>
For desitination, register a desitination unit.<br>
SI units are better for it.<br>
Therefore, 'kg' (kilogram) is registered in mass.txt.<br>
The same desitination unit should be used for all regsitered symbols.<br>
For factor, register a conversion factor for the desitination unit.<br>
For g (gram), '1e-3' is registered because of 1 g = 0.001 kg.<br>
The notaions for factor can be anything (e.g. 0.001, 1e-3), if they can be used as the float type in the program.<br>
The factors for 't' (ton) and 'lb' are registerd similarily.<br>
If unit prefixes can be used for the registered symbols, they can be registered for prefix-used.<br>
If registered, the notations and the factors are automatically generated in the program.<br>
However, it is better not to register unnecessary ones because of less time to execute the program.<br>
For 'g' (gram), seven unit prefixes of 'n' (nano), 'µ' (micro), 'u' (micro), 'm' (milli), 'k' (kilo), 'K' (kilo), 'M' (mega) are registered.<br>
Usable unit prefixes can be confirmed in unit-prefix.txt in /src/199_file/unit-prefix.<br>
For micro and kilo, 'u' and 'K' are also registered in the file as the variants for 'µ' and 'k', respectively, because they are frequently misprinted.<br>
For 't' (ton) and 'lb', unit prefixes are not regsitered.<br>
If not use at all, write 'non'.<br>
Conversely, if use all unit prefixes in unit-prefix.txt, write 'all'.<br>
<br>
<br>
If there is no proper component unit file, create a new file based on an existing file.
The finename can be anything, if the end is '.txt'.
The character string before '.txt' is used as the name.
<br>
<br>
Show how to create special component unit files from here.<br>
There are two special cases for unit conversion.<br>
The one is a conversion between different physical quantities and the example is from the mass of water vapor to volume at standard temperature and pressure (0 °C, 1 atm).<br>
In this case, register not only a symbol, also the corresponding name, for destination in a component unit file.<br>
This can be seen in water-mass.txt in /src/199_file/component-unit.<br>
In the file, 'volume: cm3' is registered using a colon (:).<br>
For factor, '1243.06' is registered because of 1 g of water vapor = 1243.06 cm3 at standard temperature and pressure.<br>
By doing this, the conversion from mass to volume will be possible.<br>
<br>
The another is a conversion between a special unit notation and normal compounded units.<br>
For example, 'Gal' is one of the unit notations for acceleration and is used for acceleration of earthquake shaking.<br>
Because of 1 Gal = 0.01 m s-2, the conversion between the units is possible.<br>
However, there is no normal component unit file for 'Gal'.<br>
For such a case, create the special component unit file, for example, as gal.txt.<br>
However, it is necessary to create also the CCU file for acceleration.<br>
The CCU file is named as acceleration_CCU.txt and regiser the following two CCUs:<br>
*gal<br>
*length /time(2)<br>
<br>
Then, register 'Gal' for symbol, 'acceleration: m s-2' for destination, '1e-2' for factor in gal.txt.<br>
For destination, 'acceleration' is registered.<br>
By doing this, the conversion between various compounded units generated automatically from acceleration_CCU.txt and 'Gal' will be possible.<br>
<br>
<br>
<br>
### How to register allowable characters for unit recognition
In recognizing a unit in text or value, every 0-1 character before and after the unit and 0-3 characters between the component units are also matched by regular expression.<br>
If the matched characters other than component units are all allowable, the matching will be accepted.<br>
Else, excluded, because it is highly possiple not to be a unit.<br>
The allowable characters are registered in allowable-char.txt in /src/199_file/other-necessaries (empty and blanc characters and numbers (0-9) are automatically registered in executing the program).<br>
If a unit cannot be recognize, the matching may be excluded by the characters which are not registed in allowable-char.txt.<br>
In the case, try to register them in the file.<br>
