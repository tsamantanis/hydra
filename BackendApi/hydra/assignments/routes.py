# from hydra import flask
from os import path

from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request
from hydra import app, db

assignments = Blueprint("assignments", __name__)


# base path /groups/<groupId>/assignments
@assignments.route("/", methods=["GET"])
def contentAll(groupId):
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


@assignments.route("/<assignmentId>", methods=["GET", "PATCH"])
def contentId(groupId, assignmentId):
    """Access assignment details, patch and delete."""
    httpCode = 200
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    assignment = db.Assignment.find_one_or_404(
        {"_id": ObjectId(assignmentId)}
    )
    if assignment is None:
        return "Assignment Not Found", 404
    if request.method == "DELETE":
        for pdfId in assignment["pdfIds"]:
            db.Pdf.deleteOne({"_id": ObjectId(pdfId)})
        db.Assignment.deleteOne({"_id": ObjectId(assignment["_id"])})
        httpCode = 204
        return "Assignment Deleted", httpCode
    if request.method == "PATCH":
        patchData = request.json
        patchFiles = request.files
        if patchData.get("pdfs"):
            for pdfData in patchData.get("pdfs"):
                jsonSet = {}
                if pdfData["dis"] is not None:
                    jsonSet["dis"] = pdfData["dis"]
                if pdfData["url"] is not None:
                    jsonSet["url"] = pdfData["url"]
                elif patchFiles.get(pdfData["_id"]) is not None:
                    pdfFile = patchFiles.get(pdfData["_id"])
                    jsonSet["url"] = path.join(
                        app.config["PDF_PATH"],
                        "{0}.{1}".format(
                            {pdfData["_id"]}, pdfFile.filename.split(".")[-1]
                        ),
                    )
                    pdfFile.save(jsonSet["url"])
                if pdfData["pdfId"]:
                    db.Pdf.update({"_id": pdfData.pdfId}, {"$set": jsonSet})
                else:
                    createdPdf = db.Pdf.insert(jsonSet)
                    assignment.pdfIds.append(createdPdf["_id"])
                httpCode = 204
            group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
            assignment = db.Assignment.find_one_or_404(
                {"_id": ObjectId(assignmentId)}
            )
            pdfs = [
                db.Pdf.find_one_or_404({"_id": ObjectId(pdfId)})
                for pdfId in assignment["pdfIds"]
            ]
            data = {
                "name": assignment["name"],
                "dis": assignment["dis"],
                "assignmentId": assignment["_id"],
                "pdfs": [
                    {
                        str(index): {
                            "pdfId": pdf["_id"],
                            "url": pdf["url"],
                            "dis": pdf["dis"],
                        }
                    }
                    for index, pdf in enumerate(pdfs)
                ],
            }
            return dumps(data), httpCode
        else:
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
            "pdfs": [],
        }
    )
    getId = insertAssignment.inserted_id
    assignment = db.Assignment.find_one_or_404({"_id": ObjectId(getId)})

    if postData.get("pdfs"):
        for pdfData in postData.get("pdfs"):
            jsonSet = {}
            if pdfData["dis"] is not None:
                jsonSet["dis"] = pdfData["dis"]
            if pdfData["url"] is not None:
                jsonSet["url"] = pdfData["url"]
            elif postFiles.get(pdfData["tempFileId"]) is not None:
                pdfFile = postFiles.get(pdfData["tempFileId"])
                jsonSet["url"] = path.join(
                    app.config["PDF_PATH"],
                    "{0}.{1}".format(
                        {pdfData["_id"]}, pdfFile.filename.split(".")[-1]
                    ),
                )
                pdfFile.save(jsonSet["url"])
            else:
                createdPdf = db.Pdf.insert(jsonSet)
                assignment.pdfIds.append(createdPdf["_id"])
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    group["assignmentIds"].append(assignment["_id"])
    return jsonify({"msg": "Your assignment has been created."}), 200



@assignments.route("/<assignmentId>/pdfs/<pdfId>", methods=["DELETE", "PATCH"])
# @jwt_required
def pdfId(groupId, assignmentId, pdfId):
    if request.method == "DELETE":
        db.Pdf.deleteOne({"_id": ObjectId(pdfId)})
        return "PDF Deleted", 204
    if request.method == "PATCH":
        jsonSet = {}
        pdf = db.Pdf.find({"_id": ObjectId(pdfId)})
        if request.json.get('tempFileId') != None:
            contentFile = request.files.get(request.json.get('tempFileId'))
            jsonSet["url"] = path.join(
                path,
                "{0}.{1}".format(
                    {pdf["_id"]},
                    contentFile.filename.split(".")[-1],
                ),
            )
            contentFile.save(jsonSet["url"])
        elif request.json.get('url') != None:
            jsonSet['url'] = request.json.get('url')
        if request.json.get('dis') != None:
            jsonSet['dis'] = request.json.get('dis')
        db.Pdf.update(
            {"_id":  ObjectId(pdfId)}, {"$set": jsonSet}
        )
    return "Patch Made", 200



@assignments.route("/<assignmentId>/pdfs/add", methods=["POST"])
# @jwt_required
def pdfAdd(groupId, assignmentId):
    jsonSet = {}
    assignment = db.Assignment.find_one_or_404({"_id": ObjectId(assignmentId)})
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
            path,
            "{0}.{1}".format(
                {pdf["_id"]},
                contentFile.filename.split(".")[-1],
            ),
        )
        contentFile.save(jsonSet["url"])
    db.Pdf.update(
            {"_id":  ObjectId(pdf["_id"])}, {"$set": jsonSet}
        )
