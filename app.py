from flask import Flask, jsonify, request, make_response
from flask_swagger_ui import get_swaggerui_blueprint

from random import randint

from classes.rpn import RPN
app = Flask(__name__)
app.debug = True
#swagger configs 

SWAGGER_URL = "/swagger"
API_URL ="/static/swagger.json"
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name":"Stack"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

# {stackId: stack()} 
memory_rpns = { }
idsCreated = []
idsLimit = 100

def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({"msg": "Not found", "success":False}), 404)


def handle_400_error(msg):
    """Return a http 404 error to client"""
    return make_response(jsonify({"msg": msg, "success":False}), 400)

def getUniqueId(id):
    uniqueId =id
    while uniqueId in idsCreated:
        uniqueId = randint(1, idsLimit)
    idsCreated.append(uniqueId)
    return uniqueId

def stackExits(id):
    if(not (id in memory_rpns)):
        return False
    return True


@app.route("/rpn/op")
def getAllOp():
    data = {
            "success" : True,
            "data" : ["+","-","*","/"],
        }
  
    return jsonify(data)



@app.route("/rpn/stack", methods = ["POST", "GET"])
def stack():
    if request.method == "POST":
        return createStack()

    if request.method == "GET":
        return jsonify(getAllStacks(memory_rpns))


@app.route("/rpn/stack/<int:stack_id>", methods = ["DELETE", "POST", "GET"])
def stackDelPostGet(stack_id):
    if(not (stackExits(stack_id))):
        return handle_400_error("stack "+str(stack_id)+" not available")
    if request.method == "DELETE":
        return deleteStack(stack_id)
    if request.method == "POST":
        data = request.get_json()
        return jsonify(pushValueStack(stack_id, data["value"]))
    if request.method == "GET":
        return jsonify({"data":{"stackID":stack_id, "stack":memory_rpns[stack_id].getStack(), "success":True}})
 
    
@app.route("/rpn/op/<op>/stack/<int:stack_id>", methods = [ "POST",])
def calcul(op, stack_id):
    if(not (stackExits(stack_id))):
        return handle_400_error("stack "+str(stack_id)+" not available")
    if(not (op in ["+", "-", "*", "/"])):
        return handle_400_error("Bad operand, only available:+, - , *, /")
    
    memory_rpns[stack_id].calcul(op)
    return jsonify({"data":{"stackId":stack_id, "stack":memory_rpns[stack_id].getStack(), "success":True}})
    

def createStack():

    if(len(idsCreated) == idsLimit):
        return handle_400_error("Limit id reached, delete existing stack")
    id =  getUniqueId(randint(1, idsLimit))
    
    userRpn = RPN()
    
    memory_rpns[id] = userRpn
    data = {
            "success" : True,
            "data" : {"stackId":id, "stack":userRpn.getStack()},
        }

    return jsonify(data)


def getAllStacks(memory_rpns):
    stacksArray = []
    for key in memory_rpns:
        stack = {"stackId":key,"stack":memory_rpns[key].getStack() }
        stacksArray.append(stack)
    

    data = {
        "success" : True,
        "data" : stacksArray,
        }
    return data


def deleteStack(id):
    if request.method == "DELETE":
        del memory_rpns[id]
        return jsonify({"success":True, "data":getAllStacks(memory_rpns)["data"], "infos":"stack "+str(id)+" deleted"}) 
        
          
def pushValueStack(id, value):
        memory_rpns[id].addValueStack(value)
        return  {"stackId":id, "stack":memory_rpns[id].getStack(), "success":True}
    
      

    
