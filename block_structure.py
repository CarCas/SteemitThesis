# OPERATIONS
from typing import List


class Vote:
    def __init__(self, voter="", author="", permlink="", weight=-1):
        self.voter = voter
        self.author = author
        self.permlink = permlink
        self.weight = weight

    def print(self):
        print("V")
        print("voter: " + self.voter)
        print("auth: " + self.author)
        print("perml: " + self.permlink)
        print("w: " + str(self.weight))

    def get_voter(self):
        return self.voter

    def get_author(self):
        return self.author

    def get_permlink(self):
        return self.permlink

    def get_weight(self):
        return self.weight


class Comment:
    votes_obtained = 0
    weights_obtained = 0

    def __init__(self, parent_author="", parent_permlink="", author="",
                 permlink="", title="", body="", json_metadata=""):
        self.parent_author = parent_author
        self.parent_permlink = parent_permlink
        self.author = author
        self.permlink = permlink
        self.title = title
        self.body = body
        self.json_metadata = json_metadata

    def get_votes(self):
        return self.votes_obtained

    def add_vote(self):
        self.votes_obtained += 1

    def get_weights(self):
        return self.weights_obtained

    def add_weight(self, w):
        self.weights_obtained += w

    def print(self):
        print("C")
        print("par_auth: " + self.parent_author)
        print("par_perml: " + self.parent_permlink)
        print("auth: " + self.author)
        print("perml: " + self.permlink)
        print("title: " + self.title)
        print("body: " + self.body)
        print("json_mt: " + self.json_metadata)


class CustomJsonFollow:
    # required_posting_auths not needed, since it is always a list of 1 element equal to the follower identifier
    def __init__(self, follower="", following="", what=None, required_posting_auths=None):
        self.follower = follower
        self.following = following
        self.what = what
        self.what = [it.strip() for it in self.what]
        self.required_posting_auths = required_posting_auths
        self.required_posting_auths = [it.strip() for it in self.required_posting_auths]

    def get_follower(self):
        return self.follower

    def get_following(self):
        return self.following

    def get_what(self):
        return self.what

    def get_required_auths(self):
        return self.required_posting_auths

    def print(self):
        print("F")
        print("follower: " + self.follower)
        print("following: " + self.following)
        if len(self.what) > 0:
            print("what: ")
            for w in self.what:
                print(w)
        else:
            print("what: []")
        if len(self.required_posting_auths) > 0:
            print("req_auths: ")
            for ra in self.required_posting_auths:
                print(str(ra))
        else:
            print("req_auths: []")


class CustomJsonReblog:
    def __init__(self, account="", author="", permlink="", req_posting_auths=None):
        self.account = account
        self.author = author
        self.permlink = permlink
        self.req_posting_auths = req_posting_auths
        self.req_posting_auths = [it.strip() for it in self.req_posting_auths]

    def get_account(self):
        return self.account

    def get_author(self):
        return self.author

    def get_permlink(self):
        return self.permlink

    def get_req_posting_auths(self):
        return self.req_posting_auths

    def print(self):
        print("RB")
        print("account: " + self.account)
        print("author: " + self.author)
        print("permlink: " + self.permlink)
        if len(self.req_posting_auths) > 0:
            print("req_posting_auths: ")
            for r in self.req_posting_auths:
                print(r)
        else:
            print("req_posting_auths: []")


class Card:

    cards = []

    def __init__(self, cards=None, price=-1, fee_pct=-1):
        self.cards = cards
        self.price = price
        self.fee_pct = fee_pct

    def get_cards(self):
        return self.cards

    def get_price(self):
        return self.price

    def get_fee_pct(self):
        return self.fee_pct

    def print(self):
        print("CARD")
        if len(self.cards) > 0:
            for r in self.cards:
                print(r)
        else:
            print("[]")
        print("price: " + str(self.price))
        print("fee_pct: " + str(self.fee_pct))


class CustomJsonSellCards:
    cards = []

    def __init__(self, req_posting_auths=""):
        self.req_posting_auths = req_posting_auths

    def append(self, card=Card()):
        self.cards.append(card)

    def get_req_posting_auths(self):
        return self.req_posting_auths

    def print(self):
        print("SM_SELL")
        for c in self.cards:
            c.print()


class VestingShares:
    def __init__(self, amount="", precision=-1, nai=""):
        self.amount = amount
        self.precision = precision
        self.nai = nai

    def print(self):
        print("amount: " + self.amount)
        print("prec: " + str(self.precision))
        print("nai: " + str(self.nai))


