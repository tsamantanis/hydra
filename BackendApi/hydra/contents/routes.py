"""Dependency and package imports."""
from flask import Blueprint, jsonify, request
from hydra import db, app
from os import path
from hydra.contents.utils import (
    createContent,
    patchContent,
)
from bson.json_util import dumps
from bson.objectid import ObjectId

contents = Blueprint("contents", __name__)

# base path /groups/<groupId>/channels/<channelId>/contents


@contents.route("", methods=["GET"])
def contentAll(groupId, channelId):
    """Show contents for group id. Return as data to front end."""
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    contents = db.Contents.find({"channelId": channelId})
    print(contents)
    if group is None or contents is None:
        return jsonify({"msg": "Invalid id provided, please try again."})
    print(f"Contents: {contents}")
    data = [
        {
            "contentId": content["_id"],
            "channelId": content["channelId"],
            "name": content["name"],
            "dis": content["dis"],
        }
        for content in contents
    ]
    print(f"Data: {data}")
    return dumps(data), 200


@contents.route("/<contentId>", methods=["GET", "PATCH", "DELETE"])
def contentId(groupId, channelId, contentId):
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
        if patchData.get("pdfs"):
            pdf = patchData.get("pdfs")
            path = app.config["PDF_PATH"]
            patchContent(pdf, patchData, patchFiles, path)
        elif patchData.get("videos"):
            video = patchData.get("videos")
            path = app.config["VIDEO_PATH"]
            patchContent(video, patchData, patchFiles, path)
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
        "name": content["name"],
        "dis": content["dis"],
        "contentId": content["_id"],
        "channelId": content["channelId"],
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
    return dumps(data), 200


@contents.route("/create", methods=["POST"])
def contentCreate(groupId, channelId):
    """
    Create content and store video or pdf url.

    Return success message for front end.
    """
    try:
        print(request.headers.get("Authorization"))
        postData = request.json
        postFiles = request.files

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
                "videoIds": [],
                "pdfIds": [],
                "channelId": insertedChannel.inserted_id,
            }
        )
        print(f"Inserted content: {content}")
        if postData.get("videos"):
            video = postData.get("videos")
            videoPath = app.config["VIDEO_PATH"]
            for contentData in postData.get("videos"):
                createContent(video, groupId, postData, postFiles, videoPath)
        if postData.get("pdfs"):
            pdf = postData.get("pdfs")
            pdfPath = app.config["PDF_PATH"]
            createContent(pdf, groupId, postData, postFiles, pdfPath)
        else:
            createdContent = db.Content.find_one_or_404(
                {"name": postData.get("name")}
            )
            group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
            group["contentIds"].append(createdContent["_id"])
            return dumps(postData)
    except Exception as e:
        print(e)
        return jsonify({"msg": "Unable to upload files"}), 200


@contents.route("/<contentId>/pdfs/<pdfId>", methods=["DELETE", "PATCH"])
def pdfId(groupId, contentId, pdfId):
    if request.method == "DELETE":
        db.Pdf.deleteOne({"_id": ObjectId(pdfId)})
        return "Assignment Deleted", 204
    if request.method == "PATCH":
        jsonSet = {}
        pdf = db.Pdf.find({"_id": ObjectId(pdfId)})
        if request.json.get("tempFileId") is not None:
            contentFile = request.files.get(request.json.get("tempFileId"))
            jsonSet["url"] = path.join(
                app.config["PDF_PATH"],
                "{0}.{1}".format(
                    {pdf["_id"]},
                    contentFile.filename.split(".")[-1],
                ),
            )
            contentFile.save(jsonSet["url"])
        elif request.json.get("url") is not None:
            jsonSet["url"] = request.json.get("url")
        if request.json.get("dis") is not None:
            jsonSet["dis"] = request.json.get("dis")
        db.Pdf.update_one({"_id": ObjectId(pdfId)}, {"$set": jsonSet})
    return "Patch Made", 200
    if request.method == "GET":
        return send_from_directory(
            app.config["PDF_PATH"], "{0}.pdf".format(pdfId)
        )


@contents.route("/<contentId>/videos/<videoId>", methods=["DELETE", "PATCH"])
# @jwt_required
def videoId(groupId, contentId, videoId):
    if request.method == "DELETE":
        db.Video.deleteOne({"_id": ObjectId(videoId)})
        return "Video Deleted", 204
    if request.method == "PATCH":
        jsonSet = {}
        video = db.Video.find({"_id": ObjectId(videoId)})
        if request.json.get("tempFileId") is not None:
            contentFile = request.files.get(request.json.get("tempFileId"))
            jsonSet["url"] = path.join(
                app.config["VIDEO_PATH"],
                "{0}.{1}".format(
                    {video["_id"]},
                    contentFile.filename.split(".")[-1],
                ),
            )
            contentFile.save(jsonSet["url"])
        elif request.json.get("url") is not None:
            jsonSet["url"] = request.json.get("url")
        if request.json.get("dis") is not None:
            jsonSet["dis"] = request.json.get("dis")
        db.Video.update({"_id": ObjectId(videoId)}, {"$set": jsonSet})
    return "Patch Made", 200
    if request.method == "GET":
        return send_from_directory(
            app.config["VIDEO_PATH"], "{0}.mp4".format(videoId)
        )


# TODO: Test more when file upload is supported on the front end


@contents.route("/<contentId>/videos/add", methods=["POST"])
def videoAdd(groupId, contentId):
    """Add singular video to channel content."""
    jsonSet = {}
    content = db.Content.find_one_or_404({"_id": ObjectId(contentId)})
    postFiles = request.files
    if request.json.get("dis") is not None:
        jsonSet["dis"] = request.json.get("dis")
    video = db.Video.insert_one(jsonSet)
    content["videos"].append(video.inserted_id)
    if request.json.get("url") is not None:
        jsonSet["url"] = request.json.get("url")
    elif postFiles.get(request.json.get("tempFileId")) is not None:
        contentFile = postFiles.get(request.json.get("tempFileId"))
        jsonSet["url"] = path.join(
            app.config["VIDEO_PATH"],
            "{0}.{1}".format(
                {video["_id"]},
                contentFile.filename.split(".")[-1],
            ),
        )
        contentFile.save(jsonSet["url"])
    db.Video.update({"_id": ObjectId(video["_id"])}, {"$set": jsonSet})
    return jsonify({"msg": "Your video has been added!"}), 200


@contents.route("/<contentId>/pdfs/add", methods=["POST"])
def pdfAdd(groupId, contentId):
    """Add single pdf document to channel content."""
    jsonSet = {}
    content = db.Content.find_one_or_404({"_id": ObjectId(contentId)})
    postFiles = request.files
    if request.json.get("dis") is not None:
        jsonSet["dis"] = request.json.get("dis")
    pdf = db.Pdf.insert_one(jsonSet)
    content["pdfs"].append(pdf.inserted_id)
    if request.json.get("url") is not None:
        jsonSet["url"] = request.json.get("url")
    elif postFiles.get(request.json.get("tempFileId")) is not None:
        contentFile = postFiles.get(request.json.get("tempFileId"))
        jsonSet["url"] = path.join(
            app.config["VIDEO_PATH"],
            "{0}.{1}".format(
                {pdf["_id"]},
                contentFile.filename.split(".")[-1],
            ),
        )
        contentFile.save(jsonSet["url"])
    db.Pdf.update({"_id": ObjectId(pdf["_id"])}, {"$set": jsonSet})
    return jsonify({"msg": "Your document has been added!"}), 200
