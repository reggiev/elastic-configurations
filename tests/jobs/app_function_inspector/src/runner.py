import requests

def check_elasticsearch():
    res = requests.get('http://elasticsearch-service:9200/')
    print("Checking elasticsearch")
    print("ES Name: " + res.json()["name"])
    print("Tag line: " + res.json()["tagline"] )
    print("Status code: " + str(res.status_code ))
    return 0 if res.json()["name"] and res.json()["tagline"] == "You Know, for Search" \
        and res.status_code == 200 else 1


def check_kibana():
    res = requests.get('http://kibana-service:5601/')
    # Check the headers of the response
    print("Checking Kibana")
    print("License: " + res.headers["kbn-license-sig"])
    print("Kibana name: " + res.headers["kbn-name"])
    print("Status code: " + str(res.status_code))
    return 0 if res.headers["kbn-license-sig"] and res.headers["kbn-name"] \
        and res.status_code == 200 else 1


def check_logstash():
    res = requests.get('http://logstash-service:9600/')
    print("Checking logstash")
    print("Response code: " + str(res.status_code))
    print("Status: " + str(res.json()["status"]))
    print("Host: " + res.json()["host"] )
    print("Status code: " + str(res.status_code))
    # Check if the response is acceptable
    return 0 if res.json()["status"] == "green" and res.json()["host"] \
        and res.status_code == 200 else 1


if __name__ == "__main__":
    if check_kibana() or \
    check_elasticsearch() or \
    check_logstash():
        # Fail the job
        print("Failing the job")
        exit(1)
    else:
        print("The job is success")
        exit(0)