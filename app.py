import streamlit as st
from PIL import Image
import numpy as np
from model import GetTopSimilar
from getData import GetMatrixCompare, GetInputArray
import os
import time
from io import BytesIO

# Title of the web app
st.title('Recycled stuffs from materials recommendation')

# Add a radio button to select the input method
input_method = st.radio("Select Input Method:", ("Upload Image", "Take Photo"))

start = time.time()  # Start time

if input_method == "Upload Image":
    # File uploader for image
    image_file = st.file_uploader("Upload an image", type=['jpg', 'png', 'webp'])
    if image_file is not None:
        # Display the uploaded image
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

        # Display identified materials
        col1, col2 = st.columns(2)
        with col1:
            st.write("Identified Materials")
            for material_id, material_quantity in enumerate(input_array):
                if material_quantity != 0:
                    material_name = materials.get(material_id + 1, "Unknown Material")
                    st.write(f"- You have {material_quantity} of '{material_name}'")

        with col2:
            st.button("Adjust Quantities")

        # Get top similar using GetTopSimilar
        top_similar = GetTopSimilar(input_array, compare_matrix)

        # Display top similar recycled items
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

elif input_method == "Take Photo":
    # Camera input to take a photo
    picture = st.camera_input("Take a picture")

    if picture is not None:
        # Convert the captured image to bytes
        image_bytes = picture.read()
        
        # Convert the bytes to a PIL Image
        image = Image.open(BytesIO(image_bytes))

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

        # Display identified materials
        col1, col2 = st.columns(2)
        with col1:
            st.write("Identified Materials")
            for material_id, material_quantity in enumerate(input_array):
                if material_quantity != 0:
                    material_name = materials.get(material_id + 1, "Unknown Material")
                    st.write(f"- You have {material_quantity} of '{material_name}'")

        with col2:
            st.button("Adjust Quantities")

        # Get top similar using GetTopSimilar
        top_similar = GetTopSimilar(input_array, compare_matrix)

        # Display top similar recycled items
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

# Calculate time taken
end = time.time()
st.write(f"Processing Time: {end - start} seconds")
