from flask import Flask, request, jsonify, json
from pprint import pprint
import pymysql

application = Flask(__name__)
application.debug = True
# database에 접근
db = pymysql.connect(host='3.35.219.129',
                     port=51308,
                     user='root',
                     password='123456789',
                     db='chatbot',
                     charset='utf8')
 
# database를 사용하기 위한 cursor를 세팅합니다.
cursor = db.cursor()

@application.route("/list", methods=["POST"])
def show_list():
    print("냉장고 둘러보기")
    query = f"DESCRIBE items"
    cursor.execute(query)
    columns = [column[0] for column in cursor.fetchall()]


    # Retrieve and display the data
    query = f"SELECT * FROM items ORDER BY exprt_date ASC"
    cursor.execute(query)
    rows = cursor.fetchall()

    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    body = []
    for row in rows:
        body.append(row)
    print(*body, sep='\n')

    message = f"{body}"

    responseBody = {
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
    return responseBody

@application.route("/direct", methods=["POST"])
def direct_function():
    global food_name, food_qty, food_expiry

    data = request.get_json()
    params = data["action"]["params"]

    food_name = params["food_name"]
    food_qty = params["food_qty"]
    food_expiry = params["food_expiry"]
    expiry_dict = eval(food_expiry)

    expiry_date = expiry_dict.get("value")

    message = f" 식품 이름: {food_name}\n 유통기한: {expiry_date}\n 수량: {food_qty}\n 식품 저장이 완료되었습니다.\n\n 냉장고를 확인하고 싶으면 채팅창에 \"냉장고\"를 입력하고 그만하고 싶으면 \"그만하기\"를 입력해주세요."


#sql = """INSERT INTO items(item_type, item_name, item_code, exprt_date, item_number)
#         VALUES('유형', '이름' ,'코드','유통기한','숫자');"""

    sql = """INSERT INTO items(item_name, item_count, exprt_date)
             values(%s,%s,%s);"""

    record = (food_name, food_qty, expiry_date)

    cursor.execute(sql,record)
    db.commit()
    result = cursor.fetchall()
# Database 닫기
    db.close()

    return jsonify({
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
    })

@application.route("/showlist", methods=["POST"])
def list():
    global show_list
    
    print("냉장고 둘러보기")
    query = f"DESCRIBE items"
    cursor.execute(query)
    columns = [column[0] for column in cursor.fetchall()]


    # Retrieve and display the data
    query = f"SELECT * FROM items"
    cursor.execute(query)
    rows = cursor.fetchall()


    show_list = []
    for row in rows:
        show_list.append(row)
    print(*show_list, sep='\n')
    
    return show_list
    message=show_list

    #for row in rows:
    #    print(row)
    
    # Close the cursor
   
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])


    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "실패"
                    }
                }
            ]
        }
    })


    cursor.close()
    
list()
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=51308, threaded=True)
