# DSE Project

My main app is the app.py, 
- To install requirements: ``` pip install -r requirements.txt ```
- To start the Docker Elasticsearch cluster: ``` docker-compose up -d ```
- To run the app: ``` streamlit run app.py ```
- To have a graphic user interface and to ingest data, use kibana on ``` http://localhost:5601/ ```

then i did a second one to try to do semantic search, the corresponding files are ```indexData.ipynb ``` to index the data, ``` IndexMapping.py ``` the data to index and ```semantic_search.py ``` for the app.
