from elasticsearch import Elasticsearch
import time
import os
import concurrent.futures
import matplotlib.pyplot as plt
import urllib3
import warnings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', category=UserWarning, module='elasticsearch')
warnings.filterwarnings('ignore', 'Connecting to .+ using TLS with verify_certs=False is insecure', category=Warning)
# Load environment variables
ES_HOSTS = [
    "https://localhost:9200",
    "https://localhost:9201",
    "https://localhost:9202"
]
ES_USER = os.getenv("ES_USER", "elastic")
ES_PASSWORD = os.getenv("ELASTIC_PASSWORD")
CA_CERT_PATH = os.getenv("CA_CERT_PATH", "/Users/remygodin/Desktop/Semester2/DSE/project/elasticsearch-8.13.4/config/certs/http_ca.crt")
print(ES_PASSWORD)
# Initialize the Elasticsearch client
try:
    es = Elasticsearch(
        ES_HOSTS,
        basic_auth=("elastic", "CIyX=*SG=U79tDbkd4Fw"),
        verify_certs=False
        #ca_certs=CA_CERT_PATH
    )
except Exception as e:
    print(f"Error: {e}")

if es.ping():
    print("Connected to Elasticsearch!")
else:
    print("Could not connect to Elasticsearch")

def average_response_time(query, index_name, num_requests=10):
    response_times = []
    
    for _ in range(num_requests):
        print(_)
        start_time = time.time()
        es.search(index=index_name, body=query)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        response_times.append(response_time)
        time.sleep(1)  # Add a small delay between requests to avoid overloading

    average_response_time = sum(response_times) / num_requests
    print(f"Average response time for {num_requests} requests: {average_response_time:.2f} ms")

def measure_response_time(query, index_name):
    start_time = time.time()
    es.search(index=index_name, body=query)
    end_time = time.time()
    response_time = (end_time - start_time) * 1000  # Convert to milliseconds
    return response_time

def measure_concurrent_requests(query, index_name, num_requests=10):
    response_times = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(measure_response_time, query, index_name) for _ in range(num_requests)]
        
        for future in concurrent.futures.as_completed(futures):
            try:
                response_time = future.result()
                response_times.append(response_time)
            except Exception as e:
                print(f"Request generated an exception: {e}")

    average_response_time = sum(response_times) / len(response_times) if response_times else 0
    print(f"Average response time for {num_requests} concurrent requests: {average_response_time:.2f} ms")
    return average_response_time


def plot_response_times(index_name, query, max_requests):
    requests = list(range(1, max_requests + 1,1000))
    response_times = []

    for num_requests in requests:
        avg_response_time = measure_concurrent_requests(query, index_name, num_requests)
        response_times.append(avg_response_time)
        print(f"Simultaneous Requests: {num_requests}, Average Response Time: {avg_response_time:.2f} ms")

    plt.figure(figsize=(10, 6))
    plt.plot(requests, response_times, marker='o')
    plt.title('Response Time vs Number of Simultaneous Requests')
    plt.xlabel('Number of Simultaneous Requests')
    plt.ylabel('Average Response Time (ms)')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    index_name = "dse_project_world_cup"
    query = {
        "query": {
            "match_all": {}
        }
    }
    max_requests = 10000
    #average_response_time(query, index_name, num_requests=100)
    #measure_concurrent_requests(query, index_name, num_requests=1000)
    plot_response_times(index_name, query, max_requests)