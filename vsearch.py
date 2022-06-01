def search4vowels(phrase: str) -> set:
    """ возвращает гласные, найденные во введеном слове"""
    vowels = set('aeiou')
    return vowels.intersection(set(phrase))


def search4letters(phrase: str, letters: str = 'aeiou') -> set:
    """ возвращает множество букв из 'letters',
                    найденных в указанной фразе"""
    return set(letters).intersection(set(phrase))
































