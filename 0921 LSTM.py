#suhyeon minhash lstm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import joblib
from datasketch import MinHash
from keras.models import Sequential
from keras.layers import Dense,LSTM,BatchNormalization
import tensorflow as tf
import numpy as np
from sklearn.metrics import r2_score


class ForensicsDataPreprocessing:
    @staticmethod # 이거없으면 민해시오류남
    def calculate_minhash(value):
        """MinHash 계산 함수"""
        if pd.isna(value):
            value = ""
        m = MinHash(num_perm=128)
        for char in str(value):
            m.update(char.encode('utf8'))
        return int.from_bytes(m.digest()[:1], byteorder='little') #8바이트로 제한

    def preprocess_data(self, filepath):
        """학습용 데이터 전처리"""
        df = pd.read_csv(filepath).transpose().reset_index()
        df.columns = df.iloc[0]
        df = df.drop(0).reset_index(drop=True).rename(columns={'name': 'feature'})
        df_melted = df.melt(id_vars='feature', var_name='name', value_name='value')
        # 위변조 라벨 부착
        df_melted['label'] = df_melted['name'].apply(lambda x: 1 if 'mfile' in x else 0)
        df_melted['sequence'] = df_melted.groupby('name').cumcount()
        # 민해시로 변경
        df_melted['minhash'] = df_melted['value'].apply(self.calculate_minhash)
        return df_melted


class ForgeryDetectorEngine:
    def train_model(self, df):
        """훈련"""
        print(df.columns)
        X = df.values[:, -2:]  # sequence minhash
        y = df.values[:, 3]  # label
        X = X.astype(dtype="int64"   )
        y = y.astype(dtype="int64")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        #print(X.shape[0])
        #print('-------x reshape-----------')
        X = X.reshape((X.shape[0], X.shape[1], 1))  # (4,3,1) reshape 전체 곱 수 같아야 4*3=4*3*1
        print('x shape : ', X.shape)
        print(X)

        # 2. 모델 구성
        lstm_model = tf.keras.Sequential()
        lstm_model.add(LSTM(256, input_shape=(2, 1)))
        # DENSE와 사용법 동일하나 input_shape=(열, 몇개씩잘라작업)
        lstm_model.add(Dense(128))
        lstm_model.add(Dense (1,activation='sigmoid'))

        lstm_model.summary()

        # 3. 실행
        lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        lstm_model.fit(X_train, y_train)

        # 성능
        y_pred = lstm_model.predict(X_test)
        y_pred = y_pred.astype(dtype="int64"   )
        accuracy = accuracy_score(y_test, y_pred)
        accuracy = accuracy.astype(dtype="float32"   )
        print("Model accuracy:", accuracy)

        return lstm_model

    def save_model(self, filename):
        """모델 저장"""
        joblib.dump(lstm_model, filename)

    def load_model(self, filename):
        """학습 모델 로드"""
        lstm_model = joblib.load(filename)

    def predict_data(self, df):
        """새 데이터 예측"""
        X_new = df.values[:, -2:]  # sequence value_mhash
        X_new = X_new.astype(dtype="int64"  )
        y_pred_new = lstm_model.predict(X_new)
        print("y_pred_new", y_pred_new)
        df['predicted_label'] = y_pred_new
        return df

    def analyze_prediction(self, df):
        """위변조 판단"""
        y_pred_mean = df['predicted_label'].mean()
        print("y_pred_mean", y_pred_mean)
        for y_pred_new in df['predicted_label'].items():
            if avg < y_pred_mean:
                df['predicted_label'] = 1
            else:
                df['predicted_label'] = 0

        group_averages = df.groupby('name')['predicted_label'].mean()
        results = {}

        threshold = df['predicted_label'].mean()
        print("threshold",threshold)
        for name, avg in group_averages.items():
            if avg < threshold:
                results[name] = '정상 가능성 높음'
            else:
                results[name] = '위변조 가능성 높음'

        return results
if __name__ == "__main__":
    data_preprocessor = ForensicsDataPreprocessing()
    detector_engine = ForgeryDetectorEngine()

    df_melted = data_preprocessor.preprocess_data('123_pe(mp4원본+위조).csv')
    print("전처리한 값:")
    print(df_melted)

    lstm_model = detector_engine.train_model(df_melted)
    detector_engine.save_model('lstm_model.pkl')

    df_test_melted = data_preprocessor.preprocess_data('123_test.csv')
    detector_engine.load_model('lstm_model.pkl')
    predicted_data = detector_engine.predict_data(df_test_melted)

    print(predicted_data[['name', 'predicted_label']].head())
    print(predicted_data)

    results = detector_engine.analyze_prediction(predicted_data)
    for name, result in results.items():
        print(f"The file {name}  {result}.")