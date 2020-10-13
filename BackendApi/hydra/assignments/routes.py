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
        }
        for assignment in assignments
    ]
    return dumps(data), 200


# TODO: More testing on this when we can upload files to FE


@assignments.route("/<assignmentId>/<channelId>", methods=["GET", "PATCH", "DELETE"])
def contentId(groupId, assignmentId, channelId):
    """Access assignment details, patch and delete."""
    httpCode = 200
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
        }
        return dumps(data), 200
    if request.method == "DELETE":
        for pdfId in assignment["pdfIds"]:
            db.Pdf.deleteOne({"_id": ObjectId(pdfId)})
        db.Assignment.deleteOne({"_id": ObjectId(assignment["_id"])})
        return jsonify({"msg": "Assignment Deleted"}), 204
    elif request.method == "PATCH":
        patchData = request.json
        patchFiles = request.files
        
        return jsonify(
            {"msg": "No files associated with this assignment."}
        )


@assignments.route("/create", methods=["POST"])
def assignmentCreate(groupId):
    """Create assignment and add to database. Return success message."""
    postData = request.json
    postFiles = request.files
    insertAssignment = db.Assignment.insert_one(
        {
            "name": postData.get("name"),
            "dis": postData.get("dis"),
            "maxGrade": postData.get("maxGrade"),
            "dueDate": postData.get("dueDate"),
            "startDate": postData.get("startDate"),
            "text": postData.get("text"),
        }
    )
    db.channels.insert_one(
        {
            "name": postData.get("name"),
            "dis": postData.get("dis"),
            "category": "Assignments",
            "groupId": groupId,
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


@assignments.route("/<assignmentId>/<channelId>/pdfs/add", methods=["POST"])
@login_required
def pdfAdd(groupId, assignmentId, channelId):
    """Add pdfs to existing assignment."""
    jsonSet = {}
    assignment = db.Assignment.find_one_or_404(
        {"_id": ObjectId(assignmentId)}
    )
    postFiles = request.files
    if request.json.get("dis") is not None:
        jsonSet["dis"] = request.json.get("dis")
    pdf = db.Pdf.insert_one(jsonSet)
    assignment["pdfs"].append(pdf.inserted_id)
    if request.json.get("url") is not None:
        jsonSet["url"] = request.json.get("url")
    elif postFiles.get(request.json.get("tempFileId")) is not None:
        contentFile = postFiles.get(request.json.get("tempFileId"))
        jsonSet["url"] = path.join(
            app.config["PDF_PATH"],
            "{0}.{1}".format(
                {pdf["_id"]},
                contentFile.filename.split(".")[-1],
            ),
        )
        contentFile.save(jsonSet["url"])
    db.Pdf.update({"_id": ObjectId(pdf["_id"])}, {"$set": jsonSet})
    return