class Transfer:
    def __init__(self, _from="", _to="", _amount=-1, _memo=""):
        self._from_ = _from
        self._to_ = _to
        self._amount_ = _amount
        self._memo_ = _memo

    @property
    def from_(self):
        return self._from_

    @property
    def to_(self):
        return self._to_

    @property
    def memo(self):
        return self._memo_

    @property
    def amount(self):
        return self._amount_

    def print(self):
        print("TR")
        print("from: " + self._from_)
        print("to: " + self._to_)
        print("amount: " + str(self._amount_))
        print("memo: " + self._memo_)


class TransferToVesting:
    def __init__(self, _from="", _to="", _amount=-1):
        self._from = _from
        self._to = _to
        self._amount = _amount

    def print(self):
        print("TR_TO_V")
        print("from: " + self._from)
        print("to: " + self._to)
        print("amount: " + str(self._amount))


class WithdrawVesting:
    def __init__(self, account="", vesting_shares=-1):
        self.account = account
        self.vesting_shares = vesting_shares

    def print(self):
        print("WITHDRAW")
        print("account: " + self.account)
        print("v_shares: " + str(self.vesting_shares))


class LimitOrderCreate:
    def __init__(self, owner="", orderid=-1, amount_to_sell=-1, min_to_receive=-1, fillorkill=False, expiration=""):
        self.owner = owner
        self.orderid = orderid
        self.amount_to_sell = amount_to_sell
        self.min_to_receive = min_to_receive
        self.fillorkill = fillorkill
        self.expiration = expiration

    def print(self):
        print("LO_CREATE")
        print("owner: " + self.owner)
        print("orderid: " + str(self.orderid))
        print("amount_to_sell: " + str(self.amount_to_sell))
        print("min_to_rcv: " + str(self.min_to_receive))
        print("f/kill: " + str(self.fillorkill))
        print("expiration: " + self.expiration)


class LimitOrderCancel:
    def __init__(self, owner, orderid):
        self.owner = owner
        self.orderid = orderid

    def print(self):
        print("LO_CANCEL")
        print("owner: " + self.owner)
        print("orderid: " + self.orderid)


class Price:
    def __init__(self, base=VestingShares(), quote=VestingShares()):
        self.base = base
        self.quote = quote

    def print(self):
        print("PRICE")
        print("base: ")
        if type(self.base) is not str:
            self.base.print()
        else:
            print(self.base)
        print("quote: ")
        if type(self.quote) is not str:
            self.quote.print()
        else:
            print(self.quote)


class FeedPublish:
    def __init__(self, publisher="", exchange_rate=Price()):
        self.publisher = publisher
        self.exchange_rate = exchange_rate

    def print(self):
        print("FEED_PUBLISH")
        print("pub: " + self.publisher)
        print("exch_rate: ")
        if type(self.exchange_rate) is not str:
            self.exchange_rate.print()
        else:
            print(self.exchange_rate)


class Convert:
    def __init__(self, owner="", requestid=-1, amount=VestingShares()):
        self.owner = owner
        self.requestid = requestid
        self.amount = amount

    def print(self):
        print("CONVERT")
        print("owner: " + self.owner)
        print("req_id: " + str(self.requestid))
        print("amount: ")
        if type(self.amount) is not str:
            self.amount.print()
        else:
            print(self.amount)


class Account:
    def __init__(self, weight_treshold=-1, account_auths: List[str] = List[str], key_auths: List[str] = List[str]):
        self.weight_treshold = weight_treshold
        self.account_auths = account_auths
        self.key_auths = key_auths

    def prints(self):
        print("ACC")
        print("w_trhold: " + str(self.weight_treshold))
        if len(self.account_auths) > 0:
            print("acc_auths: ")
            for a in self.account_auths:
                print(str(a))
        else:
            print("acc_auths: []")
        if len(self.key_auths) > 0:
            print("key_auths: ")
            for n, v in self.key_auths:
                print(str(n) + ", " + str(v))
        else:
            print("key_auths: []")


class AccountCreate:
    def __init__(self, fee="", creator="", new_account_name="", owner=Account(),
                 active=Account(), posting=Account(), memo_key="", json_metadata=""):
        self.json_metadata = json_metadata
        self.memo_key = memo_key
        self.posting = posting
        self.active = active
        self.owner = owner
        self.new_account_name = new_account_name
        self.creator = creator
        self.fee = fee

    def print(self):
        print("ACC_CREAT")
        print("fee: " + self.fee)
        print("creator: " + self.creator)
        print("new_acc_name: " + self.new_account_name)
        print("owner: ")
        if type(self.owner) is not str:
            self.owner.prints()
        else:
            print(self.owner)
        print("active: ")
        if type(self.active) is not str:
            self.active.prints()
        else:
            print(self.active)
        print("posting: ")
        if type(self.posting) is not str:
            self.posting.prints()
        else:
            print(self.posting)


