
def substitutions_to_just_words(substitutions):

    results = {}

    for k, v in substitutions.iteritems():
        if v[0] != None:
            try:
                results[k.split('_')[0]].append(v[0].split('_')[0])
            except KeyError:
                results[k.split('_')[0]] = [v[0].split('_')[0]]

    return results
