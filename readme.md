# XML2XLS

## Description

XML2XLS is a command line utility used to extract data from repeating elements in the XML file and save them to output file in excel, csv or json format.
It is written in Python and has following dependencies:

```Python
pandas
lxml
pyinstaller (for building executable only)
```

## Manual

### Usage

```bash
Extract specified elements from the XML file and save them as xlsx file (or alternative formats -
xls, csv, json). Command loops through all children elements of a given XML element (default: root) and
extracts specified fields from each of them, putting each set as a new row to the output file.
Output file format is determined by extension of filename provided with -o parameter (default: xlsx)

usage: xml2xls.py [-h] [-o OUTPUT_FILE] [-n NAMESPACE] [-p PARENT_ELEMENT]
                  [-l LABELS [LABELS ...]] [-v]
                  input_file column [column ...]

Example usage:
    xml2xls input.xml column_1 column_2
    xml2xls input.xml -p "parent_element" -o output.csv "./@attribute_01|.//@attribute_02" ".//column_1" -l "Attributes" "Column values" -v

positional arguments:
  input_file
  column                Repeatable. Name or XPath of a child element to be used as an column.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Optional name of the output file. Specified path must exist; file will be created. If not provided, file name is determined from name of the input file.
  -n NAMESPACE, --namespace NAMESPACE
                        XML namespace to be added to all columns.
  -p PARENT_ELEMENT, --parent_element PARENT_ELEMENT
                        XML element whose children will be considered as rows in output. If not provided, XML root is used.
  -l LABELS [LABELS ...], --labels LABELS [LABELS ...]
                        Optional list of column labels.         If not given, their XML names (or XPaths) given in "column" argument are used.
  -v, --preview         Display the preview of the output file in the console.
  ```

### Compiling

It is possible to build executable file for current platform, using pyinstaller (pyinstaller does not cross-compile). This makes it possible to run the program without dependencies (python runtime), but is not necessary if target computer has the runtime and dependencies installed.

To create the executable, run the following command:
`pyinstaller xml2xls.spec`
Resulting file is somewhat large (~100MB).

## Roadmap

- Examples along with imput data.
- Pre-built executables (on request).
- Simple GUI (probably using Gooey).
