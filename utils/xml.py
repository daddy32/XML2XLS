import xml.etree.ElementTree as et 
import pandas as pd
import collections

def parse_element(recordList, indent = 0, max_level = 9999):
    '''
        Helper function to parse an XML element and print all its childre, recursively.
    '''

    if max_level <= 0:
        return
        
    print(' '*indent + '{}'.format(recordList.tag))
    for child in recordList:
        #print('    ' + child.tag)
        parse_element(child, indent + 4, max_level-1)
       
# XML to pandas inspired by:
# https://robertopreste.com/blog/parse-xml-into-dataframe

def xml_element_to_df(
        xml_root: et.Element, 
        columns, # list or dictionary
        namespace = ''
    ) -> pd.DataFrame:
    '''
        Parses all first-level children of given XML element, extracts values
        from their first-level childred given by names and transforms them
        into rows and columns of a Pandas DataFrame
    '''
    
    column_names = []
    
    if xml_root is None:
        # TODO: Log
        print('Received xml_root == None.')
        return

    if isinstance(columns, collections.Mapping):              
        for column in columns:
            column_names.append(columns[column])
    else:
        column_names = columns
                
    not_found = set()

    # TODO: Option to detect column names automatically, remove namespace from them for df.
    out_df = pd.DataFrame(columns=column_names)
    for node in xml_root: 
        values = []
        for column in columns:
            cell = node.find(namespace + column)
            if cell is None:
                val = None
                not_found.add(column)
            else:                
                val = cell.text                
            values.append(val)

        out_df = out_df.append(
            pd.Series(values, index=column_names), 
            ignore_index = True
        )
        
    if len(not_found) > 0:
        # TODO: log warning
        print('Some columns could not be found (at least in some of the rows): {}'.format(not_found))

    # Try to convert columns to numeric type, if possible
    out_df = out_df.apply(pd.to_numeric, errors='ignore')

    return out_df
