# solar-panels-detection-app
Aceasta este o aplicație care are ca scop prevenirea deteriorării panourilor solare. Prin intermediul senzorilor, aceasta colectează date relevante, cum ar fi AC Power, DC Power și temperatura, voltaj, etc., și analizează aceste date pentru a identifica orice variații în graficele de performanță ale panourilor.

Aici sunt pașii succint pentru a vizualiza aplicația prin intermediul ANACONDA app.
  1. Descărcăm toate fișierele;
  2. Deschidem Anaconda;
  3. Introducem secvența: ”cd downloads”, apoi ENTER;
  4. Introducem în continuare: ”cd power-plant-project”, apoi ENTER;
  5. Introducem: ”streamlit run app.py”, apoi ENTER; (în cazul în care dă eroare, este necesar să introducem ”pip install streamlit”;
  6. După ultima secvență introdusă vom fi redirecționați pe browser, aici se va deschide un tab STREAMLIT cu aplicația noastră.
  7. Prima pagină - ABOUT. Aici este descrisă problema abordată de noi, soluția noastră pentru această problemă și cine suntem noi (echipa);
  8. În stânga avem butonul care ne permite să navigăm între pagini.
  9. Facem click pe buton, selectăm DASHBOARD. Pe această pagină avem prezentate variațiile de AC POWER, DC POWER, TEMPERATURA, IRADIAȚIE, RANDAMENTUL ZILNIC ȘI TOTAL AL PANOURILOR SOLARE. Aceste date sunt extrase din fișierele de tip CSV încărcate direct în cod. Acestea pot fi modificate în dependență de noi fișiere de tip CSV care pot fi introduse direct în această pagină by dragging, droping or browsing files. 
  10. Facem click pe buton, selectăm PERFORMANCE. Pe această pagină observăm performanța panourilor solare. Pentru a da exemplu, avem preluate datele de la o centrală de energie solară. Aici este reprezentat grafic cantitatea și variația de curent electric convertit și generat, randamentul, etc., și tot aici este graficul performanței componentelor, în special, cele care nu funcționează la capacitate normală.
  11. Facem click pe buton, selectăm FORECASTING. Această pagina are ca scop reprezentarea grafică a prezicerilor cantității de energie generată de panourilor solare. Făcând o analiză pe baza datelor deja colectate, aplicația poate genera prognoze în raport cu curentul electric generat de panouri solare. Astfel, proprietarul, poate face o analiză a energiei solare care o va obține în timpul apropiat.
