import re
import time

import pymorphy2


def range_char(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1))


isNeedWordBase = True
path = "H:/User/Documents/PythonTextAnalysis/"

if __name__ == '__main__':
    startTime = time.perf_counter()
    infile = open(path + "voyna-i-mir.txt", "r", encoding='ansi')
    lines = 0
    words = 0
    ruWords = 0
    characters = 0
    ruCharacters = 0
    dictionaryLetters = dict()
    wordBase = dict()
    morph = pymorphy2.MorphAnalyzer()

    for character in range_char('а', 'я'):
        dictionaryLetters[character] = 0

    for line in infile:
        wordsList = line.split()

        for word in wordsList:
            buffer = word.replace('ё', 'е')
            buffer = buffer.replace('Ё', 'Е')
            res = re.sub(r"[^а-яА-я]", '', buffer)
            ruCharacters += len(res)

            for character in res:
                dictionaryLetters[character.lower()] += 1

            if res != "":
                ruWords += 1

                if isNeedWordBase:
                    tmp = morph.parse(res)[0]
                    normalForm = tmp.normal_form
                    if normalForm not in wordBase:
                        wordBase[normalForm] = 1
                    else:
                        wordBase[normalForm] += 1

        lines += 1
        words += len(wordsList)
        characters += len(line)
        if words % 100 == 0:
            print('\r', end='')
            print("Обработано слов: " + str(words), end='')

    print('\r', end='')
    print("Строк: " + str(lines))
    print("Слов: " + str(words))
    print("РуСлов " + str(ruWords))
    print("Уникальных слов: " + str(len(wordBase)))
    print("Символов: " + str(characters))
    print("РуСимволов: " + str(ruCharacters))

    file = open(path + 'char.csv', 'w')
    for key, value in dictionaryLetters.items():
        file.write(key + ";" + str(value) + "\n")
    file.close()

    if isNeedWordBase:
        file = open(path + 'words.csv', 'w')
        for key, value in wordBase.items():
            file.write(key + ";" + str(value) + "\n")
        file.close()

    endTime = time.perf_counter()
    print(f"Вычисление заняло {endTime - startTime:0.4f} секунд")
