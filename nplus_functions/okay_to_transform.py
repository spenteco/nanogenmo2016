
def okay_to_transform(word, pos, original_word):

    okay = False
    word_checked = False
    
    if word_checked == False and word in ['am', 'are', 'is', 'be', 'been', 'being', 'was', 'were', 'has', 'have', 'had', 'would', 'could', 'should', 'might', 'chapter', 'and', 'note', 'glossary', 'preface', 'introductory', 'introduction']:
        okay = False
        word_checked = True

    #if word_checked == False and pos in ['nn', 'nns', 'nnp', 'nnps', 'jj', 'jjr', 'rb', 'rbr', 'rbs']:
    if word_checked == False and pos in ['nn', 'nns', 'nnp', 'nnps', 'jj', 'jjr']:
    #if word_checked == False and pos in ['nn', 'nns', 'nnp', 'nnps']:
        okay = True
        word_checked = True
            
    if word_checked == False and pos.startswith('vb'):
        okay = True
        word_checked = True

    return okay
    
