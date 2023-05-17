    ## Easy to use
    ```  
    content = requests.get(
      f"https://raw.githubusercontent.com/d10000usd/json/main/{filename}/{filename}_news_원본.md"
    ).text
    FILTER_SHARE = re.compile(r"^.*\[share_\w+\].*$", re.MULTILINE)
    st.markdown(FILTER_SHARE.sub("", content))
    ```  
