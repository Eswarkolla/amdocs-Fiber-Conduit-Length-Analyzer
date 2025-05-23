
import re
import fitz  # PyMuPDF
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to extract lengths from the PDF
def extract_lengths_from_pdf(file_path):
    pdf_document = fitz.open(file_path)
    trench_lengths = {}
    bore_lengths = {}
    hand_dig_lengths = {}

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")

        trench_matches = re.findall(r"TRENCH AND PLACE ±(\d+)'", text)
        bore_matches = re.findall(r"BORE AND INSTALL ±(\d+)'", text)
        hand_dig_matches = re.findall(r"HAND DIG AND INSTALL ±(\d+)'", text)

        trench_lengths[page_num + 1] = sum(map(int, trench_matches))
        bore_lengths[page_num + 1] = sum(map(int, bore_matches))
        hand_dig_lengths[page_num + 1] = sum(map(int, hand_dig_matches))

    return trench_lengths, bore_lengths, hand_dig_lengths

# Function to create a bar chart
def create_bar_chart(data, title, xlabel, ylabel):
    df = pd.DataFrame(list(data.items()), columns=[xlabel, ylabel])
    df.plot(kind='bar', x=xlabel, y=ylabel, legend=False)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# Streamlit app
st.title("PDF Lengths Extraction App")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    with open("uploaded_file.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    trench_lengths, bore_lengths, hand_dig_lengths = extract_lengths_from_pdf("uploaded_file.pdf")

    st.header("Total Lengths")
    st.write(f"Total Trench Length: {sum(trench_lengths.values())} feet")
    st.write(f"Total Bore Length: {sum(bore_lengths.values())} feet")
    st.write(f"Total Hand Dig Length: {sum(hand_dig_lengths.values())} feet")

    st.header("Page-wise Breakdown")
    st.write("Trench Lengths:", trench_lengths)
    st.write("Bore Lengths:", bore_lengths)
    st.write("Hand Dig Lengths:", hand_dig_lengths)

    st.header("Bar Charts")
    create_bar_chart(trench_lengths, "Trench Lengths per Page", "Page", "Trench Length (feet)")
    create_bar_chart(bore_lengths, "Bore Lengths per Page", "Page", "Bore Length (feet)")
    create_bar_chart(hand_dig_lengths, "Hand Dig Lengths per Page", "Page", "Hand Dig Length (feet)")
