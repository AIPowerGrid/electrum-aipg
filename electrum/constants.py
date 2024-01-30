# -*- coding: utf-8 -*-
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2018 The Electrum developers
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json

from typing import NamedTuple, Union

# Can't import from util due to circular
def inv_dict(d):
    return {v: k for k, v in d.items()}

def read_json(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            r = json.loads(f.read())
    except:
        r = default
    return r


GIT_REPO_URL = "https://github.com/AIPowerGrid/electrum-aipg"
GIT_REPO_ISSUES_URL = "https://github.com/AIPowerGrid/electrum-aipg/issues"
BIP39_WALLET_FORMATS = read_json('bip39_wallet_formats.json', [])


class BurnAmounts(NamedTuple):
    IssueAssetBurnAmount: Union[int, float]
    ReissueAssetBurnAmount: Union[int, float]
    IssueSubAssetBurnAmount: Union[int, float]
    IssueUniqueAssetBurnAmount: Union[int, float]
    IssueMsgChannelAssetBurnAmount: Union[int, float]
    IssueQualifierAssetBurnAmount: Union[int, float]
    IssueSubQualifierAssetBurnAmount: Union[int, float]
    IssueRestrictedAssetBurnAmount: Union[int, float]
    AddNullQualifierTagBurnAmount: Union[int, float]


class BurnAddresses(NamedTuple):
    IssueAssetBurnAddress: str
    ReissueAssetBurnAddress: str
    IssueSubAssetBurnAddress: str
    IssueUniqueAssetBurnAddress: str
    IssueMsgChannelAssetBurnAddress: str
    IssueQualifierAssetBurnAddress: str
    IssueSubQualifierAssetBurnAddress: str
    IssueRestrictedAssetBurnAddress: str
    AddNullQualifierTagBurnAddress: str
    GlobalBurnAddress: str

class AbstractNet:
    GENESIS = None
    CHECKPOINTS = None
    DGW_CHECKPOINTS = None
    DGW_CHECKPOINTS_SPACING = 0
    DGW_CHECKPOINTS_START = 0
    MATURE = 0

    NET_NAME: str
    TESTNET: bool
    WIF_PREFIX: int
    ADDRTYPE_P2PKH: int
    ADDRTYPE_P2SH: int
    SEGWIT_HRP: str
    BOLT11_HRP: str
    GENESIS: str
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS: int = 0
    BIP44_COIN_TYPE: int
    LN_REALM_BYTE: int

    @classmethod
    def max_legacy_checkpoint(cls) -> int:
        return max(0, len(cls.CHECKPOINTS) * 2016 - 1)

    @classmethod
    def max_checkpoint(cls) -> int:
        # DGW Checkpoints start at height 400,000 and are every 2016 blocks after
        return max(0, cls.DGW_CHECKPOINTS_START + (len(cls.DGW_CHECKPOINTS) * cls.DGW_CHECKPOINTS_SPACING) - 1)

    @classmethod
    def rev_genesis_bytes(cls) -> bytes:
        from . import bitcoin
        return bytes.fromhex(bitcoin.rev_hex(cls.GENESIS))


class AIPGMainnet(AbstractNet):
    NET_NAME = "mainnet"
    TESTNET = False
    WIF_PREFIX = 128
    ADDRTYPE_P2PKH = 23
    ADDRTYPE_P2SH = 23
    ADDRTYPE_P2SH_ALT = 23
    MATURE = 60
    SEGWIT_HRP = "rc"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "000000fe8c99a7aacc5aff074278a8378e625c0d02e4894db8f09bab185f4eb6"
    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers.json', {})
    CHECKPOINTS = read_json('checkpoints.json', [])
    DGW_CHECKPOINTS = read_json('checkpoints_dgw.json', [])
    DGW_CHECKPOINTS_SPACING = 2016
    DGW_CHECKPOINTS_START = 168 * DGW_CHECKPOINTS_SPACING  #338_688, DGW starts at 338_778

    X16Rv2ActivationTS = 1688764800
    KawpowActivationTS = 1688764800
    KawpowActivationHeight = 1
    nDGWActivationBlock = 1

    DEFAULT_MESSAGE_CHANNELS = ['ELECTRUM_AIPG~notification']
    ASSET_PREFIX = b'aipg'
    SHORT_NAME = 'AIPG'
    LONG_NAME = 'AIPG'

    MULTISIG_ASSETS = False

    XPRV_HEADERS = {
        'standard': 0x0488ade4,  # xprv
        'p2wpkh-p2sh': 0x049d7878,  # yprv
        'p2wsh-p2sh': 0x0295b005,  # Yprv
        'p2wpkh': 0x04b2430c,  # zprv
        'p2wsh': 0x02aa7a99,  # Zprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard': 0x0488b21e,  # xpub
        'p2wpkh-p2sh': 0x049d7cb2,  # ypub
        'p2wsh-p2sh': 0x0295b43f,  # Ypub
        'p2wpkh': 0x04b24746,  # zpub
        'p2wsh': 0x02aa7ed3,  # Zpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 2686

    BURN_AMOUNTS = BurnAmounts(
        IssueAssetBurnAmount=50,
        ReissueAssetBurnAmount=10,
        IssueSubAssetBurnAmount=10,
        IssueUniqueAssetBurnAmount=0.5,
        IssueMsgChannelAssetBurnAmount=10,
        IssueQualifierAssetBurnAmount=100,
        IssueSubQualifierAssetBurnAmount=10,
        IssueRestrictedAssetBurnAmount=150,
        AddNullQualifierTagBurnAmount=0.01
    )

    BURN_ADDRESSES = BurnAddresses(
        IssueAssetBurnAddress='AIissueAssetXXXXXXXXXXXXXXXXXhhZGt',
        ReissueAssetBurnAddress='AIReissueAssetXXXXXXXXXXXXXXVEFAWu',
        IssueSubAssetBurnAddress='AIissueSubAssetXXXXXXXXXXXXXWcwhwL',
        IssueUniqueAssetBurnAddress='AIissueUniqueAssetXXXXXXXXXXWEAe58',
        IssueMsgChannelAssetBurnAddress='AIissueMsgChanneLAssetXXXXXXSjHvAY',
        IssueQualifierAssetBurnAddress='AIissueQuaLifierXXXXXXXXXXXXUgEDbC',
        IssueSubQualifierAssetBurnAddress='AIissueSubQuaLifierXXXXXXXXXVTzvv5',
        IssueRestrictedAssetBurnAddress='AIissueRestrictedXXXXXXXXXXXXzJZ1q',
        AddNullQualifierTagBurnAddress='AIaddTagBurnXXXXXXXXXXXXXXXXZQm5ya',
        GlobalBurnAddress='AIBurnXXXXXXXXXXXXXXXXXXXXXXWUo9FV'
    )


class AIPGTestnet(AbstractNet):
    NET_NAME = "testnet"
    BIP44_COIN_TYPE = 1
    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = [
    ]
    TESTNET = True
    WIF_PREFIX = 239
    ADDRTYPE_P2PKH = 23
    ADDRTYPE_P2SH = 23
    ADDRTYPE_P2SH_ALT = 23
    MATURE = 60
    SEGWIT_HRP = "tc"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "000000f798386703ae778eeaf8a2f426dc2715eb8989b4226cddc1681b567760"
    DEFAULT_PORTS = {'t': '51001', 's': '51002'}
    DEFAULT_SERVERS = read_json('servers_testnet.json', {})
    CHECKPOINTS = []
    DGW_CHECKPOINTS = read_json('checkpoints_dgw_testnet.json', [])
    DGW_CHECKPOINTS_SPACING = 2016
    DGW_CHECKPOINTS_START = 0

    X16Rv2ActivationTS = 1688764800
    KawpowActivationTS = 1688764800
    KawpowActivationHeight = 1
    nDGWActivationBlock = 1

    DEFAULT_MESSAGE_CHANNELS = []
    ASSET_PREFIX = b'aipg'
    SHORT_NAME = 'tAIPG'
    LONG_NAME = 'AIPG'
    MULTISIG_ASSETS = False
    
    XPRV_HEADERS = {
        'standard': 0x04358394,  # tprv
        'p2wpkh-p2sh': 0x044a4e28,  # uprv
        'p2wsh-p2sh': 0x024285b5,  # Uprv
        'p2wpkh': 0x045f18bc,  # vprv
        'p2wsh': 0x02575048,  # Vprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard': 0x043587cf,  # tpub
        'p2wpkh-p2sh': 0x044a5262,  # upub
        'p2wsh-p2sh': 0x024289ef,  # Upub
        'p2wpkh': 0x045f1cf6,  # vpub
        'p2wsh': 0x02575483,  # Vpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)

    BURN_AMOUNTS = BurnAmounts(
        IssueAssetBurnAmount=50,
        ReissueAssetBurnAmount=10,
        IssueSubAssetBurnAmount=10,
        IssueUniqueAssetBurnAmount=0.5,
        IssueMsgChannelAssetBurnAmount=10,
        IssueQualifierAssetBurnAmount=100,
        IssueSubQualifierAssetBurnAmount=10,
        IssueRestrictedAssetBurnAmount=150,
        AddNullQualifierTagBurnAmount=0.01
    )

    BURN_ADDRESSES = BurnAddresses(
        IssueAssetBurnAddress='n1issueAssetXXXXXXXXXXXXXXXXWdnemQ',
        ReissueAssetBurnAddress='n1ReissueAssetXXXXXXXXXXXXXXWG9NLd',
        IssueSubAssetBurnAddress='n1issueSubAssetXXXXXXXXXXXXXbNiH6v',
        IssueUniqueAssetBurnAddress='n1issueUniqueAssetXXXXXXXXXXS4695i',
        IssueMsgChannelAssetBurnAddress='n1issueMsgChanneLAssetXXXXXXT2PBdD',
        IssueQualifierAssetBurnAddress='n1issueQuaLifierXXXXXXXXXXXXUysLTj',
        IssueSubQualifierAssetBurnAddress='n1issueSubQuaLifierXXXXXXXXXYffPLh',
        IssueRestrictedAssetBurnAddress='n1issueRestrictedXXXXXXXXXXXXZVT9V',
        AddNullQualifierTagBurnAddress='n1addTagBurnXXXXXXXXXXXXXXXXX5oLMH',
        GlobalBurnAddress='AcYHNBj8C6nCFSpu1ANsJxturWp31W32cd'
    )


def all_subclasses(cls):
    """Return all (transitive) subclasses of cls."""
    res = set(cls.__subclasses__())
    for sub in res.copy():
        res |= all_subclasses(sub)
    return res

NETS_LIST = tuple(all_subclasses(AbstractNet))

# don't import net directly, import the module instead (so that net is singleton)
net = RavencoinMainnet


def set_mainnet():
    global net
    net = RavencoinMainnet

def set_testnet():
    global net
    net = RavencoinTestnet