class CreateClaimedAccount:
    def __init__(self, creator="", new_account_name="", owner=Account(), active=Account(),
                 posting=Account(), memo_key="", json_metadata=""):
        self.creator = creator
        self.new_account_name = new_account_name
        self.owner = owner
        self.active = active
        self.posting = posting
        self.memo_key = memo_key
        self.json_metadata = json_metadata

    def print(self):
        print("ACC_CLAIM_ACC")
        print("creat: " + self.creator)
        print("new_acc_named: " + self.new_account_name)
        print("owner: ")
        if type(self.owner) is not str:
            self.owner.prints()
        else:
            print(self.owner)
        print("active: ")
        if type(self.active) is not str:
            self.active.prints()
        else:
            print(self.active)
        print("posting: ")
        if type(self.posting) is not str:
            self.posting.prints()
        else:
            print(self.posting)
        print("memo_key: " + self.memo_key)
        print("json_mt: " + self.json_metadata)


class ClaimAccount:
    def __init__(self, fee=VestingShares(), creator="", extensions=None):
        self.fee = fee
        self.creator = creator
        self.extensions = extensions

    def print(self):
        print("fee: ")
        if type(self.fee) is not str:
            self.fee.print()
        else:
            print(self.fee)
        print("creator: " + self.creator)
        if len(self.extensions) > 0:
            print("extensions: ", end=" ")
            for e in self.extensions:
                print(e, end=" ")
            print()
        else:
            print("extensions: []")


class AccountUpdate:
    def __init__(self, account="", owner=Account(), active=Account(), posting=Account(), memo_key="", json_metadata=""):
        self.account = account
        self.owner = owner
        self.active = active
        self.posting = posting
        self.memo_key = memo_key
        self.json_metadata = json_metadata

    def print(self):
        print("account: " + self.account)
        if type(self.owner) is not str:
            print("owner: ")
            self.owner.prints()
        else:
            print(self.owner)
        if type(self.active) is not str:
            print("active: ")
            self.active.prints()
        else:
            print("active: " + str(self.active))
        print("posting: ")
        if type(self.posting) is not str:
            self.posting.prints()
        else:
            print(self.posting)
        print("memo_key: " + self.memo_key)
        print("json_metadata: " + self.json_metadata)


class TransactionBlockStructure:

    operations = []
    transaction_id = ""
    transaction_num = -1

    def get_operations(self):
        return self.operations

    def set_operations(self, ops):
        if len(ops) > 0:
            self.operations = ops

    def get_transaction_id(self):
        return self.transaction_id

    def set_transaction_id(self, tid=""):
        self.transaction_id = tid

    def get_transaction_num(self):
        return self.transaction_num

    def set_transaction_num(self, trn):
        self.transaction_num = trn

    def print(self):
        print("TRANSACTION BLOCK")
        for op in self.operations:
            op.print()
        print("transaction_id: " + self.transaction_id)
        print("transaction_num: " + str(self.transaction_num))


# TRANSACTIONS AND BLOCKS


class Transaction:
    def __init__(self, transaction_id="", transaction_block: TransactionBlockStructure = None):
        self.transaction_id = transaction_id
        self.transaction_block = TransactionBlockStructure()
        self.transaction_block.set_operations((transaction_block.get_operations()))
        self.transaction_block.set_transaction_id((transaction_block.get_transaction_id()))
        self.transaction_block.set_transaction_num((transaction_block.get_transaction_num()))

    def get_transaction_id(self):
        return self.transaction_id

    def set_transaction_id(self, tid):
        self.transaction_id = tid

    def get_transaction_block(self):
        return self.transaction_block

    def set_transaction_block(self, tbl: TransactionBlockStructure):
        self.transaction_block.set_operations((tbl.get_operations()))
        self.transaction_block.set_transaction_id((tbl.get_transaction_id()))
        self.transaction_block.set_transaction_num((tbl.get_transaction_num()))

    def print(self):
        print("TRANSACTION")
        print("transaction_id: " + self.transaction_id)
        print("transaction_block: ")
        self.transaction_block.print()


class BlockStructure:
    transactions: List[Transaction] = []
    timestamp = ""
    transaction_block = None
    witness_name = ""

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_transactions(self):
        return self.transactions

    def set_transactions(self, transactions):
        self.transactions = transactions

    def get_witness_name(self):
        return self.witness_name

    def set_witness_name(self, witness_name):
        self.witness_name = witness_name

    def print_block(self):
        print("BLOCK")
        print("timestamp: " + self.timestamp)
        print("transactions: ")
        print("Num transactions: " + str(len(self.transactions)))
        for ts in self.transactions:
            ts.print()
        print("witness_name: " + self.witness_name)
