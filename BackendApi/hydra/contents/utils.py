"""Dependency and package imports."""
from flask import request, jsonify
from hydra import db, app
from os import path
from bson.json_util import dumps
from bson.objectid import ObjectId


def createContent(content, groupId, postData, postFiles):
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
                app.config["PDF_PATH"],
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


def patchContent():
    """Update content resource."""
    pass
