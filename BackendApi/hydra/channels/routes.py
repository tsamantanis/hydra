"""Package and dependency imports."""
from flask import Blueprint, jsonify, request
from hydra import db
from flask_login import current_user, login_required
from bson.json_util import dumps
from bson.objectid import ObjectId
from hydra.users.utils import loadUserToken

channels = Blueprint("channels", __name__)


@channels.route("")
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

@channels.route("/<channelId>/posts")
@login_required
def getChannelPosts(groupId, channelId):
    """
    For channels in specified group, return channel information.

    channel.id, channel.name, channel.description, channel.category
    """

    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    channel = db.channels.find_one_or_404({"_id": ObjectId(channelId)})
    post = None
    if channel['category'] == 'content':
        post = db.Content.find_one({"channelId": ObjectId(channelId)})
    elif channel['category'] == 'assignments':
        post = db.Assignment.find_one({"channelId": ObjectId(channelId)})
    elif channel['category'] == 'discussions':
        post = db.Discussion.find_one({"channelId": ObjectId(channelId)})
    if group is None or post is None:
        return jsonify({"error": "Invalid id provided, please try again."})
    owner = db.users.find_one_or_404({"_id": ObjectId(group['ownerId'])})
    data = {
        "postId": str(post["_id"]),
        "channelId": post["channelId"],
        "name": post["name"],
        "dis": post["dis"],
        "url": post["url"] if post["url"] != None else "",
        "ownerName" : "{0} {1}".format(owner['firstName'], owner['lastName']) if owner != None else ""
    }
    return dumps(data), 200
