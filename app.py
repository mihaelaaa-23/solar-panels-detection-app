from pprint import pprint
import streamlit as st
import requests
import base64
import io
from PIL import Image
import numpy as np
import cv2
from matplotlib import cm
import pandas as pd
import tih



#creating the mode choice button
mode = ["About", "Dashboard", "Performance", "Forecasting"]
choice = st.sidebar.selectbox("Select Page", mode)
data_generation = pd.read_csv("Plant_1_Generation_Data.csv")
data_weather = pd.read_csv("Plant_1_Weather_Sensor_Data.csv")
data_generation, data_weather = tih.drop_and_convert(data_generation, data_weather)


if choice == "Dashboard":
    #creating the upload button for generation data and for weather sensor data and adding the default file to upload in case they are not selected
    data_generation = st.sidebar.file_uploader("Upload new generation data", type = ["csv"], accept_multiple_files = False, key = "generation")
    data_weather = st.sidebar.file_uploader("Upload new weather data", type = ["csv"], accept_multiple_files = False, key = "weather")
    
    if data_generation is None:
        data_generation = pd.read_csv("Plant_1_Generation_Data.csv")
    if data_weather is None:
        data_weather = pd.read_csv("Plant_1_Weather_Sensor_Data.csv")
    data_generation, data_weather = tih.drop_and_convert(data_generation, data_weather)

    #creating the dashboard
    st.title("Dashboard")

    st.write("### Daily yield")
    # creating the plots for daily yield & ac-dc power
    df_gen = data_generation.groupby('DATE_TIME').sum().reset_index()
    daily_gen=df_gen.copy()
    df_gen['DATE_TIME'] = df_gen['DATE_TIME']
    
    st.line_chart(df_gen, x='DATE_TIME', y='DAILY_YIELD')
    df_gen['DATE_TIME'] = df_gen['DATE_TIME'].dt.time

    st.write("### AC-DC Power")
    st.line_chart(df_gen, x='DATE_TIME', y=['AC_POWER', 'DC_POWER'])

    st.write("### Daily yield")
    # creating the plots for daily yield & ac-dc power
    
    daily_gen['date']=daily_gen['DATE_TIME'].dt.date
    daily_gen=daily_gen.groupby('date').sum()
    #show the line chart only for the date and daily yield columns
    st.line_chart(daily_gen['DAILY_YIELD'])
    
    st.write("### Total yield")
    st.bar_chart(daily_gen['TOTAL_YIELD'])

    st.write("### Irradiation, Ambient and Module temperature")
    df_sens = data_weather.groupby('DATE_TIME').mean().reset_index()
    df_sens['time']=df_sens['DATE_TIME'].dt.time
    st.line_chart(df_sens, x='time', y=['IRRADIATION'])
    st.line_chart(df_sens, x='DATE_TIME', y=['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE'])


elif choice == "Performance":
    st.title("Perfomance")
    st.write("### Real DC Power Converted")
    tih.dc_power_converted()
    dc_power_image = Image.open("values/losses.png")
    st.image(dc_power_image, caption="DC Power Converted")

    st.write("### DC Power Generated")
    tih.dc_power_generated()
    dc_power_image = Image.open("values/dc_generated.png")
    st.image(dc_power_image, caption="DC Power Generated")

    st.write("### Underperforming Modules")
    tih.underperforming_modules()
    dc_power_image = Image.open("values/underperforming_modules.png")
    st.image(dc_power_image, caption="Underperforming Modules")

    st.write("### DC POWER and DAILY YIELD in PLANT_1")
    tih.dc_power_daily_yield()
    dc_power_image = Image.open("values/dc_power_daily_yield.png")
    st.image(dc_power_image, caption="DC POWER and DAILY YIELD in PLANT_1")

    st.write("### Module temperature and Ambient Temperature on PLANT_1")
    dc_power_image = Image.open("values/module_ambient_temperature.png")
    st.image(dc_power_image, caption="Module temperature and Ambient Temperature on PLANT_1")


#Settin the camera detection option
elif choice == "Forecasting":
    st.title("Forecasting")
    st.write("### Forecasting of DC Power Generated")
    tih.forecasting()
    dc_power_image = Image.open("values/forecasting.png")
    st.image(dc_power_image, caption="Forecasting of DC Power Generated")

#The description page of the project
elif choice == "About":
   st.write("# PREVENIREA DEFECTELOR PANOURILOR SOLARE  ")
   st.write("---")
   st.write("### PROBLEMA")
   st.write("> Problema panourilor solare care sunt costisitoare și a defectelor nedetectate la timp reprezintă o provocare majoră. În primul rând, prețul ridicat al panourilor solare face ca investiția în energie solară să fie o alegere costisitoare pentru majoritatea oamenilor și companiilor. În plus, perioada lungă de răscumpărare a banilor de cel puțin 10 ani poate descuraja mulți potențiali investitori. În al doilea rând, problema cu detectarea ulterioară a defectelor poate avea consecințe semnificative. Din motiv că panourile solare sunt de obicei amplasate în zone greu accesibile, monitorizarea lor zilnică este dificilă și costisitoare. Acest lucru înseamnă că defectele pot rămâne nedetectate până când panourile nu mai funcționează. Aceasta, la rândul ei, duce la o pierdere semnificativă de timp și resurse financiare, deoarece reparațiile pot fi costisitoare și pot necesita înlocuirea întregului panou.")
   st.write("---")
   st.write("### SOLUȚIA NOASTRĂ")
   st.write("> Crearea unei aplicații care să prevină deteriorarea panourilor solare reprezintă o soluție eficientă pentru a soluționa problemele cu costurile ridicate și cu defectele nedetectate timpurii. Aplicația poate fi proiectată pentru a colecta date relevante despre performanța panourilor solare, cum ar fi AC Power, DC Power, temperatura, voltaj, etc., prin intermediul senzorilor. Aceste date sunt analizate de algoritmi AI care folosesc tehnici de învățare automată pentru a identifica orice variații semnificative în graficele de performanță ale panourilor. În cazul în care aplicația detectează variații semnificative, utilizatorii sunt alertați imediat pentru a lua măsuri preventive. De exemplu, dacă o anumită temperatură depășește un nivel limită, aplicația poate trimite o alertă de sugestie pentru activarea sistemului de răcire sau despre reducerea temporară a producției de energie solară.")
  # st.write("#### There are two possible settings:")
   st.write("---")
   image = Image.open("images/energy.jpg")
   st.image(image)
   #st.write("The Image option works based on already saved images. You need to browse and select an image from your device and afterwards the model will return you the image with identified trash objects.")
   st.write("---")
   st.write("### CINE SUNTEM NOI?")
   st.write("Noi suntem Mihaela Untu și Ciprian Moisenco. Ambii suntem elevi ai Liceului Teoretic ”Iulia Hasdeu” în clasa 12. Împreună am format această echipă pentru a dezvolta un proiect cu elemente de AI drept răspuns la problema detectării întârziate a defectelor panourilor solare. Scopul nostru a fost să propunem o idee ce va ajuta societatea să se dezvolte în continuare. Cu ajutorul mentorului nostru – Doamna Viorica Moglan – am reușit să elaborăm această aplicație și să o îmbunătățim în așa mod ca ea să fie cât mai eficientă.")
   mc_image = Image.open("images/mc.jpg"    )
   st.image(mc_image, caption = "Ciprian & Mihaela")
   mcm_image = Image.open("images/mcm.jpg"    )
   st.image(mcm_image, caption = "Moglan Viorica, Untu Mihaela, Moisenco Ciprian")







