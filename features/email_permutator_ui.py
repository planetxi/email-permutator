import streamlit as st

def show_email_permutator():
    st.header("🧪 Email Permutator")
    st.write("Enter name and domain to generate combinations.")
    name = st.text_input("Full Name")
    domain = st.text_input("Domain (e.g. example.com)")
    if st.button("Generate"):
        st.success("Generated email permutations will appear here.")
