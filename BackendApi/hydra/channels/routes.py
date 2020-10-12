"""Package and dependency imports."""
from flask import Blueprint, jsonify, request
from hydra import db
from flask_login import current_user, login_required
from bson.json_util import dumps
from bson.objectid import ObjectId

channels = Blueprint("channels", __name__)


@channels.route("/")
@login_required
def showChannels(groupId):
    """
    For channels in specified group, return channel information.

    channel.id, channel.name, channel.description
    """
    channels = db.channels.find({"groupId": groupId})
    return dumps(channels)


@channels.route("/create", methods=["POST", "PUT"])
@login_required
def createChannel(groupId):
    """Create channel document in database."""
    name = request.json.get("name")
    dis = request.json.get("dis")
    category = request.json.get("category")
    if name and dis and category:
        group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
        newChannel = {
            "name": name,
            "dis": dis,
            "category": category,
            "groupId": groupId,
        }
        insertedChannel = db.channels.insert_one(newChannel)
        group["channelsIds"].append(insertedChannel.inserted_id)
        return jsonify({"msg": f"{name} has been added"})
    else:
        return jsonify({"msg": "Missing information, please try again."})


@channels.route("/delete/<channelId>", methods=["DELETE"])
@login_required
def deleteChannel(groupId, channelId):
    """Delete channel from database."""
    channel = db.channels.find_one_or_404({"_id": ObjectId(channelId)})
    db.channels.delete_one(channel)
    return jsonify({"msg": "This channel has been deleted"})


@channels.route("/<channelId>")
@login_required
def getChannel(groupId, channelId):
    """
    For channels in specified group, return channel information.

    channel.id, channel.name, channel.description, channel.category
    """
    channel = db.channels.find_one_or_404({"_id": ObjectId(channelId)})
    channelData = {
        "id": channel["_id"],
        "name": channel["name"],
        "dis": channel["dis"],
        "category": channel["category"],
    }
    return dumps(channelData)
