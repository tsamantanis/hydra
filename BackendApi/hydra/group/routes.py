from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from bson.objectid import ObjectId
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_raw_jwt,
)
from hydra import db
import stripe

groups = Blueprint("groups", __name__)

# TODO: This data will need to be serialized more properly to pass to front end.


@groups.route("/", methods=["GET"])
@jwt_required
def groupsAll():
    currentUser = get_jwt_identity()
    groups = db.Group.find({})
    data = [
        {
            "name": group["_id"],
            "groupId": group["_id"],
            "ownerId": group["ownerId"],
            "enrolledIds": [
                {str(index): enrolledId}
                for index, enrolledId in enumerate(group["enrolledIds"])
            ],
            "contentIds": [
                {str(index): contentId}
                for index, contentId in enumerate(group["contentIds"])
            ],
            "dis": group["dis"],
            "keywords": [
                {str(index): keyword}
                for index, keyword in enumerate(group["keywords"])
            ],
        }
        for group in groups
    ]
    return jsonify({"group": [group for group in groups]}), 200


@groups.route("/create", methods=["POST"])
# @jwt_required
def groupCreate():
    postData = request.json

    priceStripeObject = stripe.Price.create(
        unit_amount=postData["price"],
        currency="usd",
        recurring={"interval": "month"},
        product="prod_IAvvfq4TnCuNDG",
    )
    db.Group.insert_one(
        {
            ownerId: postData.ownerId,
            enrolledIds: {},
            contentIds: {},
            dis: postData.dis,
            channelsIds: {},
            keywords: postData.keywords,
            name: postData.name,
            stripePriceId: priceStripeObject.get("id"),
            userIoc: {},
        }
    )
    return "", 200


@groups.route("/search", methods=["GET"])
@jwt_required
def groupSearch():
    getData = request.args
    groups = list()
    for word in getData.parms:
        groups.append(db.Group.find({"$text": {"$search": word}}))
    groups
    data = [
        {
            "name": group.id,
            "groupId": group.id,
        }
        for group in groups
    ]
    return flask.jsonify(data), 200


@groups.route("/<groupId>", methods=["GET"])
@jwt_required
def groupId(groupId):
    group = db.Group.find({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    priceStripeObject = stripe.Price.retrieve(
        group.stripePriceId,
    )
    data = {
        "name": group.id,
        "groupId": group.id,
        "ownerId": group.ownerId,
        "enrolledIds": [
            {str(index): enrolledId}
            for index, enrolledId in enumerate(group.enrolledIds)
        ],
        "contentIds": [
            {str(index): contentId}
            for index, contentId in enumerate(group.contentIds)
        ],
        "dis": group.dis,
        "keywords": [
            {str(index): keyword}
            for index, keyword in enumerate(group.keywords)
        ],
        "price": priceStripeObject.get("id"),
    }
    return flask.jsonify(data), ""


@groups.route("/<groupId>/join", methods=["POST"])
@jwt_required
def groupIdJoin(groupId):
    if (
        groupId in currentUser.enrolledGroups
        or groupId in currentUser.ownedGroups
    ):
        return "Already Enrolled", 200
    postData = request.json
    group = db.Group.find({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    priceSubscriptionObject = stripe.Subscription.create(
        customer=currentUser.stripeId,
        items=[
            {"price": group.stripePriceId},
        ],
        defaultPaymentMethod=postData.paymentMethodId,
    )
    if priceSubscriptionObject.get("status") == "active":
        group.enrolledId.append(currentUser._id)
        current_user.enrolledGroups.append(group._id)
        return "Group Joined", 200
    return "Error", 200


@groups.route("/<groupId>/leave", methods=["POST"])
@jwt_required
def groupIdLeave(groupId):
    if (
        groupId not in currentUser.enrolledGroups
        or groupId not in currentUser.ownedGroups
    ):
        return "Not Already Enrolled", 200
    group = db.Group.find({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    userGroupData = {}
    for group in current_user.enrolledGroups:
        if group.get(groupId) == group._id:
            userGroupData = group
    priceSubscriptionObject = stripe.Subscription.delete(
        userGroupData.get("stripeSubscriptionId")
    )
    if priceSubscriptionObject.get("status") == "canceled":
        group.enrolledId.remove(currentUser._id)
        current_user.enrolledGroups.remove(group._id)
        return "Group Left", 200
    return "Error", 200
