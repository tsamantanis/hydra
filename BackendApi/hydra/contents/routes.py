"""Dependency and package imports."""
from flask import Blueprint, jsonify, request
from hydra.users.utils import loadUserToken
from hydra import db, app
from os import path
from hydra.contents.utils import (
    createContent,
    patchContent,
)
from bson.json_util import dumps
from bson.objectid import ObjectId

contents = Blueprint("contents", __name__)

# base path /groups/<groupId>/channels/contents


@contents.route("/<channelId>", methods=["GET"])
def contentAll(groupId, channelId):
    """Show contents for group id. Return as data to front end."""
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    contents = db.Contents.find({"channelId": channelId})
    print(contents)
    if group is None or contents is None:
        return jsonify({"msg": "Invalid id provided, please try again."})
    print(f"Contents: {contents}")
    owner = db.users.find_one_or_404({"_id": ObjectId(group['ownerId'])})
    data = [
        {
            "contentId": content["_id"],
            "channelId": content["channelId"],
            "name": content["name"],
            "dis": content["dis"],
            "ownerName": ["{0} {1}".format(owner['firstname'], owner['lastname']) if owner is not None else ""],
            "text": content["text"],
            "url": content["url"],
        }
        for content in contents
    ]
    print(f"Data: {data}")
    return dumps(data), 200


@contents.route("/<contentId>/<channelId>", methods=["GET", "PATCH", "DELETE"])
def contentId(groupId, contentId, channelId):
    """
    Access content by id.

    Allow for deletion, adding new content.
    For each different method, return JSON data
    corresponding to action taken.
    """
    group = db.Group.find_one({"_id": ObjectId(groupId)})
    if not group:
        return jsonify({"msg": "Group Not Found"}), 404
    content = db.Content.find_one({"_id": ObjectId(contentId)})
    if not content:
        return jsonify({"msg": "Content Not Found"}), 404
    if request.method == "DELETE":
        db.Content.deleteOne({"_id": ObjectId(content["_id"])})
        return jsonify({"msg": "Content Deleted"}), 204
    group = db.Group.find_one({"_id": ObjectId(groupId)})
    content = db.Content.find_one({"_id": ObjectId(contentId)})

    data = {
        "name": content["name"],
        "dis": content["dis"],
        "contentId": content["_id"],
        "text": content["text"],
        "url": content["url"],
        "channelId": content["channelId"],
    }
    return dumps(data), 200


@contents.route("/create", methods=["POST"])
def contentCreate(groupId):
    """
    Create content and store video or pdf url.

    Return success message for front end.
    """
    try:
        print(request.headers.get("Authorization"))
        postData = request.json

        newChannel = {
            "name": postData.get("name"),
            "dis": postData.get("dis"),
            "category": "content",
            "groupId": groupId,
        }
        insertedChannel = db.channels.insert_one(newChannel)
        group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
        content = db.Content.insert_one(
            {
                "name": postData.get("name"),
                "dis": postData.get("dis"),
                "text": [],
                "url": [postData.get('url')],
                "channelId": insertedChannel.inserted_id,
            }
        )
        createdContent = db.Content.find_one_or_404(
            {"name": postData.get("name")}
        )
        group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
        group["contentIds"].append(createdContent["_id"])
        return dumps(createdContent)
    except Exception as e:
        print(e)
        return jsonify({"msg": "Unable to upload files"}), 200


@contents.route("/<contentId>/<channelId>/text/add", methods=["POST"])
def videoAdd(groupId, contentId):
    """Add singular video to channel content."""
    jsonSet = {}
    content = db.Content.find_one_or_404({"_id": ObjectId(contentId)})
    jsonSet['text'] = content['text']
    jsonSet['text'].append(request.json.get('text'))
    db.Content.update({"_id": ObjectId(content["_id"])}, {"$set": jsonSet})
    return jsonify({"msg": "Your text has been added!"}), 200


@contents.route("/<contentId>/<channelId>/url/add", methods=["POST"])
def pdfAdd(groupId, contentId):
    """Add single pdf document to channel content."""
    jsonSet = {}
    content = db.Content.find_one_or_404({"_id": ObjectId(contentId)})
    jsonSet['url'] = content['url']
    jsonSet['url'].append(request.json.get('url'))
    db.Content.update({"_id": ObjectId(content["_id"])}, {"$set": jsonSet})
    return jsonify({"msg": "Your url has been added!"}), 200
