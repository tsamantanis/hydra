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

# base path /groups/<groupId>/contents
@groupBlueprint.route("/", methods=["GET"])
@jwt_required
def contentAll(groupId):
    group = db.Group.find({"_id": ObjectId(groupId)})
    contents = [db.Content.find({"_id" : ObjectId(contentId)}) for contentId in group.content_ids]
    data = [
        {
            "contentId": content.id,
            "name": content.name,
            "dis": content.dis,
        }
        for content in contents
    ]
    return flask.jsonify(data), ""

@groupBlueprint.route("/<contentId>", methods=["GET", "PATCH"])
@jwt_required
def contentId(groupId, contentId):
    httpCode = 200
    group = db.Group.find({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    content = db.Content.find({"_id": ObjectId(contentId)})
    if content is None:
        return "Content Not Found", 404
    if request.method == 'DELETE':
        for videoId in content.videoIds:
            db.Video.deleteOne(
                {
                    "_id": ObjectId(videoId)
                }
            )
        for pdfId in content.pdfIds:
            db.Pdf.deleteOne(
                {
                    "_id": ObjectId(pdfId)
                }
            )
        db.Content.deleteOne(
            {
                "_id" : ObjectId(content._id)
            }
        )
        httpCode = 204
        return 'Content Deleted', httpCode
    if request.method == 'PATCH':
        patchData = request.json
        patchFiles = request.files
        for videoData in patchData.get('videos'):
            jsonSet = {}
            if videoData.dis != None:
                jsonSet.dis = videoData.dis
            if videoData.url != None:
                jsonSet.url = videoData.url   
            elif patchFiles.get(videoData._id) != None:
                videoFile = patchFiles.get(videoData._id)
                jsonSet.url = path.join(app.config["VIDEO_PATH"], '{0}.{1}'.format({videoData._id}, videoFile.filename.split('.')[-1]))
                videoFile.save(jsonSet.url)
            if videoData.videoID == True:
                db.Video.update(
                    { '_id': videoData.videoId },
                    { '$set':
                        jsonSet
                    }
                )
            else:
                createdVideo = db.Video.insert(
                    jsonSet
                )
                content.videoIds.append(createdVideo._id)

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
                content.pdfIds.append(createdPdf._id)
        httpCode = 204
    group = db.Group.find({"_id": ObjectId(groupId)})
    content = db.Content.find({"_id": ObjectId(contentId)})
    videos = [db.Video.find({"_id": ObjectId(videoId)}) for videoId in content.videoIds]
    pdfs = [db.Pdf.find({"_id": ObjectId(pdfId)}) for pdfId in content.pdfIds]
    data = {
        "name": group.id,
        "dis": group.id,
        "contentId": group.ownerId,
        "videos": [
            {
                str(index): {
                    'videoId' : video._id,
                    'url' : video.url,
                    'dis' : video.dis
                }
            }
            for index, video in enumerate(videos)
        ],
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
def contentCreate(groupId):
    postData = request.json
    postFiles = request.files
    content = db.Content.insert_one(
        {
            'name' : postData.get('name'),
            'dis' : postData.get('dis'),
            'videos' : [],
            'pdfs' : [],
        }
    )
    for videoData in postData.get('videos'):
        jsonSet = {}
        if videoData.dis != None:
            jsonSet.dis = videoData.dis
        if videoData.url != None:
            jsonSet.url = videoData.url   
        elif postFiles.get(videoData.tempFileId) != None:
            videoFile = postFiles.get(videoData.tempFileId)
            jsonSet.url = path.join(app.config["PDF_PATH"], '{0}.{1}'.format({videoData._id}, videoFile.filename.split('.')[-1]))
            videoFile.save(jsonSet.url)
        else:
            createdVideo = db.Video.insert(
                jsonSet
            )
            content.videoIds.append(createdVideo._id)

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
            content.pdfIds.append(createdPdf._id)
    group = db.Group.find({"_id": ObjectId(groupId)})
    group.contentIds.append(content._id)
    return "", 200

@groupBlueprint.route("/<contentId>/pdfs/<pdfId>", methods=["DELETE"])
@jwt_required
def pdfRemove(groupId, contentId, pdfId):
    content = db.Content.find({"_id": ObjectId(contentId)})
    content.pdfIds.remove(pdfId)
    db.Pdf.deleteOne(
            {
                "_id": ObjectId(pdfId)
            }
        )
    return 'Content Deleted', 204

@groupBlueprint.route("/<contentId>/videos/<videoId>", methods=["DELETE"])
@jwt_required
def pdfRemove(groupId, contentId, videoId):
    content = db.Content.find({"_id": ObjectId(contentId)})
    content.videoIds.remove(videoId)
    db.Video.deleteOne(
            {
                "_id": ObjectId(videoId)
            }
        )
    return 'Content Deleted', 204