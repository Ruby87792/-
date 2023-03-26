# 导入相关库和框架
from flask import Flask, request, jsonify

app = Flask(__name__)

# 定义一个接口用于接收数据
@app.route('/api/receive_data', methods=['POST'])
def receive_data():
    # 从请求中获取数据
    data = request.json
    print(data)  # 打印接收到的 JSON 数据
    # 处理数据并返回响应
    result = {'message': 'Data received successfully!'}
    return jsonify(result)


# 定义一个接口用于发送数据
@app.route('/api/send_data', methods=['GET'])
def send_data():
    # 准备要发送的数据
    data = {'name': 'John Doe', 'age': 30}
    # 发送响应
    return jsonify(data)

if __name__ == '__main__':
    app.run()
