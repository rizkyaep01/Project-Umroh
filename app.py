import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="centered")

# Logo dan teks sambutan
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Kaaba_icon.svg/512px-Kaaba_icon.svg.png", width=200)
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>Ahlan wa Sahlan</h1>", unsafe_allow_html=True)

# Upload file Excel
st.markdown("---")
st.subheader("Unggah Data Paket Umroh (Excel)")

uploaded_file = st.file_uploader("Pilih file Excel (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df["waktu_keberangkatan"] = pd.to_datetime(df["waktu_keberangkatan"])
        
        st.success("Data berhasil diunggah!")

        # Ambil nilai unik dari data untuk filter
        kota_options = sorted(df["kota_keberangkatan"].dropna().unique())
        tanggal_options = sorted(df["waktu_keberangkatan"].dt.date.unique())

        # Filter Form
        st.markdown("---")
        st.subheader("Filter Pencarian Paket Umroh")

        col1, col2 = st.columns(2)
        with col1:
            tanggal = st.selectbox("Tanggal Keberangkatan", tanggal_options)

        with col2:
            kota = st.selectbox("Kota Keberangkatan", kota_options)

        if st.button("Cari Paket Umroh"):
            hasil = df[
                (df["waktu_keberangkatan"].dt.date == tanggal) &
                (df["kota_keberangkatan"] == kota)
            ]

            if hasil.empty:
                st.warning("Tidak ditemukan paket untuk pilihan tersebut.")
            else:
                st.success(f"Ditemukan {len(hasil)} paket:")
                st.dataframe(hasil)

    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
else:
    st.info("Silakan unggah file Excel untuk memulai.")
