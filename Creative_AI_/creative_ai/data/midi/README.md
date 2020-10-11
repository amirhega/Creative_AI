# Converting midi data to pysynth

## Converting midi to ascii

The `mid2asc.c` file in this folder can convert midi files into ascii text. (Credit to A.P.Shelby for writing this open-source code and the [documentation here](http://www.archduke.org/midi/instrux.html).)


`./mid2asc midifile > textfile`

This will convert the file named `midifile` into a file containing the ascii text named `textfile.`

## Converting ascii to pysynth


The `loadMusic()` function will return text structured exactly done in the core, lists of musical notes where the first elements in the list are the starting tokens `^::^` and `^:::^` and the last element in the list is the ending token `$:::$`.
