import numpy as np
import streamlit as st

def text_to_matrix(text):
    """Konversi teks menjadi matriks"""
    text = text.upper().replace(' ', '')
    matrix = [ord(char) - ord('A') for char in text]
    return matrix

def matrix_to_text(matrix):
    """Konversi matriks kembali menjadi teks"""
    return ''.join(chr(num + ord('A')) for num in matrix)

def matrix_multiply(key_matrix, vector):
    """Perkalian matriks untuk enkripsi/dekripsi"""
    result = []
    for i in range(0, len(vector), len(key_matrix)):
        sub_vector = vector[i:i+len(key_matrix)]
        if len(sub_vector) < len(key_matrix):
            sub_vector += [0] * (len(key_matrix) - len(sub_vector))
        
        row_result = [
            sum(key_matrix[j][k] * sub_vector[k] for k in range(len(key_matrix))) % 26
            for j in range(len(key_matrix))
        ]
        result.extend(row_result)
    return result

def hill_cipher_encrypt(plaintext, key_matrix):
    """Enkripsi Hill Cipher"""
    vector = text_to_matrix(plaintext)
    encrypted_vector = matrix_multiply(key_matrix, vector)
    return matrix_to_text(encrypted_vector)

def hill_cipher_decrypt(ciphertext, key_matrix):
    """Dekripsi Hill Cipher"""
    vector = text_to_matrix(ciphertext)
    decrypted_vector = matrix_multiply(key_matrix, vector)
    return matrix_to_text(decrypted_vector)

def get_matrix_inverse_mod_26(matrix):
    """Cari invers modular matriks dalam mod 26"""
    determinant = int(np.round(np.linalg.det(matrix))) % 26
    determinant_inv = pow(determinant, -1, 26)
    matrix_mod_inverse = (
        determinant_inv
        * np.round(determinant * np.linalg.inv(matrix)).astype(int)
    ) % 26
    return matrix_mod_inverse.tolist()

def practice_page():
    """Halaman Latihan Hill Cipher"""
    st.title('Latihan Hill Cipher')
    
    # Soal-soal Hill Cipher
    soal = [
      {
          'id': 1,
          'pertanyaan': 'Enkripsi teks "CIPHER" menggunakan matriks kunci [[3, 3], [2, 5]]',
          'kunci': [[3, 3], [2, 5]],
          'jawaban_benar': 'ESONLP'  
      },
      {
          'id': 2,
          'pertanyaan': 'Dekripsi teks "RIJVS" menggunakan matriks kunci [[3, 3], [2, 5]]',
          'kunci': [[3, 3], [2, 5]],
          'jawaban_benar': 'HELLO'
      },
      {
          'id': 3,
          'pertanyaan': 'Kunci apa yang digunakan untuk dekripsi jika kunci awal adalah [[3, 3], [2, 5]]?',
          'kunci': [[3, 3], [2, 5]],
          'jawaban_benar': '15 17 20 3'
      }
    ]

    
    # Membuat formulir dengan tata letak vertikal
    jawaban_user = {}
    for idx, soal_data in enumerate(soal, start=1):
        st.subheader(f"Soal {idx}")
        st.write(soal_data['pertanyaan'])
        jawaban_user[idx] = st.text_input(f"Jawaban Soal {idx}")
    
    # Tombol untuk menghitung nilai
    if st.button('Koreksi Jawaban'):
        skor = 0
        for idx, soal_data in enumerate(soal, start=1):
            if jawaban_user[idx].upper() == soal_data['jawaban_benar']:
                skor += 1
        
        # Tampilkan hasil
        st.subheader(f"Skor Anda: {skor}/{len(soal)}")
        if skor == len(soal):
            st.success("Luar biasa! Semua jawaban benar.")
        elif skor > 0:
            st.info("Bagus! Tapi masih ada yang salah.")
        else:
            st.error("Sayang sekali, semua jawaban salah. Coba lagi!")

def main():
    st.sidebar.title("Navigasi")

    # Tentukan halaman aktif menggunakan session_state
    if "page" not in st.session_state:
        st.session_state.page = "Perkenalan"  # Halaman default

    # Sidebar navigasi
    if st.sidebar.button("Perkenalan"):
        st.session_state.page = "Perkenalan"
    if st.sidebar.button("Latihan"):
        st.session_state.page = "Latihan"

    # Tampilkan halaman sesuai state
    if st.session_state.page == "Perkenalan":
        introduction_page()
    elif st.session_state.page == "Latihan":
        practice_page()


def introduction_page():
    """Halaman Perkenalan Hill Cipher"""
    st.title("Perkenalan Hill Cipher")
    st.write("""
    Hill Cipher adalah metode kriptografi klasik yang menggunakan konsep aljabar linier untuk mengenkripsi dan mendekripsi pesan.
    Dalam metode ini, teks dikonversi menjadi angka berdasarkan urutan alfabet (A=0, B=1, ..., Z=25), 
    kemudian dilakukan operasi matriks menggunakan matriks kunci.
    """)

    st.header("Langkah-Langkah Enkripsi")
    st.image(
    "hill-cipher-encryption.svg",
    caption="Skema Enkripsi Hill Cipher",
    use_column_width=True
    )
    st.write("""
    1. Konversi teks menjadi angka (A=0, B=1, ..., Z=25).
    2. Pilih matriks kunci berukuran NxN (ukuran sesuai dengan panjang teks).
    3. Kalikan matriks kunci dengan vektor teks, lalu ambil hasil modulus 26.
    4. Konversi hasilnya kembali menjadi teks.
    """)
    st.header("Langkah-Langkah Dekripsi")
    st.image(
        "hill-cipher-decryption.svg",
        caption="Skema Dekripsi Hill Cipher",
        use_column_width=True
    )
    st.write("""
    1. Gunakan matriks kunci dan cari invers modularnya (jika ada).
    2. Kalikan matriks invers dengan vektor teks terenkripsi.
    3. Ambil hasil modulus 26 dan konversi kembali ke teks.
    """)
    

    


if __name__ == '__main__':
    main()
