
def is_illustration_paragraph(p):
    
    result = False
    
    if p.strip().startswith('[') == True and p.strip().endswith(']') == True:
        if p.lower().find('illustration') > -1 or p.lower().find('picture') > -1:
            result = True
            
    return result
