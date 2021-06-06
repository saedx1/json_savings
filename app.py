import json

import streamlit as st

import logic

JSON_ERROR_STR = "invalid json"

DEFAULT_JSON = """{
  "Name": "Saed",
  "Courses": ["Data Structures", "Algorithm Design and Analysis"],
  "PreviousCourses": [
    { "Name": "Intro to Programming", "Grade": 90 },
    { "Name": "Discrete Math", "Grade": 85 }
  ]
}"""


def init_config():
    st.set_page_config(
        page_title="JSON Savings",
        layout="wide",
        initial_sidebar_state="auto",
    )
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def create_checkbox_group(label, members, sidebar=False):
    input_label(label, sidebar)
    return {i: checkbox(i, sidebar) for i in members}


def checkbox(text, sidebar=True):
    if sidebar:
        return st.sidebar.checkbox(text)

    return st.checkbox(text)


def input_label(text, sidebar=True):
    if sidebar:
        return st.sidebar.subheader(text)

    return st.subheader(text)


def html_center(str):
    return "<center>\n\n" + str + "\n\n</center>"


def main():

    init_config()

    st.sidebar.title("Inputs")
    st.title("JSON Savings!")

    input_label("JSON Payload")
    json_str = st.sidebar.text_area("", DEFAULT_JSON)

    col1, col2 = st.sidebar.beta_columns(2)
    with col1:
        comp_inputs = create_checkbox_group("Compression", logic.get_compressions())
    with col2:
        enc_inputs = create_checkbox_group("Serialization", logic.get_serializations())

    selected_encs = [k for k, v in enc_inputs.items() if v]
    selected_comps = [k for k, v in comp_inputs.items() if v]

    input_label("GB Price ($)")
    price = st.sidebar.number_input("", 0.0, value=0.09, key="gbp")

    input_label("Number of Users")
    n_users = st.sidebar.number_input("", 1, value=100, key="nu")

    input_label("User Requests per Minute")
    req_user = st.sidebar.number_input("", 1, value=100, key="nrm")

    # if st.sidebar.button("Calculate"):
    if st.sidebar.button("Calculate"):
        if len(selected_comps) == 0:
            st.error("Please select at least one compression techinque!")
            return

        try:
            json_obj = json.loads(json_str)
            if len(json_obj) == 0:
                return
        except:
            st.error(JSON_ERROR_STR)
            return

        json_bytes = json_str.encode("utf-8")

        encoded_data = {}
        encoded_data["original"] = json_bytes
        encoded_data2, _ = logic.encode(json_obj, selected_encs)
        encoded_data.update(encoded_data2)

        md_str = f"||{'|'.join(selected_comps)}|\n"
        md_str += f"|{'|'.join('-----'* (len(selected_comps)+1))}|\n"

        maxi = ("no", None, 100)
        for j in encoded_data:
            _, compressed_sizes = logic.compress(encoded_data[j], selected_comps)
            md_str += f"|**{j}**|"

            for i in compressed_sizes:
                size = compressed_sizes[i] * 100 / len(json_bytes)
                if maxi[2] > size:
                    maxi = (j, i, size)
                md_str += f"{compressed_sizes[i]} bytes - **{size:0.2f}%**|"

            md_str += "\n"

        saving_percent = (100 - maxi[2]) / 100

        st.markdown(
            html_center(f"## Original JSON Size: **{len(json_bytes)} bytes**"),
            unsafe_allow_html=True,
        )
        st.write(f"\n\n")

        md_str = html_center(md_str)
        st.markdown(md_str, unsafe_allow_html=True)
        st.write(f"\n\n")

        total_price = (
            n_users
            * req_user
            * 30  # days
            * 24  # hours
            * 60  # minutes
            / 1024  # kilobytes
            / 1024  # megabytes
            / 1024  # gigabytes
            * price
            * len(json_bytes)
        )

        st.info(f"Currently, your total monthly bill is ${total_price:0.3f}")

        if saving_percent != 0:
            st.success(
                f"You could save ** ${saving_percent * total_price:0.3f} ({saving_percent*100:0.2f}%)** with **{maxi[0]}** encoding and **{maxi[1]}** compression! Your bill could become **${total_price*(1-saving_percent):0.3f}**."
            )
        else:
            st.error(
                "Unfortunately, using any of those techniques will result in a bigger JSON!"
            )


if __name__ == "__main__":
    main()
