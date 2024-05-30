import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from FlagMapping import team_flags
import time
indexName = "dse_project_v2"

try:
    es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "CIyX=*SG=U79tDbkd4Fw"),
    verify_certs=False
    )
except ConnectionError as e:
    print("Connection Error:", e)
    
if es.ping():
    print("Succesfully connected to ElasticSearch!!")
else:
    print("Oops!! Can not connect to Elasticsearch!")




def search(input_keyword):
    model = SentenceTransformer('all-mpnet-base-v2')
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field": "DescriptionVector",
        "query_vector": vector_of_input_keyword,
        "k": 10,
        "num_candidates": 500
    }
    res = es.knn_search(index="dse_project_v2"
                        , knn=query 
                        , source=["Home Team","Win","Away Team","Home Team Goals","Away Team Goals","Total Goals","Attendance","City","Stadium","Date","Time (Brazil)"]
                        )
    results = res["hits"]["hits"]

    return results

def main():
    st.set_page_config(
    page_title="DSE Project - World Cup Search Engine",
    page_icon="⚽️",
    layout="centered",
    initial_sidebar_state="expanded",
    )
    st.image(team_flags["image"],width=750)
    st.title("World Cup Search Engine")
    search_query = st.text_input("Enter your search query")

    
    if st.button("Search"):
        if search_query:

            start_time = time.time()
            results = search(search_query)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000

            relevance_threshold = 0.65  # Adjust the threshold based on your requirements
            filtered_results = [result for result in results if result['_score'] >= relevance_threshold]

            st.subheader(f"Found {len(filtered_results)} results in {response_time:.2f} ms")
            for result in filtered_results:
                print(result['_score'])
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










