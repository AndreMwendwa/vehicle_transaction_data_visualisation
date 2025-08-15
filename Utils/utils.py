import pandas as pd

def get_years(start_col, end_col):
    min_start = start_col.min()
    max_end = end_col.max()
    return (int(min_start), int(max_end))

def replace_semicolon_with_linebreak(input_dataframe):
    '''Replace semicolon with linebreak in every element of the dataframe
    that is a string'''
    for col in input_dataframe.columns:
        if input_dataframe[col].dtype == 'object':
            input_dataframe[col] = input_dataframe[col].replace(';', '<br>', regex=True)
    return input_dataframe

def make_html_table_from_dataframe(input_dataframe, link_columns):
    '''Make an html table from a dataframe'''
    input_dataframe = replace_semicolon_with_linebreak(input_dataframe)

    # Convert "Eligible vehicles" and "Source" columns to HTML links if they exist
    for col in link_columns:
        if col in input_dataframe.columns:
            input_dataframe[col] = input_dataframe[col].apply(
                lambda x: f'<a href="{x}" target="_blank">{x}</a>' if pd.notna(x) and str(x).startswith(('http://', 'https://')) else x
            )

    input_dataframe.index.name = ''
    input_dataframe.reset_index(inplace=True)

    output = f"""
    <html>
    <head>
    <style> 
      table, th, td {{font-size:11pt; border:1px solid black; border-collapse:collapse; text-align:justify; 
      vertical-align:top; background-color: #ecf7f1; color: black;}}
      th, td {{padding: 5px;}}
      th {{background-color: #9cd1b4;}}
      tr td:first-child {{font-weight: bold;}}
    </style>
    </head>
    <body>
    {input_dataframe.to_html(index=False, escape=False)}
    </body>
    </html>
    """
    return output
    return output


def get_all_column_values(col):
    '''Get all unique values in a column'''
    if col.dtype == 'object':
        return col.unique().tolist()
    else:
        return col.dropna().unique().tolist()