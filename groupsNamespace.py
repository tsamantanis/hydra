import flask

groupBlueprint = Blueprint('Groups', __name__)

@hostBlueprint.route('/', methods=['GET'])
@log
def groupsAll():
    groups = db.Group.find({})
    data = [{
        "name": group.id,
        "group_id": group.id,
        "owner_id": group.owner_id,
        "enrolled_ids": [{
            str(index) : enrolled_id
        } for index, enrolled_id in enumerate(group.enrolled_ids)],
        "content_ids": [{
            str(index) : content_id
        } for index, content_id in enumerate(group.content_ids)],
        "dis": group.dis,
        "keywords" : [{
            str(index) : keyword
        } for index, keyword in enumerate(group.keywords)]
    } for group in groups]
    return flask.jsonify(data), ''

@hostBlueprint.route('/create', methods=['POST'])
def groupCreate():
    postData = request.form
    db.Group.insert_one({
        owner_id : postData.owner_id,
        enrolled_ids : {},
        content_ids : {},
        dis : postData.dis,
        channels_ids : {},
        keywords : postData.keywords,
        name : postData.name,
        price : postData.price,
        user_loc : {}
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
        "group_id": group.id,
    } for group in groups]
    return flask.jsonify(data), 200

@hostBlueprint.route('/<group_id>', methods=['GET'])
def groupSearch(group_id):
    group = db.Group.find({'_id' : id(group_id)})
    data = {
        "name": group.id,
        "group_id": group.id,
        "owner_id": group.owner_id,
        "enrolled_ids": [{
            str(index) : enrolled_id
        } for index, enrolled_id in enumerate(group.enrolled_ids)],
        "content_ids": [{
            str(index) : content_id
        } for index, content_id in enumerate(group.content_ids)],
        "dis": group.dis,
        "keywords" : [{
            str(index) : keyword
        } for index, keyword in enumerate(group.keywords)]
    }
    return flask.jsonify(data), ''

@hostBlueprint.route('/<group_id>/join', methods=['POST'])
def groupSearch(group_id):
    postData = request.form
    group = db.Group.find({'_id' : id(group_id)})
    group.enrolled_id.append()
    
        #TODO how to we wanna get _id
    
    
    return '', 200
