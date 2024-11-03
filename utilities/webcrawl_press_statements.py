import streamlit as st
import utilities.webcrawler as webcrawler
from datetime import datetime
import json

st.title("Press Statements")


# Input URL
main_url = 'https://www.mfa.gov.sg/Newsroom/Press-Statements-Transcripts-and-Photos'
params= '?keyword=&country=&startdate=&enddate=&topic=&page='

# url = st.text_input("Enter a URL to scrape", "https:example.com")
# if url:

pages_crawled = []
for count in range(1, 6): #latest 5 pages
    press_statement_page = main_url+params+str(count);
    pages_crawled.extend(webcrawler.web_crawl(press_statement_page, 1))

scraped_content = ''

filtered_list = [item for item in pages_crawled if item.startswith(main_url) and item != main_url and params not in item]
filtered_list = list(set(filtered_list))
obj_list=[]
for page_url in filtered_list:
    obj = webcrawler.web_scrape(page_url)
    obj["url"] = page_url
    obj["category"] = "Press Statements"
    obj["rolePermissions"] =  ["official-open","non-sensitive"]
    obj_list.append(obj)



sorted_data = sorted(obj_list, key=lambda x: datetime.strptime(x['created_on'], '%d %B %Y'), reverse=True)#st.write(sorted_data)

json_data = json.dumps(sorted_data, indent=4, ensure_ascii=True)
clean_data = json_data.replace("\t", " ")

if json_data:
    st.download_button(
        label="Download JSON",
        data=clean_data,
        file_name="data.json",
        mime="application/json"
    )