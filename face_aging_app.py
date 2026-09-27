import hashlib
import io
from pathlib import Path

import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Face Age Studio",
    page_icon="👤",
    layout="wide",
)

st.markdown(
    """
    <style>
    @media (max-width: 680px) {
        [data-testid="stAppViewBlockContainer"] {
            padding: 1rem 0.8rem 2rem;
        }
        [data-testid="stHorizontalBlock"] {
            flex-direction: column;
            gap: 0.75rem;
        }
        [data-testid="stColumn"] {
            width: 100% !important;
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
        [data-testid="stImage"] img {
            max-height: 70vh;
            object-fit: contain;
        }
        h1 {
            font-size: 1.75rem;
            line-height: 1.2;
        }
        button, [role="button"] {
            min-height: 44px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

APP_DIR = Path(__file__).resolve().parent
REFERENCE_PATHS = {
    "Age Face": APP_DIR / "old uncle photo .jpeg",
    "De-Age Face": APP_DIR / "teenage boy  photo.jpeg",
}


def open_image(uploaded_file):
    if uploaded_file is None:
        return None
    try:
        return Image.open(uploaded_file).convert("RGB")
    except Exception:
        return None


st.title("Face Age Studio")
st.caption("Show a selected reference photo for the chosen age effect.")

operation = st.radio("Choose result", ["Age Face", "De-Age Face"], horizontal=True)

source_file = st.file_uploader(
    "Upload the original photo",
    type=["jpg", "jpeg", "png"],
    help="This photo is shown as the input; the selected bundled photo is returned as the result.",
)

if source_file is None:
    st.info("Upload an original photo to get started.")
else:
    source_image = open_image(source_file)
    if source_image is None:
        st.error("The original photo could not be opened. Try another JPG or PNG.")
        st.stop()

    reference_path = REFERENCE_PATHS[operation]
    reference_image = open_image(reference_path)

    source_column, result_column = st.columns(2)
    with source_column:
        st.subheader("Original")
        st.image(source_image, use_container_width=True)

    with result_column:
        st.subheader("Result")
        if not reference_path.is_file():
            st.error(f"Reference image is missing: {reference_path.name}")
        elif reference_image is None:
            st.error("The selected reference photo could not be opened. Try another image.")
        else:
            result_key = (
                "reference-output-v1",
                operation,
                hashlib.sha256(source_file.getvalue()).hexdigest(),
                hashlib.sha256(reference_path.read_bytes()).hexdigest(),
            )
            if st.button("Show result", type="primary", use_container_width=True):
                st.session_state.processed_image = reference_image
                st.session_state.processed_key = result_key

            processed = st.session_state.get("processed_image")
            if processed is not None and st.session_state.get("processed_key") == result_key:
                st.image(processed, use_container_width=True)
                output = io.BytesIO()
                processed.save(output, format="PNG")
                st.download_button(
                    "Download PNG",
                    data=output.getvalue(),
                    file_name=f"{operation.lower().replace(' ', '_')}_reference.png",
                    mime="image/png",
                    use_container_width=True,
                )

with st.expander("About this app"):
    st.markdown(
        "This app returns a bundled reference image for the selected effect. "
        "It does not alter the uploaded original photo or generate a new face."
    )