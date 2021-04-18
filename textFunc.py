from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag


class MyTag:
    tag_name = ""
    ass_tokens = []

    # initialize the class to contain a list of tokens for the tag
    def __init__(self, tag_name, ass_tokens):
        self.tag_name = tag_name
        self.ass_tokens = ass_tokens


"""
This section contains a list of hard-coded predefined tags
"""
# TODO: make more of these
tag_list = []
#VISUAL HALLUCINATIONS TAG
visual_tokens = ['big', 'shadow', 'aura', 'color', 'depth', 'detail', 'distort', 'geometr', 'hallucin',
                 'monster', 'movement', 'perspect', 'reflect', 'scari', 'shape', 'shape', 'shimmer', 'shine',
                 'spot', 'wavi', 'wonder']
visual_hallucinations = MyTag("Visual Hallucinations", visual_tokens)

#AUDIO HALLUCINATIONS TAG
audio_tokens = ['argu', 'listen', 'loud', 'quiet', 'verbal', 'ear', 'groan', 'imagin', 'melodi', 'moan',
                'music', 'narrat', 'song', 'sound', 'speak', 'voic', 'whisper']
audio_hallucinations = MyTag("Audio Hallucinations", audio_tokens)

#EGO DEATH TAG
ego_tokens = ['ego', 'death', 'conscious', 'fantasi', 'nihilist', 'pych', 'regret', 'sad', 'small', 'anxieti',
              'fear', 'feel', 'ident', 'insignific', 'person', 'reason', 'scale', 'self', 'valu', 'worth']
ego_death = MyTag("Ego Death", ego_tokens)

# NATURE TAG
nature_tokens = ['tree', 'bauti', 'fish', 'fresh', 'green', 'leaf', 'natur', 'ocean', 'air', 'beach', 'bird',
                 'breath', 'bug', 'camp', 'dirt', 'harmoni', 'hike', 'life', 'outdoor', 'outsid', 'park', 'peac',
                 'plant', 'water', 'world']
nature = MyTag("Nature", nature_tokens)

#TIME PERCEPTION TAG
time_tokens = ['long', 'quick', 'short', 'clock', 'percept', 'race', 'speed', 'time', 'slow']
time_perception = MyTag("Time Perception", time_tokens)

# APPEND ALL OF THE TAGS TO THE LIST
tag_list.append(visual_hallucinations)
tag_list.append(audio_hallucinations)
tag_list.append(ego_death)
tag_list.append(nature)
tag_list.append(time_perception)


"""
Above this section is a list of hard-coded predifined tags
"""


def compile_to_tags(input_list, tag_list):
    """
    This function does the compiling for all possible tags.
    :param input_list: list of tokens
    :param tag_list: list of predefined tags
    :return:
    """
    tag_total_list = []

    for tag in tag_list:
        for token in tag.ass_tokens:
            # if token is in the input list of tokens
            if token in input_list:
                # if the token is not already in the list
                tag_total_list.append(tag.tag_name)

    # keeping parallel records of the tags and their numbers
    tag_counter = []
    tag_names = []

    for name in tag_total_list:
        if name in tag_names:
            tag_counter[tag_names.index(name)] += 1
        else:
            tag_counter.append(1)
            tag_names.append(name)

    tag_list_final = []
    if len(tag_counter) > 0:
        for x in range(0, 5):
            max_value = max(tag_counter)
            if max_value != 0:
                max_index = tag_counter.index(max_value)
                tag_list_final.append(tag_names[max_index])
                tag_counter[max_index] = 0

    return tag_list_final

def text_tokenizer(input_text):
    """
    This should be the function that takes in the basic string for people's reports.
    Tokenizes the string, then sorts them.
    :param input_text:
    :return:
    """

    tokenized_input_text = word_tokenize(input_text)
    sorted_tokens = sorted(tokenized_input_text)
    return sorted_tokens


def remove_duplicates(input_text):
    """
    Removes duplicate elements from a list/array
    :param input_text:
    :return:
    """
    simplified_array = []
    for w in input_text:
        if w not in simplified_array:
            simplified_array.append(w)

    return simplified_array


def text_normalizer(input_text):
    """
    normalizes words.
    TODO: understand how this works lmao
    :param input_text:
    :return:
    """
    ps = PorterStemmer()

    stemmed_words = []
    for w in input_text:
        stemmed_words.append(ps.stem(w))

    return stemmed_words


def remove_stop_words(input_text):
    """
    This function only takes in already tokenized sentences.
    Gives weird results if not normalized.
    Also removing punctuation.
    :param input_text:
    :return:
    """
    stop_words = set(stopwords.words("english"))
    # print("stop words:", stop_words)
    filtered_sent = []
    for w in input_text:
        if w not in stop_words:
            if w.isalpha():
                filtered_sent.append(w)
    return filtered_sent


def pos_tagging(input_text):
    """
    tags all of the words in the string array
    :param input_text:
    :return:
    """
    tagged_text = pos_tag(input_text)
    return tagged_text


def filter_tag(input_text, tag):
    """
    filters out all non adjective words
    :param input_text:
    :return:
    """
    filtered_list = []
    for w in input_text:
        if w[1] == tag:
            filtered_list.append(w)

    return filtered_list


