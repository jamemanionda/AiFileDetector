# 설치
# pip install keras-tuner

import pandas as pd
from sklearn.model_selection import train_test_split
from simhash import Simhash
from tensorflow import keras
import numpy as np
from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras.layers import GRU, Dense
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
#from tensorflow.keras import layers
#from kerastuner.tuners import RandomSearch
#from kerastuner.engine.hyperparameters import HyperParameters


class ForensicsDataPreprocessing:
    def preprocess_data(self, filepath, is_train=True):
        """데이터 전처리"""
        df = pd.read_csv(filepath, header=None)
        column_count = df.shape[1]
        original_labels = None

        if is_train:
            features = df.iloc[0, 1:-1].values
            df.columns = ['name'] + list(features) + ['label']
            df = df[1:]


        else:
            features = df.iloc[0, 1:-1].values
            df.columns = ['name'] + list(features) + ['label']
            original_labels = df[['name', 'label']]
            df = df[1:]

        return df, original_labels

    @staticmethod
    def calculate_simhash_lib(value):
        return Simhash(str(value)).value

    def apply_simhash(self, df):
        """Simhash 적용"""
        columns_to_process = [col for col in df.columns if col not in ['name', 'label']]
        for column in columns_to_process:
            df[column] = df[column].apply(self.calculate_simhash_lib).astype('int64')
        return df


class ForgeryDetectorEngine:
    def __init__(self):
        self.xgb_model = None

    def train_model(self, df):
        """훈련"""
        X = df.iloc[:, 1:-1].values
        y = df['label'].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)


        # 변환안하니까 오류나네
        y_train = pd.to_numeric(y_train, errors='coerce').astype(np.int32)
        y_test = pd.to_numeric(y_test, errors='coerce').astype(np.int32)


        # 모델 구성
        self.model = Sequential()
        self.model.add(GRU(50, input_shape=(X_train.shape[1], 1), return_sequences=True))
        self.model.add(GRU(50))
        self.model.add(Dense(4, activation='softmax'))
        self.model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])



        checkpoint = ModelCheckpoint('model.h5', save_best_only=True, monitor='val_accuracy', mode='max')
        self.model.fit(X_train[:, :, None], y_train, validation_data=(X_test[:, :, None], y_test), epochs=10,
                       batch_size=32, callbacks=[checkpoint])



        # 성능
        loss, accuracy = self.model.evaluate(X_test[:, :, None], y_test)
        print("Model accuracy:", accuracy)


    def save_model(self, filename):
        """모델 저장"""
        self.model.save(filename)

    def load_model(self, filename):
        """학습 모델 로드"""
        self.model = load_model(filename)

    def predict_data(self, df):
        """새 데이터 예측"""

        X_new = df.iloc[:, 1:-1].values
        y_pred_new = np.argmax(self.model.predict(X_new[:, :, None]), axis=1)
        df['label'] = y_pred_new
        return df

    def analyze_prediction(self, df, original_labels):
        """위변조 판단"""
        group_averages = df.groupby('name')['label'].mean()
        results = {}
        success_failure = {}

        for name, avg in group_averages.items():
            original_label = original_labels[original_labels['name'] == name]['label'].values[0]
            closest_label = round(avg)
            results[name] = f'기존 label : {original_label}, 예측 label : {closest_label}'


            if int(original_label) == closest_label:
                success_failure[name] = "예측 성공"
            else:
                success_failure[name] = "예측 실패"

        results_df = pd.DataFrame(list(results.items()), columns=['name', 'result'])


        return results, success_failure, results_df


if __name__ == "__main__":
    data_preprocessor = ForensicsDataPreprocessing()
    detector_engine = ForgeryDetectorEngine()

    df_melted, _ = data_preprocessor.preprocess_data('dataset.csv',  is_train=True)
    df_melted = data_preprocessor.apply_simhash(df_melted)
    print("전처리한 값:")
    print(df_melted)

    df_melted.to_csv("result1.csv", index=False)
    detector_engine.train_model(df_melted)
    detector_engine.save_model('model.h5')  # 모델 저장



    #####


    df_test_melted, original_labels = data_preprocessor.preprocess_data('dataset-2.csv', is_train=False)
    df_test_melted = data_preprocessor.apply_simhash(df_test_melted)

    detector_engine.load_model('model.h5') #모델ㄹ드

    predicted_data = detector_engine.predict_data(df_test_melted)
    predicted_data.to_csv("result2.csv", index=False)



    results, success_failure, results_df = detector_engine.analyze_prediction(predicted_data, original_labels)


    print(success_failure)
    print(results_df)


    total = len(results_df)
    success = sum([1 for row in success_failure.values() if "예측 성공" in row])
    success_rate = (success / total) * 100
    print(f"예측 성공률: {success_rate:.2f}%")
