"""Package and dependency imports."""
from flask import Blueprint, jsonify, request
from hydra import db

channels = Blueprint("channels", __name__)

# TODO: test with Postman when bug is figured out.


@channels.route("/channels/<group_id>")
def showChannels(group_id):
    """
    For channels in specified group, return channel information.

    channel.id, channel.name, channel.description
    """
    channels = db.channels.find_all({"group_id": group_id})
    return jsonify({channels})


@channels.route("/channels/<group_id>/create", methods=["POST", "PUT"])
def createChannel(group_id):
    """Create channel document in database."""
    name = request.json.get("name")
    description = request.json.get("description")
    newChannel = {"name": name, "description": description}
    insertedChannel = db.channels.insert_one(newChannel)
    return jsonify(insertedChannel)


@channels.route("/channels/<group_id>/delete", methods=["POST"])
def deleteChannel(group_id):
    pass
