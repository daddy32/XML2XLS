try:
  from lxml import etree as et
except ImportError:
    try:
        import xml.etree.ElementTree as et
    except ImportError:
        print("Failed to import ElementTree from any known place")

import pandas as pd
import collections
import time

def parse_element(recordList, indent = 0, max_level = 9999):
    '''
        Helper function to parse an XML element and print all its children, recursively.
    '''

    if max_level <= 0:
        return

    print(' '*indent + '{}'.format(recordList.tag))
    for child in recordList:
        # print('    ' + child.tag)
        parse_element(child, indent + 4, max_level-1)

# XML to pandas inspired by:
# https://robertopreste.com/blog/parse-xml-into-dataframe


def xml_element_to_df(
        xml_root: et.Element,
        columns,  # list or dictionary
        namespace: str = ''
    ) -> pd.DataFrame:
    '''
        Parses all first-level children of given XML element, extracts values
        from their first-level childred given by names and transforms them
        into rows and columns of a Pandas DataFrame
    '''
    start_time = time.time()
    column_names = []

    if xml_root is None:
        # TODO: Log
        print('ERROR: Received xml_root == None.')
        return

    if isinstance(columns, collections.Mapping):
        for column in columns:
            column_names.append(columns[column])
    else:
        column_names = columns

    not_found = set()

    # TODO: Option to detect column names automatically, remove namespace from them for df.
    # TODO: Consider: Can't we run xpath in bulk, instead of separately for every row?
    node_count = len(xml_root)
    print('     total nodes: {}'.format(node_count))
    i = 0

    dictionary_list = []
    for node in xml_root:
        i += 1

        if i % 1000 == 0:
            curr_time = time.time()
            print('     Done: {}% ({})'.format(round(1000*i/node_count)/10, i))
            print('         time = %.6f seconds' % (curr_time-start_time))

        values = {}
        k = 0
        for column in columns:
            cells = node.xpath(namespace + column)
            val: str = ''
            if cells is None or len(cells) == 0:
                val = None
                not_found.add(column)
            else:
                for cell in cells:
                    if isinstance(cell, et._Element):
                        if cell.text is not None:
                            val += cell.text
                    elif isinstance(cell, et._ElementUnicodeResult):
                        val += cell
                    else:
                        print(" WARN: not supported xpath result type: {}.".format(type(cell)))
                    val += ' '
                val = val.strip()

            values[column_names[k]] = val
            k += 1

        dictionary_list.append(values)

    print(' output size: {}'.format(len(dictionary_list)))
    out_df = pd.DataFrame.from_dict(dictionary_list)

    if len(not_found) > 0:
        # TODO: log warning
        print('WARNING: Some columns could not be found (at least in some of the rows): {}'.format(not_found))

    # Try to convert columns to numeric type, if possible
    out_df = out_df.apply(pd.to_numeric, errors='ignore')

    end_time = time.time()
    print('     Execution time = %.6f seconds' % (end_time-start_time))

    return out_df
