    content = requests.get(f"https://raw.githubusercontent.com/d10000usd/Tradingview/main_1/README.md").text
    FILTER_SHARE = re.compile(r"^.*\[share_\w+\].*$", re.MULTILINE)
    st.markdown(FILTER_SHARE.sub("", content))
