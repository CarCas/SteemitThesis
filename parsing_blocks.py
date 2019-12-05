import json
import multiprocessing as mp
from threading import Lock

import block_structure

lock = Lock()
op_lock = Lock()

errors = 0


def find_in_oparray(ar=None, author="", weight=-1):
    for i in ar:
        if type(i) is block_structure.Comment:
            cmt: block_structure.Comment = i
            if cmt.author == author:
                cmt.add_vote()
                cmt.add_weight(weight)


def fill_ops(trans_operations=None):
    op_array = []
    for op in trans_operations:
        if op[0] == 'vote':
            vt = block_structure.Vote(op[1]['voter'], op[1]['author'], op[1]['permlink'], op[1]['weight'])
            find_in_oparray(op_array, op[1]['author'], int(op[1]['weight']))
            op_array.append(vt)

        elif op[0] == 'comment':
            cmt = block_structure.Comment(op[1]['parent_author'],
                                          op[1]['parent_permlink'],
                                          op[1]['author'],
                                          op[1]['permlink'],
                                          op[1]['title'],
                                          op[1]['body'],
                                          op[1]['json_metadata'])
            op_array.append(cmt)

        elif op[0] == 'custom_json':
            custom = json.loads(json.dumps(op[1]))
            if custom['id'] == "follow":
                js = custom['json']
                req_posting_auths = custom['required_posting_auths']
                injs = json.loads(js)

                if injs[0] == 'follow':
                    if 'following' in injs[1]:
                        follow = block_structure.CustomJsonFollow(injs[1]['follower'].strip(),
                                                                  injs[1]['following'].strip(), injs[1]['what'],
                                                                  req_posting_auths)
                        op_array.append(follow)

                    else:
                        follow = block_structure.CustomJsonFollow(injs[1]['follower'].strip(), "", injs[1]['what'],
                                                                  req_posting_auths)
                        op_array.append(follow)

                        global errors
                        errors += 1

                elif injs[0] == 'reblog':
                    reblog = block_structure.CustomJsonReblog(injs[1]['account'], injs[1]['author'],
                                                              injs[1]['permlink'], req_posting_auths)
                    op_array.append(reblog)

            elif custom['id'] == "sm_sell_cards":
                js = custom['json']
                injs = json.loads(js)
                sell = block_structure.CustomJsonSellCards()

                for inn in injs:
                    cards = [c for c in inn['cards']]
                    card = block_structure.Card(cards, inn['price'], inn['fee_pct'])
                    sell.append(card)
                op_array.append(sell)

        elif op[0] == 'transfer':
            transfer = block_structure.Transfer(op[1]['from'], op[1]['to'], op[1]['amount'], op[1]['memo'])
            op_array.append(transfer)

        elif op[0] == 'transfer_to_vesting':
            transfer_to_vesting = block_structure.TransferToVesting(op[1]['from'], op[1]['to'], op[1]['amount'])
            op_array.append(transfer_to_vesting)

        elif op[0] == 'withdraw_vesting':
            withdraw_vesting = block_structure.WithdrawVesting(op[1]['account'], op[1]['vesting_shares'])
            op_array.append(withdraw_vesting)

        elif op[0] == 'limit_order_create':
            limit_order_create = block_structure.LimitOrderCreate(op[1]['owner'], op[1]['orderid'],
                                                                  op[1]['amount_to_sell'],
                                                                  op[1]['min_to_receive'],
                                                                  op[1]['fill_or_kill'], op[1]['expiration'])
            op_array.append(limit_order_create)

        elif op[0] == 'limit_order_cancel':
            limit_order_cancel = block_structure.LimitOrderCreate(op[1]['owner'], op[1]['orderid'])
            op_array.append(limit_order_cancel)

        elif op[0] == 'feed_publish':
            exc_rate = op[1]['exchange_rate']
            exc_rate = block_structure.Price(exc_rate['base'], exc_rate['quote'])
            fd_pub = block_structure.FeedPublish(op[1]['publisher'], exc_rate)
            op_array.append(fd_pub)

        elif op[0] == 'convert':
            convert = block_structure.Convert(op[1]['owner'], op[1]['requestid'], op[1]['amount'])
            op_array.append(convert)

        elif (op[0] == 'account_create') or (op[0] == 'create_claimed_account'):
            act = block_structure.Account()
            own = block_structure.Account()
            pst = block_structure.Account()
            if "active" in op[1]:
                opact = op[1]['active']
                act = block_structure.Account(opact['weight_threshold'], opact['account_auths'], opact['key_auths'])
            if "owner" in op[1]:
                opown = op[1]['owner']
                own = block_structure.Account(opown['weight_threshold'], opown['account_auths'], opown['key_auths'])
            if "posting" in op[1]:
                opst = op[1]['posting']
                pst = block_structure.Account(opst['weight_threshold'], opst['account_auths'], opst['key_auths'])
            if op[0] == 'account_create':
                new_acc = block_structure.AccountCreate(op[1]['fee'], op[1]['creator'], op[1]['new_account_name'],
                                                        own, act, pst, op[1]['memo_key'], op[1]['json_metadata'])
            else:
                new_acc = block_structure.CreateClaimedAccount(op[1]['creator'], op[1]['new_account_name'], own, act,
                                                               pst, op[1]['memo_key'], op[1]['json_metadata'])
            op_array.append(new_acc)

        elif op[0] == 'account_update':
            acc = block_structure.Account()
            own = block_structure.Account()
            act = block_structure.Account()
            pst = block_structure.Account()
            # memo_key = ""
            # json_mtdt = ""
            if "account" in op[1]:
                acc = op[1]['account']
            if "owner" in op[1]:
                opown = op[1]['owner']
                own = block_structure.Account(opown['weight_threshold'], opown['account_auths'], opown['key_auths'])
            if "active" in op[1]:
                opact = op[1]['active']
                act = block_structure.Account(opact['weight_threshold'], opact['account_auths'], opact['key_auths'])
            if "posting" in op[1]:
                opst = op[1]['posting']
                pst = block_structure.Account(opst['weight_threshold'], opst['account_auths'], opst['key_auths'])
            acc_upd = block_structure.AccountUpdate(acc, own, act, pst, op[1]['memo_key'], op[1]['json_metadata'])
            op_array.append(acc_upd)

    return op_array


def evaluate_block(line=""):
    data = [json.loads(line)]

    bs = block_structure.BlockStructure()
    for parsed_json in data:
        bs.set_timestamp(parsed_json['timestamp'])
        transss = []
        for transactions in parsed_json['transactions']:
            operations = fill_ops(transactions['operations'])
            t_block = block_structure.TransactionBlockStructure()
            t_block.set_transaction_num(transactions['transaction_num'])
            if len(operations) > 0:
                t_block.set_operations(operations)
            op_lock.acquire()
            t = block_structure.Transaction(transactions['transaction_id'], t_block)
            op_lock.release()
            transss.append(t)
        bs.set_transactions(transss)
        bs.set_witness_name(parsed_json['witness'])
    return bs


def parsing_blocks(path="steem_first2"):  # "steem.blockchain_14"
    blocks = []
    with open(path, 'r', encoding="UTF-8") as file:
        # for line in file:
        #     b = evaluate_block(line)
        #    blocks.append(copy.deepcopy(b))
        pool = mp.Pool(processes=mp.cpu_count())

        res = pool.map(evaluate_block, [line for line in file])

        pool.close()
        pool.join()

        for r in res:
            lock.acquire()
            blocks.append(r)
            lock.release()
        # for b in blocks:
        #    b.print_block()
    # print("STRANGE BEHAVIOURS in follow op: " + str(errors))
    return blocks
