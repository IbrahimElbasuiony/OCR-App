import ast




def parser(response):
    if not isinstance(response,str):
        return "Not a string"
    

    try:

        if response.strip().startswith('{') and response.strip().endswith('}'):
            dict_data = ast.literal_eval(response)
            if isinstance(dict_data,dict):
                return dict_data
            
        return "String but not dict"
    except (ValueError,SyntaxError):
        return "string but not a valied dict"
    
