from flask import Flask, make_response, request
from flask import jsonify
from flask_cors import CORS
from example import getRes

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

@app.route('/')
def hello_world():
    print("1")
    return 'Hello World!'

@app.route('/getMsg1', methods=['GET','POST'])
def home1():
    # if not request.data:  # 检测是否有数据
    #     print("fail")
    #     return ('fail')
    # print("req",request)
    # filename = request.values.get("file")
    # print(request.values)
    filename = "testData/test1.pcap"
    response = {
        'msg': getRes(filename)
    }
    return jsonify(response)

@app.route('/getMsg2', methods=['GET','POST'])
def home2():
    # if not request.data:  # 检测是否有数据
    #     print("fail")
    #     return ('fail')
    # print("req",request)
    # filename = request.values.get("file")
    # print(request.values)
    filename = "testData/test2.pcap"
    response = {
        'msg': getRes(filename)
    }
    return jsonify(response)

@app.route('/getMsg3', methods=['GET','POST'])
def home3():
    # if not request.data:  # 检测是否有数据
    #     print("fail")
    #     return ('fail')
    # print("req",request)
    # filename = request.values.get("file")
    # print(request.values)
    filename = "testData/data.pcap"
    response = {
        'msg': getRes(filename)
    }
    return jsonify(response)


# 启动运行
if __name__ == '__main__':
    app.run()   # 这样子会直接运行在本地服务器，也即是 localhost:5000
   # app.run(host='127.0.0.1',debug=True) # 这里可通过 host 指定在公网IP上运行


@app.after_request
def after(resp):
    '''
    被after_request钩子函数装饰过的视图函数
    ，会在请求得到响应后返回给用户前调用，也就是说，这个时候，
    请求已经被app.route装饰的函数响应过了，已经形成了response，这个时
    候我们可以对response进行一些列操作，我们在这个钩子函数中添加headers，所有的url跨域请求都会允许！！！
    '''
    print("?????")
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


