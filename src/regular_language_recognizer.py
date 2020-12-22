def Nullable(regex):
    result = []
    if regex == 'eps':
        return True
    elif list(set(regex) & set(['.', '|', '*'])) == []:
        return False
    elif '|' in regex:
        regexes = regex.split('|', 1)
        return Nullable(regexes[0]) or Nullable(regexes[1])
    elif '.' in regex:
        regexes = regex.split('.', 1)
        return Nullable(regexes[0]) and Nullable(regexes[1])
    elif '*' in regex:
        return True

    
def der_by_symbol(regex, s):
    if list(set(regex) & set(['.', '|', '*'])) == []:
        if regex != s:
            return 'Null'
        else:
            return 'eps'
    elif '|' in regex:
        regexes = regex.split('|', 1)
        r1 = regexes[0]
        r2 = regexes[1]
        return der_by_symbol(r1, s) + '|' + der_by_symbol(r2, s)
    elif '.' in regex:
        regexes = regex.split('.', 1)
        r1 = regexes[0]
        r2 = regexes[1]
        if Nullable(r1):
            return der_by_symbol(r1, s)+'.'+r2+'|' + der_by_symbol(r2, s)
        else:
            return der_by_symbol(r1, s)+'.'+r2
    
    elif '*' in regex:
        return der_by_symbol(regex[:-1], s) + '.' + regex


def check_word(regex, word):
    regex = ''.join(regex.split())
    alphabet = regex.replace('.','|').replace('*', '|').split('|')
    alphabet = [value for value in alphabet if value != '']
    w = ''
    prepared_word = []
    for i in word:
        w += i
        if w in alphabet:
            prepared_word.append(w)
            w = ''
    
    for i in prepared_word:
        temp = der_by_symbol(regex, i)
        temp = temp.replace('eps.', '')
        temp = temp.replace('.eps', '')
        regex = []
        for i in temp.split('|'):
            if 'Null' not in i:
                regex.append(i)
        regex = '|'.join(regex)
    return Nullable(regex)



