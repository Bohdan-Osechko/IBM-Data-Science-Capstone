import folium
import pandas as pd

# 1. Завантаження даних
df = pd.read_csv("dataset_part_2.csv")

# Координати майданчиків (приблизні для SpaceX)
launch_sites = {
    'CCAFS SLC 40': [28.562302, -80.577356],
    'VAFB SLC 4E': [34.632834, -120.610745],
    'KSC LC 39A': [28.573255, -80.646895]
}

# 2. Створення карти, центрованої на США
site_map = folium.Map(location=[30, -100], zoom_start=4)

# 3. Додавання маркерів для кожного майданчика
for site, coord in launch_sites.items():
    circle = folium.Circle(coord, radius=1000, color='#d35400', fill=True).add_child(folium.Popup(site))
    marker = folium.Marker(coord, icon=folium.DivIcon(html=f'<div style="font-size: 12; color:#d35400;"><b>{site}</b></div>'))
    site_map.add_child(circle)
    site_map.add_child(marker)

# 4. Додавання прикладу вимірювання відстані (Критерій 1.13)
# Наприклад, відстань від KSC LC 39A до найближчого узбережжя
coastline_coord = [28.57325, -80.60682]
folium.PolyLine([launch_sites['KSC LC 39A'], coastline_coord], color='blue').add_to(site_map)

# Збереження карти
site_map.save('spacex_map.html')
print("Карту 'spacex_map.html' успішно збережено!")