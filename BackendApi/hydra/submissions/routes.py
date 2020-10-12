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

submissions = Blueprint("Submission", __name__)

# base path /groups/<groupId>/assignments/<assignmentId>/submissions
@groupBlueprint.route("/", methods=["GET"])
# @jwt_required
def contentAll(groupId, assignmentId):
    group = db.Group.find({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    assignment = db.Assignment.find({"_id": ObjectId(assignmentId)})
    if assignment is None:
        return "Assignment Not Found", 404
    submissions = [db.Submission.find({"_id" : ObjectId(submissionId)}) for submissionId in assignment.submissionIds]

    data = [
        {
            "submissionId": submission._id,
            "userId": submission.userId,
            "pdfUrl": submission.pdfUrl,
            "scoredGrade": submission.scoredGrade,
            "timestamp": submission.timestamp
        }
        for submission in submissions
    ]
    return flask.jsonify(data), 200

@groupBlueprint.route("/<submissionId>", methods=["GET", "PATCH"])
# @jwt_required
def contentId(groupId, assignmentId, submissionId):
    httpCode = 200
    group = db.Group.find({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    assignment = db.Assignment.find({"_id": ObjectId(assignmentId)})
    if assignment is None:
        return "Assignment Not Found", 404
    submission = db.Submission.find({"_id": ObjectId(submissionId)})
    if submission is None:
        return "Submission Not Found", 404
    if request.method == 'DELETE':
        db.Submission.deleteOne(
            {
                "_id" : ObjectId(submission['_id'])
            }
        )
        httpCode = 204
        return 'Assignment Deleted', httpCode
    if request.method == 'PATCH':
        patchData = request.json
        patchFiles = request.files

        if patchFiles.get(patchData.tempFileId) != None:
            pdfFile = patchFiles.get(patchData.tempFileId)
            jsonSet.pdfUrl = path.join(app.config["PDF_PATH"], '{0}.{1}'.format({patchData.tempFileId}, pdfFile.filename.split('.')[-1]))
            pdfFile.save(jsonSet.pdfUrl)
        if pdfData.scoredGrade != None:
            jsonSet.scoredGrade = pdfData.scoredGrade
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
# @jwt_required
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

@groupBlueprint.route("/<assignmentId>/pdfs/<pdfId>", methods=["DELETE"])
# @jwt_required
def pdfRemove(groupId, assignmentId, pdfId):
    assignment = db.Assignment.find({"_id": ObjectId(assignmentId)})
    assignment.pdfIds.remove(pdfId)
    db.Pdf.deleteOne(
            {
                "_id": ObjectId(pdfId)
            }
        )
    return 'Assignment Deleted', 204
