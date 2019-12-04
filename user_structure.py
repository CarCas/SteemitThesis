from collections import deque

WHALE_LOWER = 350000
SHARK_LOWER = 100000
DOLPHIN_LOWER = 5000
MINNOW_LOWER = 500
PLANKTON_LOWER = 0

VS_TO_SP = 0.0005035760389197656


class User:

    def __init__(self, name):
        self.info: dict = dict()

        self.rep_class = ""
        self.steem_pow = 0
        self.rep = 25
        self.nome = name
        self.follow_ers = []
        self.comments = []
        self.given_vts = deque()
        self.obtained_vts = deque()
        self.given_amnt = []
        self.obt_amnt = []

    def set_name(self, name):
        self.nome = name

    def print(self):
        print(self.info)

    def set_info(self, info):
        self.info = info

    @staticmethod
    def compute_rep(steem_power):
        if steem_power > WHALE_LOWER:
            return "WHALE"
        if steem_power > SHARK_LOWER:
            return "SHARK"
        if steem_power > DOLPHIN_LOWER:
            return "DOLPHIN"
        if steem_power > MINNOW_LOWER:
            return "MINNOW"
        if steem_power > PLANKTON_LOWER:
            return "PLANKTON"
        else:
            return "ERROR"

    def get_reputation_class(self):
        return self.rep_class

    def set_reputation_class(self, reputation_class):
        self.rep_class = reputation_class

    def get_steem_power(self):
        return self.steem_pow

    def set_steem_power(self, sp):
        self.steem_pow = sp
        self.rep_class = self.compute_rep(self.steem_pow)

    def set_steem_power_by_vs(self, vs):
        self.steem_pow = float(vs) * VS_TO_SP
        self.rep_class = self.compute_rep(self.steem_pow)

    def get_reputation(self):
        return self.rep

    def set_reputation(self, rep):
        self.rep = int(rep)

    def get_comments(self):
        return self.comments

    def append_comment(self, cm):
        self.comments.append(cm)

    def get_given_votes(self):
        return self.given_vts

    def append_given_votes(self, given_vts):
        self.given_vts.append(given_vts)

    def get_obtained_votes(self):
        return self.obtained_vts

    def append_obtained_votes(self, obtained_vts):
        self.obtained_vts.append(obtained_vts)

    def get_given_amount(self):
        return self.given_amnt

    def append_given_amount(self, a):
        self.given_amnt.append(a)

    def get_obtained_amount(self):
        return self.obt_amnt

    def append_obtained_amount(self, a):
        self.obt_amnt.append(a)

    @property
    def get_id(self):
        return self.info['id']

    @property
    def followers(self):
        return self.follow_ers

    @followers.setter
    def followers(self, f):
        self.follow_ers.append(f)

    @property
    def name(self) -> str:
        return self.nome

    @property
    def get_owner(self):
        return self.info['owner']

    @property
    def get_active(self):
        return self.info['active']

    @property
    def get_posting(self):
        return self.info['posting']

    @property
    def get_memo_key(self):
        return self.info['memo_key']

    @property
    def get_json_metadata(self):
        return self.info['json_metadata']

    @property
    def get_proxy(self):
        return self.info['proxy']

    @property
    def get_last_owner_update(self):
        return self.info['last_owner_update']

    @property
    def get_last_account_update(self):
        return self.info['last_account_update']

    @property
    def get_created(self):
        return self.info['created']

    @property
    def get_mined(self):
        return self.info['mined']

    @property
    def get_recovery_account(self):
        return self.info['recovery_account']

    @property
    def get_last_account_recovery(self):
        return self.info['last_account_recovery']

    @property
    def get_reset_account(self):
        return self.info['reset_account']

    @property
    def get_comment_count(self):
        return self.info['comment_count']

    @property
    def get_lifetime_vote_count(self):
        return self.info['lifetime_vote_count']

    @property
    def get_post_count(self):
        return self.info['post_count']

    @property
    def get_can_vote(self):
        return self.info['can_vote']

    @property
    def get_voting_manabar(self):
        return self.info['voting_manabar']

    @property
    def get_balance(self):
        return self.info['balance']

    @property
    def get_savings_balance(self):
        return self.info['savings_balance']

    @property
    def get_sbd_balance(self):
        return self.info['sbd_balance']

    @property
    def get_sbd_seconds(self):
        return self.info['sbd_seconds']

    @property
    def get_sbd_seconds_last_update(self):
        return self.info['sbd_seconds_last_update']

    @property
    def get_sbd_last_interest_payment(self):
        return self.info['sbd_last_interest_payment']

    @property
    def get_savings_sbd_balance(self):
        return self.info['savings_sbd_balance']

    @property
    def get_savings_sbd_seconds(self):
        return self.info['savings_sbd_seconds']

    @property
    def get_savings_sbd_seconds_last_update(self):
        return self.info['savings_sbd_seconds_last_update']

    @property
    def get_savings_sbd_last_interest_payment(self):
        return self.info['savings_sbd_last_interest_payment']

    @property
    def get_savings_withdraw_requests(self):
        return self.info['savings_withdraw_requests']

    @property
    def get_reward_sbd_balance(self):
        return self.info['reward_sbd_balance']

    @property
    def get_reward_steem_balance(self):
        return self.info['reward_steem_balance']

    @property
    def get_reward_vesting_balance(self):
        return self.info['reward_vesting_balance']

    @property
    def get_reward_vesting_steem(self):
        return self.info['reward_vesting_steem']

    @property
    def get_vesting_shares(self):
        return self.info['vesting_shares']

    @property
    def get_delegated_vesting_shares(self):
        return self.info['delegated_vesting_shares']

    @property
    def get_received_vesting_shares(self):
        return self.info['received_vesting_shares']

    @property
    def get_vesting_withdraw_rate(self):
        return self.info['vesting_withdraw_rate']

    @property
    def get_next_vesting_withdrawal(self):
        return self.info['next_vesting_withdrawal']

    @property
    def get_withdrawn(self):
        return self.info['withdrawn']

    @property
    def get_to_withdraw(self):
        return self.info['to_withdraw']

    @property
    def get_withdraw_routes(self):
        return self.info['withdraw_routes']

    @property
    def get_curation_rewards(self):
        return self.info['curation_rewards']

    @property
    def get_posting_rewards(self):
        return self.info['posting_rewards']

    @property
    def get_proxied_vsf_votes(self):
        return self.info['proxied_vsf_votes']

    @property
    def get_witnesses_voted_for(self):
        return self.info['witnesses_voted_for']

    @property
    def get_last_post(self):
        return self.info['last_post']

    @property
    def get_last_root_post(self):
        return self.info['last_root_post']

    @property
    def get_last_vote_time(self):
        return self.info['last_vote_time']

    @property
    def get_post_bandwidth(self):
        return self.info['post_bandwidth']

    @property
    def get_pending_claimed_accounts(self):
        return self.info['pending_claimed_accounts']

    @property
    def get_is_smt(self):
        return self.info['is_smt']
