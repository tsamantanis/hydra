"""Dependency and package import."""
import flask
from hydra import db, app
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from os import path
from bson.objectid import ObjectId
from bson.json_util import dumps
from hydra.users.utils import loadUserToken

submissions = Blueprint("submission", __name__)

# base path /groups/<groupId>/assignments/<assignmentId>/submissions


@submissions.route("/", methods=["GET"])
@login_required
def contentAll(groupId, assignmentId):
    """
    Return submission information.

    Check groupId and AssignmentId to be sure assignment and group exist.
    Loop through submissionIds in assignment to show submission data.
    """
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    if group is None:
        return jsonify({"msg": "Group Not Found"}), 404
    assignment = db.Assignment.find_one_or_404(
        {"_id": ObjectId(assignmentId)}
    )
    if assignment is None:
        return jsonify({"msg": "Assignment not found"}), 404
    submissions = [
        db.Submission.find_one_or_404({"_id": ObjectId(submissionId)})
        for submissionId in assignment["submissionIds"]
    ]

    data = [
        {
            "submissionId": submission["_id"],
            "userId": submission["userId"],
            "url": submission["url"],
            "scoredGrade": submission["scoredGrade"],
            "timestamp": submission["timestamp"],
        }
        for submission in submissions
    ]
    return dumps(data), 200


@submissions.route("/<submissionId>", methods=["GET", "PATCH"])
@login_required
def contentId(groupId, assignmentId, submissionId):
    """Return submission details."""
    httpCode = 200
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    assignment = db.Assignment.find_one_or_404(
        {"_id": ObjectId(assignmentId)}
    )
    if assignment is None:
        return "Assignment Not Found", 404
    submission = db.Submission.find_one_or_404(
        {"_id": ObjectId(submissionId)}
    )
    if submission is None:
        return jsonify({"msg": "Submission Not Found"}), 404
    if request.method == "DELETE":
        db.Submission.deleteOne({"_id": ObjectId(submission["_id"])})
        return jsonify({"msg": "Submission successfully deleted."}), 204
    if request.method == "PATCH":
        patchData = request.json
        patchFiles = request.files
        jsonSet = {}
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    assignment = db.Assignment.find_one_or_404(
        {"_id": ObjectId(assignmentId)}
    )
    data = {
        "name": assignment["name"],
        "dis": assignment["dis"],
        "assignmentId": assignment["_id"],
        "url" : assignment["url"],
    }
    return dumps(data), httpCode


@submissions.route("/create", methods=["POST"])
@login_required
def submissionCreate(groupId):
    """Create new assignment submission."""
    postData = request.json
    postFiles = request.files
    assignment = db.Submission.insert_one(
        {
            "name": postData.get("name"),
            "dis": postData.get("dis"),
            "url": postData.get("url"),
        }
    )
    group = db.Group.find({"_id": ObjectId(groupId)})
    group.assignmentIds.append(assignment.inserted_id)
    return "", 200
