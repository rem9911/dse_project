import streamlit as st
from elasticsearch import Elasticsearch
from FlagMapping import team_flags
import time
import concurrent.futures
import json
indexName = "dse_project_world_cup"
#"https://192.168.1.130:9200/"
try:
    es = Elasticsearch(
        "https://localhost:9200",
        
        basic_auth=("elastic","CIyX=*SG=U79tDbkd4Fw"),
        verify_certs=False
#        ca_certs="/Users/remygodin/Desktop/Semester2/DSE/project/elasticsearch-8.13.4/config/certs/http_ca.crt"
    )
except Exception as e:
    print("Error: ", e)
if es.ping():
    
    print("Connected to ES!")
else: 
    print(es.info())
    print("Could not connect to ES")

def main():
    st.set_page_config(
    page_title="DSE Project - World Cup Search Engine",
    page_icon="⚽️",
    layout="centered",
    initial_sidebar_state="expanded",
    )
    st.image(team_flags["image"],width=750)
    st.title("World Cup Search Engine")
    search_field = st.selectbox("Search by", [ "Team","Home Team", "Away Team","City","Stadium","Date","Time (Brazil)","Stage","Win","Win Conditions","Penalty"])
    search_query = st.text_input(f"Enter a {search_field} name to search for matches")
    if search_field == "Team":
        query = {
                "query": {
                    "bool": {
                        "should": [
                            {"match": {"Home Team": search_query}},
                            {"match": {"Away Team": search_query}},
                            {"match": {"Win": search_query}}
                        ]
                    }
                }
            }
    else:
        query = {
            "query": {
                "match": {search_field: search_query}
            }
        }
    if st.button("Search"):
        if search_query:

            start_time = time.time()
            results = es.search(index=indexName, body=query)["hits"]["hits"]
            end_time = time.time()
            response_time = (end_time - start_time) * 1000

            st.subheader(f"Found {len(results)} results in {response_time:.2f} ms")
            for result in results:
                with st.container(border=True):
                    print(result)
                    if '_source' in result:
                        
                        try:
                            col1, mid, col2 = st.columns([0.22,0.56,0.22])
                            HomeTeamFlag = team_flags[result['_source']['Home Team']]
                            AwayTeamFlag = team_flags[result['_source']['Away Team']]
                            with col1:
                                st.image(HomeTeamFlag,width=50)
                            with mid:
                                st.header(f"{result['_source']['Home Team']} vs {result['_source']['Away Team']}")
                            with col2:
                                st.image(AwayTeamFlag,width=50)
                        except Exception as e:
                            st.write(e)
                        try:
                            st.write(f"Score: {result['_source']['Home Team Goals']} - {result['_source']['Away Team Goals']}")
                        except Exception as e:
                            st.write(e)
                        try:
                            st.write(f"Stadium: {result['_source']['Stadium']} in {result['_source']['City']} on {result['_source']['Date']} at {result['_source']['Time (Brazil)']}")
                        except Exception as e:
                            st.write(e)
                        try:
                            st.write(f"Attendance: {result['_source']['Attendance']} fans")
                        except Exception as e:
                            st.write(e)
                        winner = result['_source']['Win']
                        if winner in team_flags:
                            col1, mid, col2 = st.columns([0.38,0.40,0.22])
                            with mid:
                                st.image(team_flags[winner], width=100)
                                st.write(f"{winner} won !")
                        
                        st.divider()

if __name__ == "__main__":
    main()

