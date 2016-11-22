
def fix_quotes(fixed_p):

    for i in range(0, len(fixed_p)):
        
        if fixed_p[i:i + 1] == '"':
            if i == 0:
                fixed_p = '``' + fixed_p[1:]
            else:
                if fixed_p[i - 1:i] == ' ':
                    fixed_p = fixed_p[:i] + '``' + fixed_p[i + 1:]
                    
        if fixed_p[i:i + 1] == '\'':
            if i == 0:
                fixed_p = '`' + fixed_p[1:]
            else:
                if fixed_p[i - 1:i] == ' ':
                    fixed_p = fixed_p[:i] + '`' + fixed_p[i + 1:]

    return fixed_p
    
