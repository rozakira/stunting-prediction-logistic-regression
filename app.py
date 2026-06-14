<<<<<<< HEAD

=======
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
import pickle

# Membaca dataset
dataset_path = r'C:\Users\use\Documents\PROJECT UAS MACHINE LEARNING\Data_Mentah_Stunting_Prediction.csv'
df = pd.read_csv(dataset_path)

# Melakukan preprocessing pada data
X = df[['Gender', 'Age', 'Birth Weight', 'Birth Length', 'Body Weight', 'Body Length', 'Breastfeeding']]
y = df['Stunting']

# Menyandikan kategori menjadi angka
label_encoder = LabelEncoder()
X['Gender'] = label_encoder.fit_transform(X['Gender'])
X['Breastfeeding'] = X['Breastfeeding'].map({'Yes': 1, 'No': 0})

# Mengatur nilai NaN (jika ada)
X.fillna(X.mean(), inplace=True)
y = y.map({'Yes': 1, 'No': 0})

# Menyusun model
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Membagi data menjadi data pelatihan dan pengujian
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Membangun model Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Menyimpan model ke file pickle
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
    
with open('scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)

# Inisialisasi Flask
app = Flask(__name__)

# Fungsi untuk memuat model dan scaler
def load_model():
    global model, scaler
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)

# Fungsi untuk memprediksi
def make_prediction(features):
    features_scaled = scaler.transform([features])  # Normalisasi fitur input
    prediction = model.predict(features_scaled)
    return prediction[0]

# Route untuk halaman utama (form input)
@app.route('/')
def home():
    return render_template('index.html')

# Route untuk halaman form input data
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Mengambil input dari form
        gender = request.form['gender']
        age = request.form['age'].replace(',', '.')  # Mengganti koma dengan titik
        birth_weight = request.form['birth_weight'].replace(',', '.')  # Mengganti koma dengan titik
        birth_length = request.form['birth_length'].replace(',', '.')  # Mengganti koma dengan titik
        body_weight = request.form['body_weight'].replace(',', '.')  # Mengganti koma dengan titik
        body_length = request.form['body_length'].replace(',', '.')  # Mengganti koma dengan titik
        breastfeeding = request.form['breastfeeding']

        # Mengonversi input ke tipe data yang sesuai
        try:
            age = float(age)
            birth_weight = float(birth_weight)
            birth_length = float(birth_length)
            body_weight = float(body_weight)
            body_length = float(body_length)
        except ValueError:
            return render_template('form.html', error="Input salah. Pastikan angka menggunakan titik sebagai pemisah desimal.")

        # Menyusun data fitur sesuai urutan yang dibutuhkan oleh model
        gender_map = {'Male': 1, 'Female': 0}
        breastfeeding_map = {'Yes': 1, 'No': 0}

        features = [
            gender_map[gender],
            age,
            birth_weight,
            birth_length,
            body_weight,
            body_length,
            breastfeeding_map[breastfeeding]
        ]

        # Menggunakan model untuk memprediksi
        prediction = make_prediction(features)

        # Mengonversi hasil prediksi ke dalam format yang lebih mudah dipahami
        result = "Stunting" if prediction == 1 else "Not Stunting"

        return render_template('result.html', prediction=result)

    return render_template('form.html')

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    try:
        load_model()  # Memuat model saat aplikasi dimulai
    except FileNotFoundError:
        print("Model file tidak ditemukan. Membuat model baru.")
        pass
    
    app.run(debug=True)
>>>>>>> 194a7ee (add stunting ML project)
