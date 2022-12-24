from flask import Response,jsonify,request
from app.api import api
from app import db
from app.api.models import Users,Posts
from app.api.util import createJWT,verifyJWT,verify_pass,auth_required




@api.route("/login",methods=['POST'])
def login():
    print("Logging In")
    data = request.get_json(force=True)
    try:
        email = data["email"]
        password = data["password"]
        user = Users.query.filter_by(email=email).first_or_404()
        ok = verify_pass(password, user.password)
        if ok:
            token = createJWT({"id":2,"admin":True})
            return jsonify({"access_token":token})
        else:
            return Response(status=401)
    except Exception:
        return Response(status=401)



@api.get("/user")
@auth_required
def getUser():
    print("Request User: ",request.user['id'])
    try:
        user = Users.query.filter_by(id=request.user['id']).first_or_404()
        res = Users.serialize(user)
        posts = Posts.query.filter_by(author_id = request.user['id']).all()
        res["posts"] = [Posts.serialize(post) for post in posts]
        return jsonify(res)
    except Exception:
        return Response(status=404)



@api.post("/register")
def register():
    data = request.get_json(force=True)
    data_keys = data.keys()
    error = ""
    if "name" not in data_keys:
        error = "Name is required"
    elif "email" not in data_keys:
        error = "Email is required"
    elif "password" not in data_keys:
        error = "Password is required"
    
    if error !="":
        return  jsonify({"msg":error})
    else:
        try:
            name = data["name"]
            email = data["email"]
            password = data["password"]
            user = Users.query.filter_by(email=email).first()
            print("User Found: ",user)
            if user is None:
                u = Users(name=name,email=email,password=password).create()
                return jsonify(Users.serialize(u))
            else:
                return jsonify({"msg":"User Already Exists"}),400
            
            
        except Exception:
            return jsonify({"msg":"Invalid request body"}), 400
    
@api.get("/")
@auth_required
def index():
    users = Users.query.all()
    res = [Users.serialize(user) for user in users]
    return jsonify(res)

@api.get("/post/<post_id>")
def getPost(post_id):
    post = Posts.query.filter_by(id=post_id).first_or_404()
    res = Posts.serialize(post)
    return jsonify(res)


@api.post("/post")
@auth_required
def createPost():
    data = request.get_json(force=True)
    data_keys = data.keys()
    error = ""
    if "title" not in data_keys:
        error = "Title is required"
    elif "content" not in data_keys:
        error = "Contentis required"
    
    if error !="":
        return  jsonify({"msg":error})
    else:
        title = data['title']
        content = data['content']
        post = Posts(title, content, request.user['id']).create()
        return jsonify(Posts.serialize(post)),201
    


@api.get("/myposts")
@auth_required
def myPosts():
    posts = Posts.query.filter_by(author_id = request.user['id']).all()
    res = [Posts.serialize(post) for post in posts]
    return jsonify(res)

@api.get("/posts")
def getPosts():
    posts = Posts.query.all()
    res = [Posts.serialize(post) for post in posts]
    return jsonify(res)