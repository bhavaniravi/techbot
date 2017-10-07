import nltk


def extract_entity_names(query):
    """
    Returns extracted entities
    :param t: nltk tree
    :return: entity list
    """
    entity_names = []
    words = nltk.word_tokenize(query.lower())
    tags = nltk.pos_tag(words)
    tags = tags
    # print(tags)
    for tag in tags:
        if tag[1] in ["JJ", "NN", "NNS", "NNP"]:
            entity_names.append(tag[0])
    print(entity_names)
    return entity_names
# class extractor():
#     chunked_sentences = []
#
#     def __init__(self, s):
#         """
#         initializing the class with the sentence which will be tokenized and chuncked
#         """
#         s = s.lower()
#
#
#     def extract_entity_names(self):
#         """
#         Returns extracted entities
#         :param t: nltk tree
#         :return: entity list
#         """
#         entity_names = []
#         tags = self.tags
#         print(tags)
#         for tag in tags:
#             if tag[1] in ["JJ", "NN", "NNS", "NNP"]:
#                 entity_names.append(tag[0])
#         print(entity_names)
#         return entity_names
#
#     def extract(self):
#         """
#         A helper function for extract_entity_names
#         :return: Entity list
#         """
#
#         return self.extract_entity_names()
