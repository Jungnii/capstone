from flask import Flask,jsonify,request
from util.mainForChatbot import mainForChatbot as mainForChatbot
application = Flask(__name__)

@application.route("/barcode", methods=["POST"])
def barcode():
    json_data = request.get_json()
    json_barcode = json_data['action']['params']['barcode']
    dict = eval(json_barcode)
    global barcodeNum
    barcodeNum = dict.get('barcodeData')
    message = f"바코드 번호 : {barcodeNum}\n바코드 인식 완료!🙂\n\n이제 유통기한 사진이 필요합니다. \"유통기한\"을 채팅창에 입력해주세요."

    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": message
                    }
                }
            ]
        }
    }
    return jsonify(response)

@application.route("/image", methods=["POST"])
def image():
    json_data = request.get_json()
    global image_url
    image_url = json_data['userRequest']['params']['media']['url']
    message = f"유통기한 사진 전달 완료!🙂\n\n냉장고를 확인하고 싶으면 채팅창에 \"냉장고\"를 입력하고 그만하고 싶으면 \"그만하기\"를 입력해주세요."

    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": message
                    }
                }
            ]
        }
    }
    return jsonify(response)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=True)