from hydra import flask
from flask import Blueprint
from flask_jwt_extended import jwt_required
from os import path
from bson.objectid import ObjectId 
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_raw_jwt,
)

groupBlueprint = Blueprint("Content", __name__)

# base path /groups/<groupId>/assignments
@groupBlueprint.route("/", methods=["GET"])
@jwt_required
def contentAll(groupId):
    group = db.Group.find({"_id": ObjectId(groupId)})
    assignments = [db.Assignment.find({"_id" : ObjectId(assignmentId)}) for assignmentId in group.assignmentIds]
    data = [
        {
            "assignmentId": assignment.id,
            "name": assignment.name,
            "dis": assignment.dis,
        }
        for assignment in assignments
    ]
    return flask.jsonify(data), ""

@groupBlueprint.route("/<assignmentId>", methods=["GET", "PATCH"])
@jwt_required
def contentId(groupId, assignmentId):
    httpCode = 200
    group = db.Group.find({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    assignment = db.Assignment.find({"_id": ObjectId(assignmentId)})
    if assignment is None:
        return "Assignment Not Found", 404
    if request.method == 'DELETE':
        for pdfId in assignment.pdfIds:
            db.Pdf.deleteOne(
                {
                    "_id": ObjectId(pdfId)
                }
            )
        db.Assignment.deleteOne(
            {
                "_id" : ObjectId(assignment._id)
            }
        )
        httpCode = 204
        return 'Assignment Deleted', httpCode
    if request.method == 'PATCH':
        patchData = request.json
        patchFiles = request.files

        for pdfData in patchData.get('pdfs'):
            jsonSet = {}
            if pdfData.dis != None:
                jsonSet.dis = pdfData.dis
            if pdfData.url != None:
                jsonSet.url = pdfData.url   
            elif patchFiles.get(pdfData._id) != None:
                pdfFile = patchFiles.get(pdfData._id)
                jsonSet.url = path.join(app.config["PDF_PATH"], '{0}.{1}'.format({pdfData._id}, pdfFile.filename.split('.')[-1]))
                pdfFile.save(jsonSet.url)
            if pdfData.pdfId == True:
                db.Pdf.update(
                    { '_id': pdfData.pdfId },
                    { '$set':
                        jsonSet
                    }
                )
            else:
                createdPdf = db.Pdf.insert(
                    jsonSet
                )
                assignment.pdfIds.append(createdPdf._id)
        httpCode = 204
    group = db.Group.find({"_id": ObjectId(groupId)})
    assignment = db.Assignment.find({"_id": ObjectId(assignmentId)})
    pdfs = [db.Pdf.find({"_id": ObjectId(pdfId)}) for pdfId in assignment.pdfIds]
    data = {
        "name": assignment.name,
        "dis": assignment.dis,
        "assignmentId": assignment._id,
        "pdfs": [
            {
                str(index): {
                    'pdfId' : pdf._id,
                    'url' : pdf.url,
                    'dis' : pdf.dis
                }
            }
            for index, pdf in enumerate(pdfs)
        ],
    }
    return flask.jsonify(data), httpCode

@groupBlueprint.route("/create", methods=["POST"])
@jwt_required
def assignmentCreate(groupId):
    postData = request.json
    postFiles = request.files
    assignment = db.Assignment.insert_one(
        {
            'name' : postData.get('name'),
            'dis' : postData.get('dis'),
            'pdfs' : [],
        }
    )

    for pdfData in postData.get('pdfs'):
        jsonSet = {}
        if pdfData.dis != None:
            jsonSet.dis = pdfData.dis
        if pdfData.url != None:
            jsonSet.url = pdfData.url   
        elif postFiles.get(pdfData.tempFileId) != None:
            pdfFile = postFiles.get(pdfData.tempFileId)
            jsonSet.url = path.join(app.config["PDF_PATH"], '{0}.{1}'.format({pdfData._id}, pdfFile.filename.split('.')[-1]))
            pdfFile.save(jsonSet.url)
        else:
            createdPdf = db.Pdf.insert(
                jsonSet
            )
            assignment.pdfIds.append(createdPdf._id)
    group = db.Group.find({"_id": ObjectId(groupId)})
    group.assignmentIds.append(assignment._id)
    return "", 200

@groupBlueprint.route("/assignmentId/pdfs/<pdfId>", methods=["DELETE"])
@jwt_required
def pdfRemove(groupId, assignmentId, pdfId):
    assignment = db.assignment.find({"_id": ObjectId(assignmentId)})
    assignment.pdfIds.remove(pdfId)
    db.Pdf.deleteOne(
            {
                "_id": ObjectId(pdfId)
            }
        )
    return 'Assignment Deleted', 204

@groupBlueprint.route("/assignmentId/videos/<videoId>", methods=["DELETE"])
@jwt_required
def pdfRemove(groupId, assignmentId, videoId):
    assignment = db.Assignment.find({"_id": ObjectId(assignmentId)})
    assignment.videoIds.remove(videoId)
    db.Video.deleteOne(
            {
                "_id": ObjectId(videoId)
            }
        )
    return 'Assignment Deleted', 204