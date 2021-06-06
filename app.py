import json
import msgpack
import cbor2
import zstd
import snappy
import brotli
import codecs
import streamlit as st

st.set_page_config(layout="wide")


def minify_json(content, output_path=None):
    res = json.dumps(content, separators=(",", ":"))
    if output_path:
        open(output_path, "w").write(res)
    else:
        return res.encode("utf-8")


def encode_payload(content, alg, output_path=None):
    if alg == "msgpack":
        res = msgpack.dumps(content, use_bin_type=True)
    elif alg == "cbor":
        res = cbor2.dumps(content)

    if output_path:
        open(output_path, "wb").write(res)
    else:
        return res


def compress_payload(content, alg, output_path=None):
    if alg == "zstd":
        res = zstd.compress(content)
    elif alg == "brotli":
        res = brotli.compress(content)
    elif alg == "gz":
        res = codecs.encode(content, "zlib")
    elif alg == "snappy":

        res = snappy.compress(content)

    if output_path:
        open(output_path, "wb").write(res)
    else:
        return res


def encode_with_all(content):
    data = {}
    sizes = {}

    res = encode_payload(content, "msgpack")
    data["msgpack"] = res
    sizes["msgpack"] = len(res)

    res = encode_payload(content, "cbor")
    data["cbor"] = res
    sizes["cbor"] = len(res)

    return data, sizes


def compress_with_all(content):
    data = {}
    sizes = {}

    res = compress_payload(content, "zstd")
    data["zstd"] = res
    sizes["zstd"] = len(res)

    res = compress_payload(content, "brotli")
    data["brotli"] = res
    sizes["brotli"] = len(res)

    res = compress_payload(content, "snappy")
    data["snappy"] = res
    sizes["snappy"] = len(res)

    res = compress_payload(content, "gz")
    data["gz"] = res
    sizes["gz"] = len(res)

    return data, sizes


def main():
    st.title("json encoding and compression")

    json_str = st.sidebar.text_area(
        "json",
        "{}",
        350,
    )

    money = st.sidebar.number_input("bandwidth spending ($)", 0, value=1000)

    if st.sidebar.button("calculate savings"):
        try:
            ERROR_STR = "invalid or empty json!"
            json_obj = json.loads(json_str)
            if len(json_obj) == 0:
                st.error(ERROR_STR)
                return
        except:
            st.error(ERROR_STR)
            return

        json_bytes = json.dumps(json_str).encode("utf-8")
        json_minified = minify_json(json_obj)

        encoded_data = {}
        encoded_data["original"] = json_bytes
        encoded_data["minified"] = json_minified
        encoded_data2, _ = encode_with_all(json_obj)
        encoded_data.update(encoded_data2)

        md_str = "||zstd|brotli|snappy|gz|\n"
        md_str += "|-----|-----|-----|-----|-----|\n"
        maxi = ("no", None, 100)
        for j in encoded_data:
            _, compressed_sizes = compress_with_all(encoded_data[j])
            md_str += f"|**{j}**|"

            for i in compressed_sizes:
                size = compressed_sizes[i] * 100 / len(json_bytes)
                if maxi[2] > size:
                    maxi = (j, i, size)
                md_str += f"{compressed_sizes[i]} bytes - **{size:0.2f}%**|"

            md_str += "\n"

        saving_percent = (100 - maxi[2]) / 100
        st.success(
            f"you could save ** ${saving_percent * money:0.2f} ({saving_percent*100:0.2f}%)** with **{maxi[0]}** encoding and **{maxi[1]}** compression!"
        )

        st.write(
            f"""|json|size|
        |----|----|
        |**original**|{len(json_bytes)} bytes - **100.00%**|
        |**minified**|{len(json_minified)} bytes - **{len(json_minified) * 100 / len(json_bytes):0.2f}%**|
        """
        )
        st.write(f"\n\n")
        st.markdown(md_str)


if __name__ == "__main__":
    main()