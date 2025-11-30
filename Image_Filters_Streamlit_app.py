import io
import base64
import os

import cv2
import numpy as np
import streamlit as st
from PIL import Image

from filters import *  # your bw_filter, sepia, vignette, pencil_sketch, etc.


# Generating a link to download a particular image file.
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href


# Base directory of this script (Applications folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Thumbnail image paths (put the JPGs in the same folder as this .py file)
THUMB_BW = os.path.join(BASE_DIR, "filter_bw.jpg")
THUMB_SEPIA = os.path.join(BASE_DIR, "filter_sepia.jpg")
THUMB_VIGNETTE = os.path.join(BASE_DIR, "filter_vignette.jpg")
THUMB_PENCIL = os.path.join(BASE_DIR, "filter_pencil_sketch.jpg")


# Set title.
st.title("Artistic Image Filters")

# Upload image.
uploaded_file = st.file_uploader("Choose an image file:", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Convert the file to an OpenCV image (BGR).
    raw_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)

    input_col, output_col = st.columns(2)

    with input_col:
        st.header("Original")
        # Display uploaded image.
        st.image(img, channels="BGR", use_container_width=True)

    st.header("Filter Examples:")

    # Display a selection box for choosing the filter to apply.
    option = st.selectbox(
        "Select a filter:",
        (
            "None",
            "Black and White",
            "Sepia / Vintage",
            "Vignette Effect",
            "Pencil Sketch",
        ),
    )

    # Define columns for thumbnail images.
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.caption("Black and White")
        if os.path.exists(THUMB_BW):
            st.image(THUMB_BW, use_container_width=True)
        else:
            st.write("Preview not available")

    with col2:
        st.caption("Sepia / Vintage")
        if os.path.exists(THUMB_SEPIA):
            st.image(THUMB_SEPIA, use_container_width=True)
        else:
            st.write("Preview not available")

    with col3:
        st.caption("Vignette Effect")
        if os.path.exists(THUMB_VIGNETTE):
            st.image(THUMB_VIGNETTE, use_container_width=True)
        else:
            st.write("Preview not available")

    with col4:
        st.caption("Pencil Sketch")
        if os.path.exists(THUMB_PENCIL):
            st.image(THUMB_PENCIL, use_container_width=True)
        else:
            st.write("Preview not available")

    # Flag for showing output image.
    output_flag = 1
    # Colorspace of output image.
    color = "BGR"

    # Generate filtered image based on the selected option.
    if option == "None":
        # Don't show output image.
        output_flag = 0
        output = None
    elif option == "Black and White":
        output = bw_filter(img)
        color = "GRAY"
    elif option == "Sepia / Vintage":
        output = sepia(img)
    elif option == "Vignette Effect":
        level = st.slider("Vignette level", 0, 5, 2)
        output = vignette(img, level)
    elif option == "Pencil Sketch":
        ksize = st.slider("Blur kernel size", 1, 11, 5, step=2)
        output = pencil_sketch(img, ksize)
        color = "GRAY"

    with output_col:
        if output_flag == 1 and output is not None:
            st.header("Output")
            st.image(output, channels=color, use_container_width=True)

            # Convert cv2 image to PIL format for saving via download link.
            if color == "BGR":
                # Convert BGR → RGB
                result = Image.fromarray(output[:, :, ::-1])
            else:
                result = Image.fromarray(output)

            # Display download link.
            st.markdown(
                get_image_download_link(result, "output.jpg", "Download Output"),
                unsafe_allow_html=True,
            )
