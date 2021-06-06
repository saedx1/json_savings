import codecs
import json
from functools import partial

import msgpack
import cbor2
import zstd
import snappy
import brotli


def minify(content):
    res = json.dumps(content, separators=(",", ":"))
    return res.encode("utf-8")


SERIAL_FUNCS = {
    "minifed": minify,
    "msgpack": partial(msgpack.dumps, use_bin_type=True),
    "cbor": cbor2.dumps,
}

COMPRESSION_FUNCS = {
    "zstd": zstd.compress,
    "brotli": brotli.compress,
    "gz": partial(codecs.encode, encoding="zlib"),
    "snappy": snappy.compress,
}


def get_serializations():
    return list(SERIAL_FUNCS.keys())


def get_compressions():
    return list(COMPRESSION_FUNCS.keys())


def encode(content, algs):

    data = {}
    sizes = {}
    for i in algs:
        data[i] = SERIAL_FUNCS[i](content)
        sizes[i] = len(data[i])

    return data, sizes


def compress(content, algs):

    data = {}
    sizes = {}

    for i in algs:
        data[i] = COMPRESSION_FUNCS[i](content)
        sizes[i] = len(data[i])

    return data, sizes
