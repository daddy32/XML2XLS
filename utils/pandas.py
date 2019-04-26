from os.path import splitext
import pandas as pd


def save_df_to_file(
        df: pd.DataFrame,
        filename: str,
        **kwargs
    ):
    '''
        Saves the Pandas DataFrame to the file, while automatically
        determining the method to call by using the file extension.
    '''
    # TODO: test parameters, extension
    _, extension = splitext(filename)
    extension = extension.lower()[1:]

    if extension == 'xlsx' or extension == 'xls':
        df.to_excel(filename, index=False, **kwargs)
    elif extension == 'csv':
        df.to_csv(filename, index=False, **kwargs)
    elif extension == 'json':
        df.to_json(filename, index=False, orient='table', **kwargs)
    '''
    # Not supported yet
    elif extension == 'html':
        df.to_html(filename, index=False, render_links=True, force_unicode=True, **kwargs)
    '''
