"""Dependency and package imports."""
from flask import Blueprint, jsonify, request
from hydra import db, app
from os import path
from hydra.contents.utils import createContent, patchContent
from bson.json_util import dumps
from bson.objectid import ObjectId

contents = Blueprint("contents", __name__)

# base path /groups/<groupId>/contents


@contents.route("/", methods=["GET"])
def contentAll(groupId):
    """Show contents for group id. Return as data to front end."""
    group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
    print(f"Group: {group}")
    contents = [
        db.Content.find_one_or_404({"_id": ObjectId(group["contentId"])})
        for contentId in group["contentIds"]
    ]
    print(f"Contents: {contents}")
    data = [
        {
            "contentId": content["_id"],
            "name": content["name"],
            "dis": content["dis"],
        }
        for content in contents
    ]
    print(f"Data: {data}")
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
        if patchData.get("videos"):
            videoPath = app.config("VIDEO_PATH")
            patchContent("video", patchData, patchFiles, path)
        if patchData.get("pdfs"):
            pdfPath = app.config("PDF_PATH")
            patchContent("pdf", patchData, patchFiles, path)
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
    try:
        postData = request.json
        postFiles = request.files
        content = db.Content.insert_one(
            {
                "name": postData.get("name"),
                "dis": postData.get("dis"),
                "videoIds": [],
                "pdfIds": [],
            }
        )
        if postData.get("videos"):
            videoPath = app.config["VIDEO_PATH"]
            createContent("video", groupId, postData, postFiles, videoPath)
        if postData.get("pdfs"):
            pdfPath = app.config["PDF_PATH"]
            createContent("pdf", groupId, postData, postFiles, pdfPath)
        else:
            createdContent = db.Content.find_one_or_404(
                {"name": postData.get("name")}
            )
            group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
            group["contentIds"].append(createdContent["_id"])
            return dumps(postData)
    except:
        return jsonify({"msg": "Unable to upload files"}), 200


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
