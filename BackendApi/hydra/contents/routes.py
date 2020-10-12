from flask import Blueprint, jsonify, request
from hydra import db, app
from os import path
from bson.json_util import dumps
from bson.objectid import ObjectId

contents = Blueprint("contents", __name__)

# base path /groups/<groupId>/contents


@contents.route("/", methods=["GET"])
def contentAll(groupId):
    """Show contents for group id. Return as data to front end."""
    group = db.Group.find({"_id": ObjectId(groupId)})
    contents = [
        db.Content.find_one_or_404({"_id": ObjectId(group["contentId"])})
        for contentId in group["contentIds"]
    ]
    data = [
        {
            "contentId": content["_id"],
            "name": content["name"],
            "dis": content["dis"],
        }
        for content in contents
    ]
    return dumps(data), 200


@contents.route("/<contentId>", methods=["GET", "PATCH", "DELETE"])
def contentId(groupId, contentId):
    """
    Access content by id.

    Allow for deletion, updating, and adding new content.
    For each different method, return JSON data
    corresponding to action taken.
    """
    httpCode = 200
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    if group is None:
        return jsonify({"msg": "Group Not Found"}), 404
    content = db.Content.find_one_or_404({"_id": ObjectId(contentId)})
    if content is None:
        return jsonify({"msg": "Content Not Found"}), 404
    if request.method == "DELETE":
        for videoId in content["videoIds"]:
            db.Video.deleteOne({"_id": ObjectId(videoId)})
        for pdfId in content["pdfIds"]:
            db.Pdf.deleteOne({"_id": ObjectId(pdfId)})
        db.Content.deleteOne({"_id": ObjectId(content["_id"])})
        httpCode = 204
        return jsonify({"msg": "Content Deleted"}), httpCode
    if request.method == "PATCH":
        patchData = request.json
        patchFiles = request.files
        for videoData in patchData.get("videos"):
            jsonSet = {}
            if videoData["dis"] is not None:
                jsonSet["dis"] = videoData["dis"]
            if videoData["url"] is not None:
                jsonSet["url"] = videoData["url"]
            elif patchFiles.get(videoData["_id"]) is not None:
                videoFile = patchFiles.get(videoData["_id"])
                jsonSet["url"] = path.join(
                    app.config["VIDEO_PATH"],
                    "{0}.{1}".format(
                        {videoData["_id"]}, videoFile.filename.split(".")[-1]
                    ),
                )
                videoFile.save(jsonSet["url"])
            if videoData["videoId"]:
                db.Video.update(
                    {"_id": videoData["videoId"]}, {"$set": jsonSet}
                )
            else:
                createdVideo = db.Video.insert(jsonSet)
                content.videoIds.append(createdVideo["_id"])

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
                pdfFile.save(jsonSet.url)
            if pdfData["pdfId"] is True:
                db.Pdf.update({"_id": pdfData["pdfId"]}, {"$set": jsonSet})
            else:
                createdPdf = db.Pdf.insert(jsonSet)
                content.pdfIds.append(createdPdf["_id"])
        httpCode = 204
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    content = db.Content.find_one_or_404({"_id": ObjectId(contentId)})
    videos = [
        db.Video.find_one_or_404({"_id": ObjectId(videoId)})
        for videoId in content["videoIds"]
    ]
    pdfs = [
        db.Pdf.find_one_or_404({"_id": ObjectId(pdfId)})
        for pdfId in content["pdfIds"]
    ]
    data = {
        "name": group["_id"],
        "dis": group["_id"],
        "contentId": group["ownerId"],
        "videos": [
            {
                str(index): {
                    "videoId": video["_id"],
                    "url": video["url"],
                    "dis": video["dis"],
                }
            }
            for index, video in enumerate(videos)
        ],
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


@contents.route("/create", methods=["POST"])
def contentCreate(groupId):
    """
    Create content and store video or pdf url.

    Return success message for front end.
    """
    postData = request.json
    postFiles = request.files
    content = db.Content.insert_one(
        {
            "name": postData.get("name"),
            "dis": postData.get("dis"),
            "videos": [],
            "pdfs": [],
        }
    )
    for videoData in postData.get("videos"):
        jsonSet = {}
        if videoData["dis"] is not None:
            jsonSet["dis"] = videoData["dis"]
        if videoData["url"] is not None:
            jsonSet["url"] = videoData["url"]
        elif postFiles.get(videoData["tempFileId"]) is not None:
            videoFile = postFiles.get(videoData["tempFileId"])
            jsonSet["url"] = path.join(
                app.config["PDF_PATH"],
                "{0}.{1}".format(
                    {videoData["_id"]}, videoFile.filename.split(".")[-1]
                ),
            )
            videoFile.save(jsonSet["url"])
        else:
            createdVideo = db.Video.insert(jsonSet)
            content.videoIds.append(createdVideo["_id"])

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
            content.pdfIds.append(createdPdf["_id"])
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    group.contentIds.append(content["_id"])
    return (
        jsonify({"msg": "Your files have been added!"}),
        200,
    )  # TODO: What do we want to return here?


# TODO: Don't we allow for the deletion of these in the <contentId> route??

# @contents.route("/pdfs/<pdfId>", methods=["DELETE"])
# def pdfRemove(groupId, contentId, pdfId):
#     content = db.Content.find({"_id": ObjectId(contentId)})
#     content.pdfIds.remove(pdfId)
#     db.Pdf.deleteOne({"_id": ObjectId(pdfId)})
#     return "Content Deleted", 204
#
#
# @contents.route("/<contentId>/videos/<videoId>", methods=["DELETE"])
# def pdfRemove(groupId, contentId, videoId):
#     content = db.Content.find({"_id": ObjectId(contentId)})
#     content.videoIds.remove(videoId)
#     db.Video.deleteOne({"_id": ObjectId(videoId)})
#     return "Content Deleted", 204
