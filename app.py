from flask import Flask, jsonify, request  
from flask_jwt_extended import JWTManager, create_access_token, jwt_required  
from flask_cors import CORS  
import datetime  
import json

with open("./serversettings.json", 'r') as file:
    deviceData = json.load(file)

crt_path= deviceData.get('certificate_crt_path')
key_path= deviceData.get('certificate_key_path')
command_file = deviceData.get('command_file')
report_file= deviceData.get('report_file')

app = Flask(__name__)  
CORS(app)  

# API_KEY ve token süresinin ayarlanması  
API_KEY = deviceData.get('API_KEY')  # API_KEY token almak için kullanılacak, belli aralıklarda değiştirilmeli
token_duration= deviceData.get('jwt_token_duration')
app.config['JWT_SECRET_KEY'] =  deviceData.get('JWT_SECRET_KEY') # Token'lar için gizli anahtar  

jwt = JWTManager(app)  

# Token alma  
@app.route('/token', methods=['POST'])  
def get_token():  
    api_key = request.json.get('api_key', None)  
    
    if api_key != API_KEY:  
        return jsonify({"msg": "API_KEY is invalid!"}), 401  
    
    # Token oluşturuluyor  
    access_token = create_access_token(identity= api_key, expires_delta=datetime.timedelta(hours=token_duration))  
    return jsonify(access_token=access_token)  

# Örnek API  
@app.route('/secure-data', methods=['GET'])  
@jwt_required()  
def secure_data():  
    return jsonify({"msg": "Bu veriye sadece yetkili kullanıcı erişebilir."})  

# Client'a işlem isteklerini göndermek için 
@app.route('/command-requests', methods=['GET'])  
@jwt_required()  
def requests():
    # client'dan işlenmesi istenecek komutu dosyadan oku  
    # Gelen parametrelere göre bir yanıt oluştur  
    response_data = read_command_from_file(command_file) 

    return jsonify(response_data) 

# Yeni endpoint: JSON verisini kaydetme  
@app.route('/save-data', methods=['POST'])  
@jwt_required()  
def save_data():  
    data = request.json  # Gönderilen JSON verisini al  
    if data is None:  
        return jsonify({"msg": "No data provided!"}), 400  

    try:  
        with open(report_file, 'a', encoding='utf-8') as f:  # UTF-8 ile açıyoruz  
            json.dump(data, f, ensure_ascii=False)  # Türkçe karakterleri doğru kaydet  
            f.write('\n')  # Her kayıttan sonra yeni bir satır ekliyoruz  
    except Exception as e:  
        return jsonify({"msg": "Error saving data!", "error": str(e)}), 500  

    return jsonify({"msg": "Data saved successfully!"}), 200 


def read_command_from_file(filename):  
    data_clear = {}  
    data_clear['command'] = ''  # Boş bir komut oluştur   

    try:  
        with open(filename, 'r') as file:  
            data = json.load(file)  

        if not data:
            data= data_clear  

        # Güncellenmiş veriyi dosyaya yaz  
        with open(filename, 'w') as file:  
            json.dump(data_clear, file, indent=4)  # Command boşaltılmış halini dosyaya yaz
        
        return data

    except FileNotFoundError:  
        print(f"Dosya '{filename}' bulunamadı.")  
        return data_clear  
    except json.JSONDecodeError:  
        print(f"Dosya '{filename}' bir JSON dosyası değil ya da bozulmuş durumda.")  
        return data_clear  



if __name__ == '__main__':  
    # SSL sertifikalarınızın dosya yollarını belirtin  
    app.run(debug=True, host='0.0.0.0', port=5001, ssl_context=(crt_path, key_path))