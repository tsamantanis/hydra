from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from bson.json_util import dumps
from bson.objectid import ObjectId
from hydra import db
from hydra.users.utils import loadUserToken
import stripe
import os

groups = Blueprint("groups", __name__)


@groups.route("", methods=["GET"])
@login_required
def allGroups():
    """Show all groups to users, enable search on client."""
    groups = db.Group.find({})
    groupData = []
    print(f"Getting data: {groups}")
    for group in groups:
        print(group)
        groupData.append(
            {
                "_id": str(group["_id"]),
                "name": group["name"],
                "dis": group["dis"],
                "ownerId": group["ownerId"],
                "contentIds": group["contentIds"],
                "keywords": group["keywords"],
            }
        )
    return dumps(groupData), 200


@groups.route("/yourgroups", methods=["GET"])
@login_required
def UserSections():
    """Show all groups to current user's enrolled groups."""
    groups = []
    user = db.users.find_one({"_id": ObjectId(current_user.id)})
    print(f"user {user}")
    print(user["enrolledGroups"])
    for groups in user["enrolledGroups"]:
        groups = db.Group.find({})
    print(groups)
    data = [
        {
            "name": group["name"],
            "groupId": group["_id"],
            "ownerId": group["ownerId"],
            "enrolledIds": [
                {str(index): enrolledId}
                for index, enrolledId in enumerate(group["enrolledIds"])
            ],
            "contentIds": [
                {str(index): contentId}
                for index, contentId in enumerate(group["contentIds"])
            ],
            "assignmentIds": [
                {str(index): assignmentId}
                for index, assignmentId in enumerate(group["assignmentIds"])
            ],
            "dis": group["dis"],
            "keywords": [
                {str(index): keyword}
                for index, keyword in enumerate(group["keywords"])
            ],
        }
        for group in groups
    ]
    return dumps(data), 200


@groups.route("/create", methods=["POST"])
@login_required
def groupCreate():
    """Create new group."""
    postData = request.json
    db.Group.insert_one(
        {
            "ownerId": postData["ownerId"],
            "enrolledIds": [],
            "contentIds": [],
            "assignmentIds": [],
            "dis": postData["dis"],
            "channelsIds": [],
            "keywords": postData["keywords"],
            "name": postData["name"],
            "userIoc": [],
        }
    )
    return jsonify({"msg": "Your group has been created"}), 200


@groups.route("/search", methods=["GET"])
@login_required
def groupSearch():
    """Search for groups to join (user)."""
    params = request.args.get("params")
    groups = list()
    for word in params:
        groups.append(db.Group.find_one_or_404({"$text": {"$search": word}}))
    groups
    print(groups)
    data = [
        {
            "name": group["_id"],
            "groupId": group["_id"],
        }
        for group in groups
    ]
    return dumps(data), 200


@groups.route("/<groupId>", methods=["GET"])
@login_required
def groupId(groupId):
    """Access group details based on groupId"""
    group = db.Group.find_one({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    data = {
        "name": group["name"],
        "groupId": str(group["_id"]),
        "ownerId": group["ownerId"],
        "enrolledIds": [group["enrolledIds"]] or None,
        "contentIds": [group["contentIds"]] or None,
        "dis": group["dis"],
        "keywords": [group["keywords"]],
    }
    return dumps(data), 200


@groups.route("/<groupId>/join", methods=["GET", "POST"])
@login_required
def groupIdJoin(groupId):
    """
    User can join group.

    Add group id to user's enrolledGroups and create
    stripe subscription object.
    """
    group = db.Group.find_one({"_id": ObjectId(groupId)})
    user = db.users.find_one({"_id": ObjectId(current_user.id)})
    if group is not None:
        if group['enrolledIds'] is None:
            updatedGroup = db.Group.update_one({'_id': group['_id']}, {"$set": {
                "enrolledIds": [user['_id']]
            }})
        else:
            updatedGroup = db.Group.update_one({'_id': group['_id']}, {"$set": {
                "enrolledIds": group['enrolledIds'].append(user['_id'])
            }})
        if user['enrolledGroups'] is None:
            updatedUser = db.users.update_one({'_id': user['_id']}, {
                "$set": {
                    "enrolledGroups": [group['_id']]
                }
            })
        else:
            updatedGroup = db.users.update_one({'_id': group['_id']}, {
                "$set": {
                    "enrolledIds": user['enrolledGroups'].append(group['_id'])
                    }
            })
        return jsonify({"msg": "Group successfully joined!"}), 200
    elif group is None:
        return jsonify({"msg": "Group Not Found"}), 404
    return jsonify({"msg": "something went wrong"})


@groups.route("/<groupId>/leave", methods=["POST"])
@login_required
def groupIdLeave(groupId):
    """Remove user from group."""
    if (
        groupId not in current_user.enrolledGroups
        or groupId not in current_user.ownedGroups
    ):
        return jsonify({"msg": "Not Enrolled"}), 200
    group = db.Group.find_one({"_id": ObjectId(groupId)})
    if group is None:
        return jsonify({"msg": "Group Not Found"}), 404
    group['enrolledIds'].remove(current_user.id)
    current_user.enrolledGroups.remove(group["_id"])
    return jsonify({"msg": "Group Left"}), 200
