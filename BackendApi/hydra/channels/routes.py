"""Package and dependency imports."""
from flask import Blueprint, jsonify, request
from hydra import db

channels = Blueprint("channels", __name__)


@channels.route("/groups/<groupId>/channels")
def showChannels(groupId):
    """
    For channels in specified group, return channel information.

    channel.id, channel.name, channel.description
    """
    channels = db.channels.find_all({"groupId": groupId})
    return jsonify({channels})


@channels.route("/groups/<groupId>/channels/create", methods=["POST", "PUT"])
def createChannel(groupId):
    """Create channel document in database."""

    # TODO: Ensure that we're adding channelid to the group object
    # TODO: Add category to channel object (Assignments, lectures, chat)
    name = request.json.get("name")
    dis = request.json.get("dis")
    newChannel = {"name": name, "dis": dis}
    insertedChannel = db.channels.insert_one(newChannel)
    return jsonify({"msg": "{{name}} has been added"})


@channels.route("/channels/<groupId>/delete", methods=["POST"])
def deleteChannel(groupId):
    pass
