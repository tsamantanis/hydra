import flask

groupBlueprint = Blueprint('Groups', __name__)

@hostBlueprint.route('/', methods=['GET'])
@log
def groupsAll():
    groups = db.Group.find({})
    data = [{
        "name": group.id,
        "groupId": group.id,
        "ownerId": group.ownerId,
        "enrolledIds": [{
            str(index) : enrolledId
        } for index, enrolledId in enumerate(group.enrolledIds)],
        "contentIds": [{
            str(index) : contentId
        } for index, contentId in enumerate(group.contentIds)],
        "dis": group.dis,
        "keywords" : [{
            str(index) : keyword
        } for index, keyword in enumerate(group.keywords)]
    } for group in groups]
    return flask.jsonify(data), ''

@hostBlueprint.route('/create', methods=['POST'])
def groupCreate():
    postData = request.form
    
    priceStripeObject = stripe.Price.create(
        unit_amount=postData.price,
        currency="usd",
        recurring={"interval": "month"},
        product="prod_IAvvfq4TnCuNDG",
    )
    db.Group.insert_one({
        ownerId : postData.ownerId,
        enrolledIds : {},
        contentIds : {},
        dis : postData.dis,
        channelsIds : {},
        keywords : postData.keywords,
        name : postData.name,
        stripePriceId : priceStripeObject.get('id'),
        userIoc : {}
    })
    return '', 200

@hostBlueprint.route('/search', methods=['GET'])
def groupSearch():
    getData = request.args
    groups = list()
    for word in getData.parms:
        groups.append(db.Group.find({"$text": {"$search": word}}))
    groups
    data = [{
        "name": group.id,
        "groupId": group.id,
    } for group in groups]
    return flask.jsonify(data), 200

@hostBlueprint.route('/<groupId>', methods=['GET'])
def groupId(groupId):
    group = db.Group.find({'_id' : id(groupId)})
    if group is None:
        return 'Group Not Found', 404
    priceStripeObject = stripe.Price.retrieve(
        group.stripePriceId,
    )
    data = {
        "name": group.id,
        "groupId": group.id,
        "ownerId": group.ownerId,
        "enrolledIds": [{
            str(index) : enrolledId
        } for index, enrolledId in enumerate(group.enrolledIds)],
        "contentIds": [{
            str(index) : contentId
        } for index, contentId in enumerate(group.contentIds)],
        "dis": group.dis,
        "keywords" : [{
            str(index) : keyword
        } for index, keyword in enumerate(group.keywords)],
        "price" : priceStripeObject.get('id')
    }
    return flask.jsonify(data), ''

@hostBlueprint.route('/<groupId>/join', methods=['POST'])
def groupIdJoin(groupId):
    if groupId in currentUser.enrolledGroups or groupId in currentUser.ownedGroups:
        return 'Already Enrolled', 200
    postData = request.form
    group = db.Group.find({'_id' : id(groupId)})
    if group is None:
        return 'Group Not Found', 404
    priceSubscriptionObject = stripe.Subscription.create(
        customer=currentUser.stripeId,
        items=[
            {"price": group.stripePriceId},
        ],
        defaultPaymentMethod=postData.paymentMethodId
    )
    if priceSubscriptionObject.get('status'):
        group.enrolledId.append(currentUser._id)
        return 'Invalid Payment', 200
    return 'Group Joined', 200
