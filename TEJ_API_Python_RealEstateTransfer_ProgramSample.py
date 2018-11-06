#pip install selenium
#pip install folium 
#pip install tejapi
import tejapi 
import folium.plugins
import pandas as pd
import os
from selenium import webdriver
#金鑰
tejapi.ApiConfig.api_key = "userKey"
if __name__ == "__main__": 
#   TEJ API 設定 
    data = tejapi.get("TWN/AAPRTRAN",coid="A",ann_date={"gt":"2018-09-01"},opts={"sort":"tot_prc.desc"},paginate=True)
#   folium套件    產生地圖TXT 設定基礎座標
    TPE_COORDINATES = (24.1075342,  120.6000887)
    m = folium.Map(location=TPE_COORDINATES, zoom_start=8 , tiles="Stamen Terrain")
    cluster = folium.plugins.MarkerCluster().add_to(m)
    for rowNumber in data.index.tolist():
        coordinate_X = None
        coordinate_Y = None
        tot_prc = None  
        location = None
        for columName in data.columns:
            val = data.get(columName)[rowNumber]
#             print(data.get(columName)[rowNumber])
            if pd.isnull(val):
                val = ""
            val = str(val)
            if columName=="coord_x":
                coordinate_X = val
            elif columName=="coord_y":
                coordinate_Y = val
            elif columName=="tot_prc":   
                tot_prc = val
            elif columName=="location":
                location = val
        if coordinate_X == "" or coordinate_Y == "":
            continue
#         print(str(rowNumber)+" # "+coordinate_X+","+coordinate_Y)
        folium.Marker(location=[float(coordinate_X), float(coordinate_Y)]     
                      ,popup =str(location +"<br/> 售價金額: " + tot_prc+"萬")
                      ,icon = folium.Icon(color="blue",icon="cloud")
                      ).add_to(cluster)              
        folium.LayerControl(collapsed=False).add_to(m) 
    m.save("地圖.html")
    try:
        print(os.getcwd())
        path = os.getcwd() + "\\"
        driver = webdriver.Chrome(executable_path = path + "chromedriver.exe")
#         driver.maximize_window()
        driver.get(path + "地圖.html")
    except Exception as e:
        raise
    finally:
        driver.quit()
    pass

    