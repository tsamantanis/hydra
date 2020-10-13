# from hydra import flask
from os import path
from flask_login import login_required
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request, send_from_directory
from hydra import app, db
from hydra.users.utils import loadUserToken

assignments = Blueprint("assignments", __name__)

# base path /groups/<groupId>/channels/assignments


@assignments.route("/<channelId>", methods=["GET"])
def contentAll(groupId, channelId):
    """Show all assignments for particular group."""
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    assignments = [
        db.Assignment.find({"_id": ObjectId(assignmentId)})
        for assignmentId in group["assignmentIds"]
    ]
    data = [
        {
            "assignmentId": assignment["_id"],
            "name": assignment["name"],
            "dis": assignment["dis"],
            "maxGrade": assignment["maxGrade"],
            "startDate": assignment["startDate"],
            "dueDate": assignment["dueDate"],
            "type": assignment["type"],
            "url": assignment["url"],
        }
        for assignment in assignments
    ]
    return dumps(data), 200


@assignments.route("/<assignmentId>/<channelId>", methods=["GET", "PATCH", "DELETE"])
def contentId(groupId, assignmentId, channelId):
    """Access assignment details, patch and delete."""
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    assignment = db.Assignment.find_one_or_404(
        {"_id": ObjectId(assignmentId)}
    )
    if assignment is None:
        return jsonify({"msg": "Assignment Not Found"}), 404
    if request.method == "GET":
        data = {
            "assignmentId": assignmentId,
            "name": assignment["name"],
            "dis": assignment["dis"],
            "maxGrade": assignment["maxGrade"],
            "startDate": assignment["startDate"],
            "dueDate": assignment["dueDate"],
            "url": assignment["url"],
        }
        return dumps(data), 200
    if request.method == "DELETE":
        db.Assignment.deleteOne({"_id": ObjectId(assignment["_id"])})
        return jsonify({"msg": "Assignment Deleted"}), 204
    # elif request.method == "PATCH":
    #     patchData = request.json
    #     newName = request.json.get('name')
    #     newDis = request.json.get("dis")
    #     newMaxGrade = request.json.get("maxGrade")
    #     newStartDate = request.json.get("startDate")
    #     newDueDate = request.json.get("dueDate")
    #     newUrl = request.json.get("url")
    #     db.Assignment.update_one({'_id': ObjectId(assignment['_id'])}, {
    #         "$set": {
    #
    #         }
    #     })


@assignments.route("/create", methods=["POST"])
def assignmentCreate(groupId):
    """Create assignment and add to database. Return success message."""
    postData = request.json
    new_channel = db.channels.insert_one(
            {
                "name": postData.get("name"),
                "dis": postData.get("dis"),
                "category": "assignments",
                "groupId": groupId,
            }
        )
    insertAssignment = db.Assignment.insert_one(
        {
            "name": postData.get("name"),
            "dis": postData.get("dis"),
            "maxGrade": postData.get("maxGrade"),
            "dueDate": postData.get("dueDate"),
            "startDate": postData.get("startDate"),
            "url": postData.get("url"),
            "channelId": new_channel.inserted_id
        }
    )

    getId = insertAssignment.inserted_id
    assignment = db.Assignment.find_one({"_id": ObjectId(getId)})
    print(f"Assignment {assignment}")

    group = db.Group.find_one({"_id": ObjectId(groupId)})
    print(f"Group from EOF: {group}")
    group["assignmentIds"].append(assignment["_id"])
    print(f"Group assignmentIds after append: {group['assignmentIds']}")
    return jsonify({"msg": "Your assignment has been created."}), 200
