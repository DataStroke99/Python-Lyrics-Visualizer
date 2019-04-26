from nltk_process import *


phone_dict = nltk.corpus.cmudict.dict()
pattern =  '(?m)^\[.*\n?'

def count_syllables(word):
    vowels = ("a", "e", "i", "o", "u", "A", "E", "I", "O", "U")
    if word.lower() in phone_dict:
        return max([len([y for y in x if (y[-1].isdigit())]) for x in phone_dict[word.lower()]])
    else:
        return sum(word.count(c) for c in vowels)






def last_word(line):
    return get_the_nth_word(line,-1)



def get_the_nth_word(line,pos):
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(line)

    if not words:
        raise ValueError('The given line is empty')

    return words[pos]



def possible_phone(word):
    if word not in phone_dict:
        return []
    return phone_dict[word]



def syllables(word):
    phones_list = possible_phone(word)

    if not phones_list:
        return []

    phones = phones_list[0]

    syllables = []
    syllable = ""

    for phone in phones:
        if phone[-1].isdigit():
            syllable += phone[:-1].lower()
            syllables.append(syllable)
            syllable = ""
        else:
            syllable += phone.lower()

    if syllable:
        syllables.append(syllable)

    return syllables



def line_similarity(first_line, second_line):
    first_compare = last_word(first_line)
    second_compare = last_word(second_line)

    return word_similarity(first_compare, second_compare)


def word_similarity(first_word, second_word, start_phone=None, end_phone=None):
    first_phones = possible_phone(first_word)
    second_phones = possible_phone(second_word)

    if not first_phones or not second_phones:
        return 0

    first_phones = first_phones[0]
    second_phones = second_phones[0]

    first_range = first_phones[start_phone:end_phone]
    second_range = second_phones[start_phone:end_phone]

    first_range = first_range[::-1]
    second_range = second_range[::-1]

    if len(first_range) > len(second_range):
        first_range, second_range = second_range, first_range

    hits = 0
    total = len(first_range)

    for idx, phone in enumerate(first_range):
        other_phone = second_range[idx]

        if phone == other_phone:
            hits += 1

            # Phones with emphasis are better matches, weight them more
            if phone[-1].isdigit():
                hits += 1
                total += 1

    return hits / total





def clear_cluter(lyric):
    res = re.sub(pattern ,'', str(lyric))
    return res




















'''


def find_artist(song_n,artist_name):
    try:
        search_url = base_url+search+song_n
        response = requests.get(search_url,headers = header,verify=False)
        json = response.json()
        song_info = None
        for hit in json['response']['hits']:
            if hit['result']['primary_artist']['name'] ==artist_name:
                song_info = hit
                break
            else:
                print("Artist does not exists")
        if song_info:
            song_api_path = song_info['result']['api_path']
            return lyrics_fetch(song_api_path)
    except:
        print('an error occured')


def start():
    lines = []
    artist = input("Input the Artist you want Lyrics of: ")
    lines = get_lyrics(artist)
    lines = '\n'.join(lines)
    #print(lines)
    return lines





def tokenize(lines):
    rx = re.compile(u"[^\wåÅäÄöÖéÉ'’\.\?!\n]+")
    line = [re.sub(rx,' ', str(i)) for i in lines]
    line = ''.join(line)
    print(line)
    tokens = [word_tokenize(i) for i in line]
    #print(tokens)
    return tokens



































def tail_rhyme():
    for sent in range(0, len(song_list)):
        print(lines[sent])
        print(lines[sent].split())


def get_word(line,position):
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(line)
    print(words)


    return words[position]

def last_word(line):
    return get_word(line,-1);



def possible_phones(word):
    phone_dictionary = nltk.corpus.cmudict.dict()

    if word not in phone_dictionary:
        return []

    return phone_dictionary[word]


def syllables(word):
    phones_list = possible_phones(word)
    if not phones_list:
        return []
    phones = phones_list[0]
    syllables = []
    syllable = ""
    for phone in phones:
        if phone[-1].isdigit():
            syllable += phone[:-1].lower()
            syllables.append(syllable)
            syllable = ""
        else:
            syllable += phone.lower()
    if syllable:
        syllables.append(syllable)
    return syllables'''












