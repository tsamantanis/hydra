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


@channels.route("/channels/<groupId>")
@jwt_required
def showChannels(groupId):
    """
    For channels in specified group, return channel information.

    channel.id, channel.name, channel.description
    """
    channels = db.channels.find_all({"groupId": groupId})
    return jsonify({channels})


@channels.route("/channels/<groupId>/create", methods=["POST", "PUT"])
@jwt_required
def createChannel(groupId):
    """Create channel document in database."""
    name = request.json.get("name")
    description = request.json.get("description")
    newChannel = {"name": name, "description": description}
    insertedChannel = db.channels.insert_one(newChannel)
    return jsonify(insertedChannel)


@channels.route("/channels/<groupId>/delete", methods=["POST"])
@jwt_required
def deleteChannel(groupId):
    pass
