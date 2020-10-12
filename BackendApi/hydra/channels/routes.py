"""Package and dependency imports."""
from flask import Blueprint, jsonify, request
from hydra import db
from flask_login import current_user
from bson.json_util import dumps

channels = Blueprint("channels", __name__)


@channels.route("/groups/<groupId>/channels")
def showChannels(groupId):
    """
    For channels in specified group, return channel information.

    channel.id, channel.name, channel.description
    """
    channels = list(db.channels.find({"groupId": groupId}))
    return dumps(channels)


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


@channels.route("/<channelId>")
# @jwt_required
def getChannel(groupId, channelId):
    """
    For channels in specified group, return channel information.

    channel.id, channel.name, channel.description
    """
    channel = db.channels.find_all(
        {"groupId": groupId, "_id": ObjectId(channelId)}
    )
    return jsonify({channel})
