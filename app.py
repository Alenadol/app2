import sklearn
#from sklearn.ensemble import GradientBoostingClassifier
import streamlit as st
import pickle
import numpy as np

import base64
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
     background-image: url("data:image/png;base64,%s");
     background-size: cover;
     }
     </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return
set_png_as_page_bg('8.png')


classifier_name=['GradientBoosting']
option = st.sidebar.selectbox('Предиктивная модель для депозитных сделок (ФЛ)', classifier_name)
st.subheader(option)



model=pickle.load(open("model_saved","rb"))



def predict_churn(days_passed, age, house_loan, duration, number_previous_contact, loan):
    input = np.array([[days_passed, age, house_loan, duration, number_previous_contact, loan]])
    prediction = model.predict_proba(input)[:, 1] * 100
    return float(prediction)    



def main():
    st.title("Предиктивная модель для депозитных сделок (ФЛ)")
    html_temp = """
    <div style="background-color:white ;padding:5px">
    <h2 style="color:black;text-align:center;"> депозиты позволяют безопасно хранить, накапливать и увеличивать сумму денежных средств. По окончании срока действия договора вкладчик получает вложенную сумму с процентами.</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    st.sidebar.image('9.jpg', width=300)
    st.sidebar.subheader("Учебный проект IT Academy/ w.2.0")
    st.sidebar.info("Не спала до трех ночи Алёна Долбик")

    days_passed = st.sidebar.slider('Последний раз клиенту звонили ... дней назад', 0, 365)
  

    age = st.sidebar.number_input('Возраст', min_value=16, max_value=100, step=1)
    #st.slider("Возраст", 10, 100)
    number_previous_contact = st.number_input('Клиенту уже позвонили ... раз:', min_value=1, max_value=50, step = 1)
    
    house_loan = st.sidebar.selectbox('Ипотека', ['да', 'нет'])
    if house_loan == 'да':
        house_loan = 1
    else:
        house_loan = 0
    
    loan = st.sidebar.selectbox('Потребительский кредит', ['да', 'нет'])
    if loan == 'да':
        loan = 1
    else:
        loan = 0

    duration = st.sidebar.slider('Длительность звонка, min', 0, 60)
   

    churn_html = """  
              <div style="background-color:#f44336;padding:20px >
               <h2 style="color:red;text-align:center;"> Клиенту с большой долей вероятности будут интересны вклады => высокаяя доля вероятности заключения депозита . <br>Добавить клиента в CRM кампанию.</h2>
               </div>
            """
    
    no_churn_html = """  
              <div style="background-color:#94be8d;padding:20px >
               <h2 style="color:green ;text-align:center;"> Клиенту с большой долей вероятности будут не интересны вклады.</h2>
               </div>
            """
    
    mb_churn_html = """  
              <div style="background-color:#c9c7c7;padding:20px >
              <h2 style="color:blue ;text-align:center;"> Клиент может уйти из банка. <br>Добавить клиента в CRM кампанию: удержание клиентов.</h2>
              </div>
            """

    
    if age < 16:
        st.error('Некорректный возраст клиента')
    
    else:
        if st.sidebar.button('Прогноз'):
              
            if age < 40 and number_previous_contact < 5 and house_loan == 0 and NumOfProducts == 1:
                st.success('Вероятность заключения депозитного договора не менее 90%.')
                st.markdown(churn_html, unsafe_allow_html= True)

                        
            else:
                output = predict_churn(days_passed, age, house_loan, duration, number_previous_contact, loan)
                st.success('Вероятность заключения депозитного договора низкая')
    #st.markdown(no_churn_html, unsafe_allow_html= True)
                    #st.balloons()


if __name__=='__main__':
    main()

