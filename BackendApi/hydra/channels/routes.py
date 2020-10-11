"""Package and dependency imports."""
from flask import Blueprint, jsonify, request
from hydra import db
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_raw_jwt,
)

channels = Blueprint("channels", __name__)

# TODO: test with Postman when bug is figured out.


@channels.route("/")
# @jwt_required
def showChannels(groupId):
    """
    For channels in specified group, return channel information.

    channel.id, channel.name, channel.description
    """
    channels = db.channels.find_all({"groupId": groupId})
    return jsonify({channels})


@channels.route("/create", methods=["POST", "PUT"])
# @jwt_required
def createChannel(groupId):
    """Create channel document in database."""
    print("In function")
    name = request.json.get("name")
    print(f"Name: {name}")
    dis = request.json.get("dis")
    print(f"Description: {dis}")
    newChannel = {"name": name, "dis": dis}
    print(f"New Channel: {newChannel}")
    insertedChannel = db.channels.insert_one(newChannel)
    print(f"Inserted Channel: {insertedChannel}")
    return jsonify({"msg": "This has been successful"})


@channels.route("/delete", methods=["POST"])
@jwt_required
def deleteChannel(groupId):
    pass
