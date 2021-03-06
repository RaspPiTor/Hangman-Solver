import lzma
import re

def suggest_next(words, string, not_in='', letters='abcdefghijklmnopqrstuvwxyz'):
    length = len(string)
    blank = '[%s]' % ''.join(l for l in letters if l not in not_in + string)
    regex = ''.join(re.escape(i) if i != '_' else blank for i in string)
    regex = re.compile(regex)
    counts = dict((i, 0) for i in letters if i not in not_in)
    for word in words:
        if len(word) == length:
            if regex.fullmatch(word):
                count = words[word]
                for l in set(word):
                    counts[l] += count
    counts = [(counts[i], i) for i in counts if i not in string]
    return sorted(counts, reverse=True)

def main():
    word_dict = {}
    with open('compressed.xz', 'rb') as file:
        decompressed = lzma.decompress(file.read()).decode('utf-8')
        for line in decompressed.splitlines():
            count, words = line.split(':')
            count = int(count, 16)
            words = words.split(',')
            for i in words:
                word_dict[i] = count
    while True:
        string = input('String>>>')
        not_in = input('Letters not in>>>>')
        print('\n'.join('%s %s' % i for i in suggest_next(word_dict, string,
                                                          not_in)))
        

if __name__ == '__main__':
    main()
