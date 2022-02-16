import requests
import schedule
import time
import docker

url = "http://host.docker.internal:8080/containers"
# localhost --> host.docker.internal

response = requests.get(url)
docker_client = docker.from_env()
status_state_list = []


def currently_running_containers():
    running_containers_list = []
    try:
        for container in docker_client.containers.list(filters={"status": "running"}):
            running_containers_list.append(container.attrs["Id"])
    except:
        print("controller.py | Exception thrown.")
    return running_containers_list


def compare_containers():
    to_start = set(status_state_list).difference(
        set(currently_running_containers()))
    to_stop = set(currently_running_containers()
                  ).difference(set(status_state_list))
    if(len(to_start) != 0):
        start_containers(to_start)
    if(len(to_stop) != 0):
        stop_containers(to_stop)
    # print(f"controller.py | Containers to Start: {len(to_start)}")
    # print(f"controller.py | Containers to Stop: {len(to_stop)}")


def start_containers(tSet):
    try:
        for item in tSet:
            container = docker_client.containers.get(item)
            print(f"Starting container with id: {container.attrs['Id']}")
            container.start()
    except:
        print("controller.py | Error starting container(s).")


def stop_containers(tSet):
    try:
        for item in tSet:
            container = docker_client.containers.get(item)
            # container.stop()
            print(f"Removing container with id: {container.attrs['Id']}")
            container.remove(force=True)
    except:
        print("controller.py | Error stopping container(s).")


try:
    if(response.ok):
        result = response.json()
        data = result["data"]
        status_state_list = [item["container_id"] for item in data]
        print(f"controller.py | status_state_list:\n {status_state_list}\n")
        print(f"controller.py | Containers to maintain: {len(status_state_list)}")
        # print(currently_running_containers())
        compare_containers()
    else:
        response.raise_for_status()
except:
    print("controller.py | Exception thrown. Check server response")


schedule.every(30).seconds.do(compare_containers)

while True:
    schedule.run_pending()
    time.sleep(1)