def simplify_to_word(input_text):
    """
    removes the tags from a word list
    :param input_text:
    :return:
    """
    simplified_list = []
    for w in input_text:
        simplified_list.append(w[0])
    return simplified_list


def undo_lem(input_text, original_array):

    # this function undoes lemitization
    # by comparing the original string to
    # the post-lem forms through the originally imported function
    ps = PorterStemmer()
    output_text = []

    for m in original_array:
        if ps.stem(m) in input_text:
            output_text.append(m.upper())
    return output_text





"""---below this is the main function---"""


def rivers_func(text):

    # step 1: tokenize sentence into words.
    tokenized_text = text_tokenizer(text)
    # step 1.5: remove duplicates
    # TODO: This step may be considered unnecessary or detrimental if repeats are valuable
    tokenized_text = remove_duplicates(tokenized_text)

    # step 2.1: remove stop words round one
    tokenized_text = remove_stop_words(tokenized_text)

    # step 2.2: normalize words
    normalized_words = text_normalizer(tokenized_text)

    # step 3: remove stop words
    post_stop_text = remove_stop_words(normalized_words)

    # step 4: tag words for part of speech
    tagged_words = pos_tagging(post_stop_text)

    # step 5a: filter adjectives only
    adjectives = filter_tag(tagged_words, "JJ")

    # step 5b: filter nouns only
    nouns = filter_tag(tagged_words, "NN")

    # step 5b: filter verb only
    verbs = filter_tag(tagged_words, "VB")

    # step 6: simplify list to only words, no tag
    simple_words = simplify_to_word(adjectives + nouns + verbs)

    # step 7: compile to tags
    compiled_tags = compile_to_tags(simple_words, tag_list)

    # step 8: undo lemmitization
    # renormalized = undo_lem(simple_words, tokenized_text)

    # print("Original text:", text)
    # print("Tokenized text:", tokenized_text)
    # print("Normalized text:", normalized_words)
    # print("Text after stop:", post_stop_text)
    # print("Text after tag:", tagged_words)
    # print("Only adjectives:", adjectives)
    # print("Only nouns:", nouns)
    # print("Only verbs:", verbs)
    # print("Simple adj:", simple_adj)
    # print("renormalized:", renormalized)

    output_text = []
    x = 0
    while x < 5 and x < len(compiled_tags):
        output_text.append(compiled_tags[x])
        x += 1

    return output_text


# ORIGINAL BLOCK OF TEXT USED TO TEST FUNCTION
# text = "This night was crazy. I had been drinking a lot, it was Spring 2016, i went to 2 different parties that night, and was socially exhausted. We went back to Kennedy's dorm in Oakes and i took 3 or 4 mushrooms. At first, i felt nothing. 20 minutes later, the walls began shimmering a bit and I began hysterically laughing for about 20 more minutes. It was 3am, dark, cramped apartment, and I did not feel physically or emotionally comfortable. Then I began crying. I was hysterical. I was in so much pain during my trip. I was full of painful, infinite regret about not doing more slam poetry when I was in high school. I cried so hard, so wet, I thought I was dying. In fact, I eventually crawled out of Kennedy's room and into the living room, and layed down on the couch, begging the sunshine to return because I felt like I was spiraling into a black hole of sadness and regret. I peered at the windows and just held on, tempted to call my parents, because I felt as if I was dying, like my failures were staring at me and I could not handle it. Eventually, the sunshine returned, the morning glow, so beautiful. I walked outside with connor and i gazed with wonder at the dew covered tree outside his apartment, commenting to connor that it was the most beautiful, fullness of a tree I had ever seen. It shimmered, i could see the aura of the tree separated at the edge of its frame from the tree itself, and i saw colors more vividly than I ever had. The colors and the due and the morning light were so much more PRESENT. That is how I would describe it. The greens were greener, the tree was tree-er, the essence of the plants and the dew took off their clothes and were naked but dignified infront of me, but yet I felt like the one exposed in the heavenly fullness of naked, natural nature. I felt out of place and inferior in the presence of plants. Also, the walls inside shimmered and became wavy and appeared purple. I had the shroomy giggles. I walked back to my apartment, and the trees listened to me and made their essence known, and I was taken aback. I decided I did not want to live this way, full of regret everyday, and that if I had to decide how to live my life, if I could just kill the ego and forgive/love myself, I would feel so much better every day and would be so much happier."
# gonna add some stuff to the text here.
# text = "I was warm and cold. I had visual hallucinations all night. Sometimes it was scary, other times it was peaceful " + text


# VISUAL HALLUCINATIONS TEST
# text = "visual seeing colors aura shine shimmer wave distort reflect imaginary scary hallucinate spots shapes monster big small wonder shape geometric shadows depth perspective movement detail"
# AUDIO HALLUCINATIONS TEST
# text = "audio hear imagine voices sounds loud quiet whisper moan groan ear listen music song tune melody thought arguing narrating verbal speaking"
# EGO DEATH TEST
# text = "ego death feel small identity self ego consciousness insignificant nihilist personal trance memory reason fantasy existence scale pyche community sense transend sadness regret perception worth existence fear anxiety value"
# NATURE TAGS TEST
# text = "water trees ocean beach air forest walk park dirt earth plants animals life breathing sense nature world peace harmony fish green fresh leaf bird bugs bautiful outside outdoors camp hike naked"
# TIME PERCEPTION TEST
# text = ""

# rivers_func(text)
