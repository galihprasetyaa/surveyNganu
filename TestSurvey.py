import streamlit as st
import matplotlib.pyplot as plt
import csv
import os

# Data & Konfigurasi awal
pertanyaan_list = [
    "1. Apakah bumi itu bulat?",
    "2. Apakah Python adalah bahasa pemrograman?",
    "3. Apakah matahari mengelilingi bumi?",
    "4. Apakah air mendidih pada suhu 100 derajat Celsius?"
]

pilihan_jawaban = ["Benar", "Salah", "Tidak tahu"]

# Inisialisasi session state
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.jawaban_respondens = []
    st.session_state.hasil_survei = {jawaban: 0 for jawaban in pilihan_jawaban}
    st.session_state.selesai = False

st.title("📝 Survei Pendapat Sederhana")

if not st.session_state.selesai:
    # Tampilkan pertanyaan
    current_q = st.session_state.current_question
    st.write(pertanyaan_list[current_q])
    jawaban = st.radio("Pilih jawaban Anda:", pilihan_jawaban)

    if st.button("Kirim Jawaban"):
        st.session_state.jawaban_respondens.append(jawaban)
        st.session_state.hasil_survei[jawaban] += 1
        st.session_state.current_question += 1

        if st.session_state.current_question >= len(pertanyaan_list):
            st.session_state.selesai = True
        st.experimental_rerun()

else:
    st.subheader("✅ Survei Selesai!")
    total = sum(st.session_state.hasil_survei.values())
    for pilihan, jumlah in st.session_state.hasil_survei.items():
        persen = (jumlah / total) * 100 if total > 0 else 0
        st.write(f"- {pilihan}: {jumlah} jawaban ({persen:.2f}%)")

    # Visualisasi hasil
    st.subheader("📊 Visualisasi Hasil")
    fig, ax = plt.subplots()
    ax.bar(st.session_state.hasil_survei.keys(), st.session_state.hasil_survei.values(), color=['green', 'red', 'gray'])
    ax.set_ylabel("Jumlah Jawaban")
    ax.set_title("Hasil Survei")
    st.pyplot(fig)

    # Simpan ke CSV
    csv_path = "hasil_survei.csv"
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Pertanyaan", "Jawaban"])
        for pertanyaan, jawaban in zip(pertanyaan_list, st.session_state.jawaban_respondens):
            writer.writerow([pertanyaan, jawaban])
    st.success(f"Hasil disimpan ke: `{os.path.abspath(csv_path)}`")

    # Tombol untuk ulangi survei
    if st.button("Ulangi Survei"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
