import streamlit as st
import matplotlib.pyplot as plt
import csv
import os

# Pertanyaan survei
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
    st.session_state.hasil_survei = {j: 0 for j in pilihan_jawaban}
    st.session_state.selesai = False

st.title("📝 Survei Pendapat")

if not st.session_state.selesai:
    index = st.session_state.current_question
    st.subheader(pertanyaan_list[index])
    jawaban = st.radio("Pilih jawaban Anda:", pilihan_jawaban, key=f"q_{index}")
    
    if st.button("Kirim Jawaban", key=f"submit_{index}"):
        st.session_state.jawaban_respondens.append(jawaban)
        st.session_state.hasil_survei[jawaban] += 1
        st.session_state.current_question += 1

        if st.session_state.current_question >= len(pertanyaan_list):
            st.session_state.selesai = True

        # Hindari rerun paksa — Streamlit akan refresh otomatis
        # st.experimental_rerun()

else:
    st.success("✅ Survei selesai!")
    st.write("**Rekap Jawaban:**")
    total = sum(st.session_state.hasil_survei.values())
    for pilihan, jumlah in st.session_state.hasil_survei.items():
        persen = (jumlah / total) * 100 if total > 0 else 0
        st.write(f"- {pilihan}: {jumlah} jawaban ({persen:.2f}%)")

    # Visualisasi
    fig, ax = plt.subplots()
    ax.bar(st.session_state.hasil_survei.keys(), st.session_state.hasil_survei.values(), color=['green', 'red', 'gray'])
    ax.set_ylabel("Jumlah Jawaban")
    ax.set_title("Hasil Survei")
    st.pyplot(fig)

    # Simpan ke file
    filename = "hasil_survei.csv"
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Pertanyaan", "Jawaban"])
        for pertanyaan, jawaban in zip(pertanyaan_list, st.session_state.jawaban_respondens):
            writer.writerow([pertanyaan, jawaban])
    st.success(f"Hasil disimpan sebagai `{filename}`")

    if st.button("🔁 Ulangi Survei"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
