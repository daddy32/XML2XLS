import numpy as np
import pandas as pd
import utils.xml as xml
import utils.pandas as pd_util
import argparse
import textwrap

from datetime import datetime
from pathlib import Path
from os.path import splitext

try:
  from lxml import etree as et
except ImportError:
    try:
        import xml.etree.ElementTree as et
    except ImportError:
        print("  Failed to import ElementTree from any known place")


def convert_and_save(
        input_file_name: str,
        columns,
        output_file_name: str='',
        namespace: str='',
        root_element_name: str='',
        file_format: str='',
        preview: bool=False
    ):
    # Load the XML file and parse it
    xtree = et.parse(input_file_name)
    xroot = xtree.getroot()

    if root_element_name is None or root_element_name == '':
        data_root = xroot
    else:
        root_query = root_element_name
        data_root = xtree.find(root_query)
        if data_root is None:
            # TODO: Log
            print('  ERROR: Root not found. Query used: {}'.format(root_query))
            raise ValueError('Root not found.')

    # Convert the file to Pandas dataFrame
    df = xml.xml_element_to_df(data_root, columns, namespace)
    if preview:
        print('  Output preview:')
        print(df.head(10))
        print('  Total rows: {}.'.format(len(df)))

    # Determine file format and file name
    if output_file_name is None or output_file_name == '':
        output_file_name, _ = splitext(input_file_name)
        if file_format is None or file_format == '':
            file_format = 'xlsx'
        output_file_name += '.' + file_format

    if file_format is None or file_format == '':
        _, extension = splitext(output_file_name)
        if extension != '' and (file_format is None or file_format == ''):
            file_format = extension[1:]

    print('  Writing output data to: "{}" ({} format).'.format(
        output_file_name, file_format
    ))

    # Save the file
    pd_util.save_df_to_file(df, output_file_name)
    #df.to_excel(output_file_name)

def parse_args():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''\
            Extract specified elements from the XML file and save them as xlsx file (or alternative formats -
            xls, csv, json). Command loops through all children elements of a given XML element (default: root) and
            extracts specified fields from each of them, putting each set as a new row to the output file.
            Output file format is determined by extension of filename provided with -o parameter (default: xlsx)

            Example usage:
                xml2xls input.xml column_1 column_2
                xml2xls input.xml -p "parent_element" -o output.csv "./@attribute_01|.//@attribute_02" ".//column_1" -l "Attributes" "Column values" -v
        '''),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('input_file', type=str)
    parser.add_argument('-o', '--output_file', type=str,
        help='Optional name of the output file. Specified path must exist; file will be created. If not provided, file name is determined from name of the input file.'
    )
    parser.add_argument('-n', '--namespace', type=str, help='XML namespace to be added to all columns.', default='')
    parser.add_argument('-p', '--parent_element', type=str,
        help='XML element whose children will be considered as rows in output. If not provided, XML root is used.',
        default='')
    '''
    # TODO: Implement.
    #   Requires adding parameter below and modifications in main, xml_element_to_df and convert_and_save.

    parser.add_argument('-r', '--row_element', type=str,
        help='Name or XPath of a child element to be used as a row. \
        IE all parent\'s children with satisfying this selection will be transformed to rows in resulting table.',
        default='')
    '''
    parser.add_argument('column', nargs='+', action='append',
        help='Repeatable. Name or XPath of a child element to be used as an column.')
    parser.add_argument('-l', '--labels', nargs='+', action='append',
        help='Optional list of column labels. \
        If not given, their XML names (or XPaths) given in "column" argument are used.')
    parser.add_argument('-v', '--preview', action='store_true',
        help='Display the preview of the output file in the console.')

    # TODO: null value, explicit file_format

    return parser.parse_args()

def main(args):
    # Prepare the parameters
    columns = args.column[0]
    labels = args.labels

    if labels != None and len(labels) > 0:
        columns = dict(zip(columns, labels[0]))

    # Do the action
    convert_and_save(
        input_file_name = args.input_file,
        columns = columns,
        output_file_name = args.output_file,
        namespace = args.namespace,
        root_element_name = args.parent_element,
        # file_format = file_format,
        preview = args.preview
    )


if __name__ == "__main__":
    print("Initializing...")

    args = parse_args()

    try:
        main(args)
    except:
        print('ERROR: Failed to convert the data. Arguments:')
        print('  {}'.format(args))
        print('Stack trace:')
        raise

    print("...OK, conversion is done.")
