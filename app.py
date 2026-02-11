import streamlit as st
import re
from collections import Counter

# =========================
# Fungsi intisari materi
# =========================
def intisari_materi(teks, jumlah_poin=5):
    # 1. Normalisasi teks
    teks = teks.lower()
    teks = re.sub(r'[^a-zA-Z\s.]', '', teks)

    # 2. Pisahkan kalimat
    kalimat = [k.strip() for k in teks.split('.') if k.strip()]

    # 3. Stopwords sederhana Bahasa Indonesia
    stopwords = {
        'dan','yang','di','ke','dari','ini','itu','adalah','untuk',
        'dengan','pada','sebagai','oleh','dalam','atau','karena'
    }

    # 4. Hitung frekuensi kata penting
    kata_penting = [w for w in teks.split() if w not in stopwords]
    frekuensi = Counter(kata_penting)

    # 5. Skor tiap kalimat
    skor_kalimat = {}
    for k in kalimat:
        for w in k.split():
            if w in frekuensi:
                skor_kalimat[k] = skor_kalimat.get(k, 0) + frekuensi[w]

    # 6. Ambil kalimat inti
    kalimat_inti = sorted(skor_kalimat, key=skor_kalimat.get, reverse=True)[:jumlah_poin]

    # 7. Format hasil
    hasil = []
    for i, k in enumerate(kalimat_inti, 1):
        hasil.append(f"{i}. {k.capitalize()}.")
    return "\n".join(hasil)


# =========================
# UI Streamlit
# =========================
st.set_page_config(page_title="Asisten Pembuat Intisari Materi", page_icon="📝")

st.title("📝 Asisten Peringkas Materi")
st.write("Masukkan materi di bawah ini, lalu pilih jumlah poin intisari:")

# Input teks materi
materi = st.text_area("Masukkan Materi:", height=200)

# Pilih jumlah poin ringkasan
jumlah_poin = st.slider("Jumlah Poin Ringkasan:", min_value=1, max_value=10, value=5)

# Tombol Ringkas
if st.button("Ringkas Materi"):
    if materi.strip() == "":
        st.warning("Silakan masukkan materi terlebih dahulu!")
    else:
        ringkasan = intisari_materi(materi, jumlah_poin)
        st.subheader("📌 Intisari Materi:")
        st.text(ringkasan)
