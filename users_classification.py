import collections
import copy
import json
import os
import re
import sys
from typing import Set, List, Dict

import nltk
import pycountry as pycountry
import stop_words
from nltk import chain, download
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

import block_structure
import parsing_blocks
import user_structure

WHALE_COMMENTS = "./cmt/whale/"
SHARK_COMMENTS = "./cmt/shark/"
DOLPHIN_COMMENTS = "./cmt/dolphin/"
MINNOW_COMMENTS = "./cmt/minnow/"
PLANKTON_COMMENTS = "./cmt/plankton/"

FREQUENCY_PATH = "./frequency/freq."

USERS_PATH = "users.dat"
COMMENTS_PATH = "comments.dat"


class UsersClassification:

    def __init__(self, path="steem_first200"):
        download('stopwords')
        self.blocks: List[block_structure] = parsing_blocks.parsing_blocks(path=path)
        self.users: List[user_structure.User] = []
        self.foreign_users: Set[user_structure.User] = set()
        self.whale_users: List[user_structure.User] = []
        self.shark_users: List[user_structure.User] = []
        self.dolphin_users: List[user_structure.User] = []
        self.minnow_users: List[user_structure.User] = []
        self.plankton_users: List[user_structure.User] = []
        self._lemmas: Dict[str, List[str]] = dict()
        self._lemmas_for_categories: Dict[str, List[str]] = {"whale": [], "shark": [], "dolphin": [],
                                                             "minnow": [], "plankton": []}
        self.word_net_lemmatizing: WordNetLemmatizer = WordNetLemmatizer()
        self._stop_words: Set[str] = set(chain.from_iterable(stop_words.get_stop_words(lang)
                                                             for lang in stop_words.AVAILABLE_LANGUAGES))
        print("FINISHED INIT")

    @property
    def whales(self) -> List[user_structure.User]:
        return self.whale_users

    @property
    def sharks(self) -> List[user_structure.User]:
        return self.shark_users

    @property
    def dolphins(self) -> List[user_structure.User]:
        return self.dolphin_users

    @property
    def minnows(self) -> List[user_structure.User]:
        return self.minnow_users

    @property
    def plankton(self) -> List[user_structure.User]:
        return self.plankton_users

    @property
    def lemmas(self) -> Dict[str, List[str]]:
        return self._lemmas_for_categories

    def users_initialize_from_blocks(self):
        print("STARTED USERS INITIALIZATION")
        for b in self.blocks:
            transactions: List[block_structure.Transaction] = b.get_transactions()
            print("INSIDE BLOCK")
            for t in transactions:
                tops: block_structure.TransactionBlockStructure = t.get_transaction_block()
                for o in tops.get_operations():
                    if type(o) is block_structure.Vote:
                        v: block_structure.Vote = o
                        found = False
                        if v.author not in self.foreign_users:
                            for us in self.users:
                                # check only if the voter has voted because in the block_structure.Comment
                                # there is already the votes obtained by others users.
                                if v.get_voter() == us.name:
                                    found = True
                                    us.append_given_votes(v.get_weight())
                                    break
                            if not found:
                                us = user_structure.User(v.get_voter())
                                us.append_given_votes(v.get_weight())
                                self.users.append(us)
                    elif type(o) is block_structure.Comment:
                        c: block_structure.Comment = o
                        found = False
                        foreign = False
                        for us in self.users:
                            if c.author == us.name:
                                found = True
                                print("FOUND")
                                cmt = c.title + " " + c.body
                                b = TextBlob(cmt)
                                iso_code = b.detect_language()
                                if pycountry.languages.get(alpha_2=iso_code).name not in ("en", "eng", "English"):
                                    if c.author not in self.foreign_users:
                                        self.foreign_users.add(c.author)
                                        foreign = True
                                    break
                                else:
                                    cmt = re.sub(r"[^a-zA-Z0-9:/.@()\[\]\-$? ]+", "", cmt)
                                    cmt = re.sub(r"([\[\]()]+)", " ", cmt)
                                    cmt = self.remove_stopwords(cmt)
                                    lems = map(bytes.decode, self.lemmatize(cmt))
                                    print("BEFORE COMMENT: " + cmt)
                                    if us.name not in self._lemmas:
                                        self._lemmas[us.name] = []
                                    i = 0
                                    print(len(list(lems)))
                                    for _ in range(len(list(lems))):
                                        el = yield next(lems)
                                        self._lemmas[us.name].append(next(lems))
                                        print(str(i) + ": " + str(len(list(lems))))
                                        i += 1
                                    print("MIDDLE: " + ' '.join(ln for ln in self._lemmas[us.name]))
                                    tmp_lem = copy.deepcopy(list(lems))
                                    cmt = ' '.join(tmp_lem)
                                    print("LEN _LEMMAS AFTER: " + str(len(list(lems))))
                                    print("AFTER COMMENT: " + cmt)
                                    us.comments.append(cmt)
                                    us.append_obtained_votes(c.weights_obtained)
                                    break
                        if not found and not foreign:
                            cmt = c.title + " " + c.body
                            cmt = re.sub(r"[^a-zA-Z0-9:/.@()\[\]\-$? ]+", "", cmt)
                            cmt = re.sub(r"([\[\]()]+)", " ", cmt)
                            cmt = self.remove_stopwords(cmt)
                            lems = map(bytes.decode, self.lemmatize(cmt))

                            cmt = ' '.join(lems)
                            us = user_structure.User(c.author)
                            us.comments.append(cmt)
                            us.append_obtained_votes(c.weights_obtained)
                            self._lemmas[us.name] = list(lems)
                            self.users.append(us)
                    elif type(o) is block_structure.CustomJsonFollow:
                        f: block_structure.CustomJsonFollow = o
                        found = False
                        if f.following not in self.foreign_users:
                            for us in self.users:
                                if f.follower.__eq__(us.name):
                                    found = True
                                    us.followers.append(f.following)
                                    break
                            if not found:
                                us = user_structure.User(f.follower)
                                us.followers.append(f.following)
                                self.users.append(us)
                    elif type(o) is block_structure.Transfer:
                        tr: block_structure.Transfer = o
                        found_from = False
                        found_to = False
                        if (tr.from_ not in self.foreign_users) and (tr.to_ not in self.foreign_users):
                            for us in self.users:
                                if tr.from_.__eq__(us.name):
                                    found_from = True
                                    us.append_given_amount(tr.amount)
                                if tr.to_.__eq__(us.name):
                                    found_to = True
                                    us.append_obtained_amount(tr.amount)
                                if found_from and found_to:
                                    break
                            if found_from and not found_to:
                                us = user_structure.User(tr.to_)
                                us.append_obtained_amount(tr.amount)
                                self.users.append(us)
                            elif found_to and not found_from:
                                us = user_structure.User(tr.from_)
                                us.append_given_amount(tr.amount)
                                self.users.append(us)
                            elif not found_from and not found_to:
                                u1 = user_structure.User(tr.from_)
                                u1.append_given_amount(tr.amount)
                                self.users.append(u1)
                                u2 = user_structure.User(tr.to_)
                                u2.append_obtained_amount(tr.amount)
                                self.users.append(u2)
        return True

    # In this function there is the initialization of the fields of the users
    # steem power, reputation and reputation class and the removal of all the
    # stop words of all the words that are in the comments of the user
    def users_classification(
            self,
            path="./accounts/accountsInfoNew.json"
    ) -> None:
        print("Starting users classification")
        with open(path, 'r', encoding="UTF-8") as f:
            # The formula for calculating Steem Power is as follows:
            # total_vesting_fund_steem * (user's vesting_shares / total_vesting_shares)
            for line in f:
                data: Dict[str, str] = json.loads(line)
                for us in self.users:
                    if us.name.__eq__(data['name']):
                        us.set_reputation(data['reputation'])
                        us.info = data
                        us.set_steem_power_by_vs(data['vesting_shares'].split(' ')[0])
                        if us.get_reputation_class() == "WHALE":
                            self.whale_users.append(us)
                            if us.name in self._lemmas:
                                self._lemmas_for_categories["whale"] += self._lemmas[us.name]
                        elif us.get_reputation_class() == "SHARK":
                            self.shark_users.append(us)
                            if us.name in self._lemmas:
                                self._lemmas_for_categories["shark"] += self._lemmas[us.name]
                        elif us.get_reputation_class() == "DOLPHIN":
                            self.dolphin_users.append(us)
                            if us.name in self._lemmas:
                                self._lemmas_for_categories["dolphin"] += self._lemmas[us.name]
                        elif us.get_reputation_class() == "MINNOW":
                            self.minnow_users.append(us)
                            if us.name in self._lemmas:
                                self._lemmas_for_categories["minnow"] += self._lemmas[us.name]
                        elif us.get_reputation_class() == "PLANKTON":
                            self.plankton_users.append(us)
                            if us.name in self._lemmas:
                                self._lemmas_for_categories["plankton"] += self._lemmas[us.name]
                                print("LEMMAS: " + str(len(self._lemmas[us.name])))
                                print("LEMMAS_CAT: " + str(len(self._lemmas_for_categories["plankton"])))
                        else:
                            sys.stderr.write("ERROR: USER NOT CLASSIFIED")
                            return
                        self.users.remove(us)
                        # if us.name in self._lemmas:
                        #    del self._lemmas[us.name]
                        break

    @staticmethod
    def write_on_file(path, list_users):
        if len(list_users) > 0:
            os.makedirs(os.path.dirname(path + USERS_PATH), exist_ok=True)
            os.makedirs(os.path.dirname(path + COMMENTS_PATH), exist_ok=True)
            with open(path + USERS_PATH, 'w') as f:
                f.write(''.join(us.name + "\n" for us in list_users))
            with open(path + COMMENTS_PATH, "w") as f:
                for us in list_users:
                    f.write(''.join(cmt + "\n" for cmt in us.get_comments()))
                    # for cmt in us.get_comments():
                    #    f.write(cmt + "\n")
                    f.write("\n")
                f.write("\n")

    @staticmethod
    def write_frequency(path: str, frequency: dict):
        print(path)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, 'w') as f:
            for k, v in frequency.items():
                f.write("w: %s, \t\t\t fq: %s\n" % (k, v))

    def classification_write(self):
        print("Starting classification write")
        self.write_on_file(WHALE_COMMENTS + "whale", self.whale_users)
        self.write_on_file(SHARK_COMMENTS + "shark", self.shark_users)
        self.write_on_file(DOLPHIN_COMMENTS + "dolphin", self.dolphin_users)
        self.write_on_file(MINNOW_COMMENTS + "minnow", self.minnow_users)
        self.write_on_file(PLANKTON_COMMENTS + "plankton", self.plankton_users)
        for k, v in self._lemmas_for_categories.items():
            print("CAT: " + k)
            c = collections.Counter(self._lemmas_for_categories[k])
            print(c.most_common(10))
            self.write_frequency(FREQUENCY_PATH + k + ".dat", c)

    def remove_stopwords(self, comment):
        comment = comment.lower()
        for s in self._stop_words:
            comment = re.sub(r"\b" + s.lower() + r"\b", '', comment)
        comment = re.sub(" +", " ", comment)
        return comment

    @staticmethod
    def get_wordnet_pos(word):
        # Map POS tag to first character lemmatize() accepts
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    def lemmatize(self, comment):
        # cmt = nltk.word_tokenize(comment)
        cmt = comment.split()
        return [self.word_net_lemmatizing
                    .lemmatize(word)
                    .encode('UTF-8').strip()
                for word in cmt]

    def start_process(self, path_accounts):
        if self.users_initialize_from_blocks():
            self.users_classification(path_accounts)
            self.classification_write()


if __name__ == '__main__':
    path_to_pass = "./steem_first10"  # steem.blockchain_14
    path_acc = "./accounts/accountsInfoNew.json"
    uc = UsersClassification(path=path_to_pass)
    uc.start_process(path_accounts=path_acc)
