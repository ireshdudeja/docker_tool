from flask import Flask
from flask_restful import Resource, Api
import docker

app = Flask(__name__)
api = Api(app)

class Home(Resource):
    def get(self):
        return {"api": {"path": "/containers"}}, 200


class Containers(Resource):
    def get(self):
        return {'data': list_containers()}, 200


api.add_resource(Home, "/")
api.add_resource(Containers, "/containers")


def list_containers():
    running_containers_list = []
    try:
        client = docker.from_env()
        for container in client.containers.list(filters={"status": "running"}):
            container_info = {
                "container_id": container.attrs["Id"],
                "container_name": container.attrs["Name"],
                "image": container.attrs["Image"],
                "status": container.attrs["State"]["Status"]
            }
            running_containers_list.append(container_info)
    except:
        print("server.py | Exception thrown. Check if docker is running.")
    return running_containers_list


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
