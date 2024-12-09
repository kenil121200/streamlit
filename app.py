import time
import streamlit as st
from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np

occlusion_class_names =  ['Blocked', 'Clear', 'Partially Blocked']
fog_density_class_names = ['No Fog', 'Dense Fog', 'Light Fog']
revised_occlusion_class_names = ['Clear', 'Partially Blocked', 'Blocked']
revised_fog_density_class_names = ['No Fog', 'Light Fog', 'Dense Fog']


st.title("Visual Coverage and Fog Density Level")

image_folder_path = "test_images"
image_files = [f for f in os.listdir(image_folder_path) if f.endswith(("jpg", "jpeg", "png"))]

if "current_image_index" not in st.session_state:
    st.session_state.current_image_index = 0

left, middle, right = st.columns(3)
if left.button("Previous", use_container_width=True):
    st.session_state.current_image_index = (st.session_state.current_image_index - 1) % len(image_files)
if right.button("Next", use_container_width=True):
    st.session_state.current_image_index = (st.session_state.current_image_index + 1) % len(image_files)

image_name = image_files[st.session_state.current_image_index]
current_image_path = os.path.join(image_folder_path, image_name)
image = Image.open(current_image_path)

predictions = {'6.jpg': ['Clear', 'No Fog'], '8.jpg': ['Blocked', None], '14.jpg': ['Clear', 'Light Fog'], '3.jpg': ['Partially Blocked', 'No Fog'], '18.jpg': ['Partially Blocked', 'No Fog'], '13.jpg': ['Partially Blocked', 'No Fog'], '20.jpg': ['Partially Blocked', 'Light Fog'], '10.jpg': ['Blocked', None], '16.jpg': ['Partially Blocked', 'No Fog'], '15.jpg': ['Blocked', None], '5.jpg': ['Blocked', None], '7.jpg': ['Partially Blocked', 'No Fog'], '2.jpg': ['Partially Blocked', 'No Fog'], '19.jpg': ['Partially Blocked', 'No Fog'], '12.jpg': ['Clear', 'Light Fog'], '1.jpg': ['Blocked', None], '17.jpg': ['Partially Blocked', 'No Fog'], '9.jpg': ['Clear', 'Dense Fog'], '11.jpg': ['Partially Blocked', 'Dense Fog'], '4.jpg': ['Clear', 'No Fog']}

occlusion_prediction, fog_density_prediction = predictions[image_name]

occlusion_level = revised_occlusion_class_names.index(occlusion_prediction) + 1
fog_level = revised_fog_density_class_names.index(fog_density_prediction) + 1 if fog_density_prediction else None


def plot_vertical_bar(level, class_names, colors, title=None):
    fig, ax = plt.subplots(figsize=(1.5, 5))
    rgb_background = (14 / 255, 17 / 255, 23 / 255) 
    fig.patch.set_facecolor(rgb_background) 
    ax.set_facecolor(rgb_background)
    ax.bar(0, level, color=colors[level - 1], width=0.5)
    ax.set_ylim(0, len(class_names))
    ax.set_xticks([]) 
    ax.set_yticks(range(1, len(class_names) + 1))
    ax.set_yticklabels(class_names, fontsize=8)
    ax.tick_params(axis='y', length=0) 
    if title:
        ax.set_title(title, fontsize=10)
    else:
        ax.set_title("")

    ax.axis('off') 
    return fig

def display_fog_legend():
    st.markdown("""
        <div style="display: flex; align-items: center;">
            <div style="width: 20px; height: 20px; background-color: #16F4D0; margin-right: 10px;"></div>
            <div style="font-size: 12px; color: white;">No Fog</div>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="width: 20px; height: 20px; background-color: #429EA6; margin-right: 10px;"></div>
            <div style="font-size: 12px; color: white;">Light Fog</div>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="width: 20px; height: 20px; background-color: #153B50; margin-right: 10px;"></div>
            <div style="font-size: 12px; color: white;">Dense Fog</div>
        </div>
    """, unsafe_allow_html=True)

def display_occ_legend():
    st.markdown("""
        <div style="display: flex; align-items: center;">
            <div style="width: 20px; height: 20px; background-color: #06FF00; margin-right: 10px;"></div>
            <div style="font-size: 12px; color: white;">Clear</div>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="width: 20px; height: 20px; background-color: #FFE400; margin-right: 10px;"></div>
            <div style="font-size: 10px; color: white;">Partially Blocked</div>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="width: 20px; height: 20px; background-color: #FF1700; margin-right: 10px;"></div>
            <div style="font-size: 12px; color: white;">Blocked</div>
        </div>
    """, unsafe_allow_html=True)

occlusion_colors = ['#06FF00', '#FFE400', '#FF1700']  
fog_colors = ['#16F4D0', '#429EA6', '#153B50']        

occlusion_bar = plot_vertical_bar(occlusion_level, revised_occlusion_class_names, occlusion_colors)
fog_bar = None
if fog_level:
    fog_bar = plot_vertical_bar(fog_level, revised_fog_density_class_names, fog_colors)

col1, col2, col3 = st.columns([1, 4, 1], vertical_alignment="top")
with col1:
    st.markdown('''##### :blue[Visual Coverage]''')
    display_occ_legend()
    st.pyplot(occlusion_bar)  
    
with col2:
    st.image(image, use_container_width=True) 
with col3:
    st.markdown('''##### :blue[Fog Density]''')
    
    if fog_density_prediction:
        display_fog_legend()
        st.pyplot(fog_bar)  
    else:
        st.write("Fog density unavailable.")