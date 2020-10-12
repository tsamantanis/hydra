"""Dependency and package imports."""
from flask import request, jsonify
from hydra import db, app
from os import path
from bson.json_util import dumps
from bson.objectid import ObjectId


def createContent(content, groupId, postData, postFiles, path):
    """
    Create content.

    Create filepath for storing content,
    return success message to client."""
    for contentData in postData.get(content):
        jsonSet = {}
        if contentData["dis"] is not None:
            jsonSet["dis"] = contentData["dis"]
        if contentData["url"] is not None:
            jsonSet["url"] = contentData["url"]
        elif postFiles.get(contentData["tempFileId"]) is not None:
            contentFile = postFiles.get(contentData["tempFileId"])
            jsonSet["url"] = path.join(
                path,
                "{0}.{1}".format(
                    {contentData["_id"]},
                    contentFile.filename.split(".")[-1],
                ),
            )
            contentFile.save(jsonSet["url"])
        else:
            if "video" in content:
                createdContent = db.Video.insert(jsonSet)
            elif "pdf" in content:
                createdContent = db.Pdf.insert(jsonSet)
            group = db.Group.find_one_or_404({"_id": ObjectId(groupId)})
            group["contentIds"].append(createdContent["_id"])
            return (
                jsonify({"msg": "Your files have been added!"}),
                200,
            )  # TODO: What do we want to return here?


def patchContent(content, patchData, patchFiles, path):
    """Update content resource."""
    for contentData in patchData.get(content):
        jsonSet = {}
        if contentData["dis"] is not None:
            jsonSet["dis"] = contentData["dis"]
        if contentData["url"] is not None:
            jsonSet["url"] = contentData["url"]
        elif patchFiles.get(contentData["_id"]) is not None:
            contentFile = patchFiles.get(contentData["_id"])
            jsonSet["url"] = path.join(
                path,
                "{0}.{1}".format(
                    {contentData["_id"]}, contentFile.filename.split(".")[-1]
                ),
            )
            contentFile.save(jsonSet["url"])
        if "video" in content:
            if contentData["videoId"]:
                db.Video.update(
                    {"_id": contentData["videoId"]}, {"$set": jsonSet}
                )
            else:
                createdVideo = db.Video.insert(jsonSet)
                content.videoIds.append(createdVideo["_id"])
        elif "pdf" in content:
            if contentData["pdfId"]:
                db.Pdf.update(
                    {"_id": contentData["pdfId"]}, {"$set": jsonSet}
                )
            else:
                createdPdf = db.Pdf.insert(jsonSet)
                content.pdfIds.append(createdPdf["_id"])
    return jsonify({"msg": "Your content has been updated"}), 200
