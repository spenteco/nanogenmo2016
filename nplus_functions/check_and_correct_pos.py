    
def check_and_correct_pos(word, pos, rita_lexicon):
    
    corrected_pos = pos
    checked = False
    
    rita_pos = None
    try:
        rita_pos = rita_lexicon[word]
    except KeyError:
        pass
        
    if checked == False and rita_pos == None:
        #print 'WORD NOT IN RITA', word, pos
        checked = True
        
    if checked == False and pos in rita_pos:
        #print 'POS OK', word, pos, rita_pos
        checked = True
        
    if checked == False and word == 'i' and pos == 'prp':
        #print 'POS OK', word, pos, rita_pos
        checked = True
    
    if checked == False:
        #corrected_pos = rita_pos[0]
        corrected_pos = rita_pos[-1]
        checked = True
        
        #print 'POS ERROR', word, pos, rita_pos, '-->', corrected_pos
        
    return corrected_pos
    
