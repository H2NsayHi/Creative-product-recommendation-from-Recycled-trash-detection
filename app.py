import streamlit as st
from PIL import Image
import numpy as np
from model import GetTopSimilar
from getData import GetMatrixCompare, GetInputArray
import os
import time



# Title of the web app
st.title('Recycled stuffs from materials recommendation')

# File uploader for image
image_file = st.file_uploader("Upload an image", type=['jpg', 'png', 'webp'])
start = time.time()
# Check if image is uploaded
if image_file is not None:
    # Display the image
    image = Image.open(image_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    

    # Get input array using GetInputArray
    num_of_ingredient = 24  # Assuming number of ingredients
    input_array = GetInputArray(image, num_of_ingredient).input_array


    # Assuming your JSON file path
    json_file_path = 'data.json'

    # Get compare matrix using GetMatrixCompare
    gmc = GetMatrixCompare(json_file_path)

    compare_matrix = gmc.matrix
    materials = {material["id"]: material["name"] for material in gmc.materials}
    recycled_items = {item["id"]: item for item in gmc.recycled}

    col1, col2 = st.columns(2)
    with col1:
        st.write("VẬT LIỆU NHẬN DIỆN ĐƯỢC")
        for material_id, material_quantity in enumerate(input_array):
            if material_quantity != 0:
                material_name = materials.get(material_id + 1, "Unknown Material")
                st.write(
                    f""" - Bạn có {material_quantity} vật liệu '{material_name}'"""
                    )
    with col2:
        st.button("Điều chỉnh số lượng")

    # Get top similar using GetTopSimilar
    top_similar = GetTopSimilar(input_array, compare_matrix)

    # Create a Streamlit layout with two columns
    col1, col2 = st.columns(2)

    for recycled_id, euclidean_distance in zip(top_similar.recycled_id, top_similar.euclidean_distances):
            col1, col2 = st.columns(2)
            with col1:
                recycled_image_path = f'recycled_images/{recycled_id+1}.png'
                if os.path.exists(recycled_image_path):
                    recycled_image = Image.open(recycled_image_path)
                    st.image(recycled_image, caption=f'Recycled ID: {recycled_id+1}', use_column_width=True)
                else:
                    st.write(f'Image not found for Recycled ID: {recycled_id+1}')
            with col2:
                recycled_item = recycled_items[recycled_id+1]
                st.write(f'Recycled ID: {recycled_id+1}')
                st.write(f'Euclidean Distance: {euclidean_distance}')
                st.write(f"Name: {recycled_item['name']}")
                st.write(f"URL: {recycled_item['url']}")
                st.write(f"Difficulty Level: {recycled_item['difficult_level']}")
                st.write(f"Danger Level: {recycled_item['danger_level']}")
                st.write('--------------------------------')
    
    end = time.time()
    st.write(f"Thời gian tính toán: {end - start}")




