from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from bson.json_util import dumps
from bson.objectid import ObjectId
from hydra import db
import stripe
import os

groups = Blueprint("groups", __name__)


@groups.route("/", methods=["GET"])
def allGroups():
    """Show all groups to users, enable search on client."""
    groups = db.Group.find({})
    groupData = []
    for group in groups:
        groupData.append(
            {
                "_id": str(group["_id"]),
                "name": group["name"],
                "dis": group["dis"],
                "ownerId": group["ownerId"],
                "contentIds": group["contentIds"],
                "stripePriceId": group["stripePriceId"],
                "keywords": group["keywords"],
            }
        )
    return dumps(groupData), 200


@groups.route("/yourgroups", methods=["GET"])
@login_required
def UserSections():
    """Show all groups to current user's enrolled groups."""
    groups = []
    for groups in current_user.enrolledGroups:
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
            "assignmentIds": [
                {str(index): assignmentId}
                for index, assignmentId in enumerate(group.assignmentIds)
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


# TODO: roles required for certain access


@groups.route("/create", methods=["POST"])
# @login_required
def groupCreate():
    """Create new group."""
    postData = request.json

    priceStripeObject = stripe.Price.create(
        unit_amount=postData["price"],
        currency="usd",
        recurring={"interval": "month"},
        product="prod_IAvvfq4TnCuNDG",
    )
    db.Group.insert_one(
        {
            "ownerId": postData["ownerId"],
            "enrolledIds": [],
            "contentIds": [],
            "assignmentIds": [],
            "dis": postData["dis"],
            "channelsIds": [],
            "keywords": postData["keywords"],
            "name": postData["name"],
            "stripePriceId": priceStripeObject.get("id"),
            "userIoc": [],
        }
    )
    return jsonify({"msg": "Your group has been created"}), 200


@groups.route("/search", methods=["GET"])
@login_required
def groupSearch():
    """Search for groups to join (user)."""
    params = request.args.get("params")
    groups = list()
    for word in params:
        groups.append(db.Group.find_one_or_404({"$text": {"$search": word}}))
    groups
    print(groups)
    data = [
        {
            "name": group["_id"],
            "groupId": group["_id"],
        }
        for group in groups
    ]
    return dumps(data), 200


@groups.route("/<groupId>", methods=["GET"])
@login_required
def groupId(groupId):
    """Access group details based on groupId"""
    group = db.Group.find({"_id": ObjectId(groupId)})
    if group is None:
        return "Group Not Found", 404
    priceStripeObject = stripe.Price.retrieve(
        group["stripePriceId"],
    )
    data = {
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
        "price": priceStripeObject.get("id"),
    }
    return dumps(data), 200


# TODO: more testing on these routes with frontend


@groups.route("/<groupId>/join", methods=["POST"])
@login_required
def groupIdJoin(groupId):
    """
    User can join group.

    Add group id to user's enrolledGroups and create
    stripe subscription object.
    """
    if (
        groupId in current_user.enrolledGroups
        or groupId in current_user.ownedGroups
    ):
        return jsonify({"msg": "Already Enrolled"}), 200
    postData = request.json
    group = db.Group.find({"_id": ObjectId(groupId)})
    if group is None:
        return jsonify({"msg": "Group Not Found"}), 404
    priceSubscriptionObject = stripe.Subscription.create(
        customer=current_user.stripeId,
        items=[
            {"price": group["stripePriceId"]},
        ],
        defaultPaymentMethod=postData.paymentMethodId,
    )
    if priceSubscriptionObject.get("status") == "active":
        group.enrolledId.append(current_user.id)
        current_user.enrolledGroups.append(group["_id"])
        return jsonify({"msg": "Group Joined"}), 200
    return jsonify({"msg": "Error"}), 200


@groups.route("/<groupId>/leave", methods=["POST"])
@login_required
def groupIdLeave(groupId):
    """Remove user from group."""
    if (
        groupId not in current_user.enrolledGroups
        or groupId not in current_user.ownedGroups
    ):
        return jsonify({"msg": "Not Enrolled"}), 200
    group = db.Group.find({"_id": ObjectId(groupId)})
    if group is None:
        return jsonify({"msg": "Group Not Found"}), 404
    UserSectionData = {}
    for group in current_user.enrolledGroups:
        if group.get(groupId) == group["_id"]:
            UserSectionData = group
    priceSubscriptionObject = stripe.Subscription.delete(
        UserSectionData.get("stripeSubscriptionId")
    )
    if priceSubscriptionObject.get("status") == "canceled":
        group.enrolledId.remove(current_user.id)
        current_user.enrolledGroups.remove(group["_id"])
        return jsonify({"msg": "Group Left"}), 200
    return jsonify({"msg": "Error"}), 200
