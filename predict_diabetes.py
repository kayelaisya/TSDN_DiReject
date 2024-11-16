import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit as st
import base64
import joblib
import requests
import io
import os

def preprocess_inputs(jenis_kelamin, usia, tinggi_badan, berat_badan, tekanan_darah,
                    kolesterol, cek_kolesterol, merokok, aktif, alkohol, dokter,
                    kesehatan, kesehatan_mental, kesehatan_fisik, stroke, jantung, berjalan):
    # Mapping usia (age) to numerical values for the new age categories
    age_mapping = {
        "18 hingga 24 tahun": 1,
        "25 hingga 29 tahun": 2,
        "30 hingga 34 tahun": 3,
        "35 hingga 39 tahun": 4,
        "40 hingga 44 tahun": 5,
        "45 hingga 49 tahun": 6,
        "50 hingga 54 tahun": 7,
        "55 hingga 59 tahun": 8,
        "60 hingga 64 tahun": 9,
        "65 hingga 69 tahun": 10,
        "70 hingga 74 tahun": 11,
        "75 hingga 79 tahun": 12,
        "80 tahun ke atas": 13
    }

    input_data = {
        'jenis_kelamin': 1 if jenis_kelamin == "Laki-laki" else 0,
        'usia': age_mapping.get(usia, 0),  # Convert age category to numerical value
        'tinggi_badan': tinggi_badan,
        'berat_badan': berat_badan,
        'tekanan_darah': 1 if tekanan_darah == "Tinggi" else 0,
        'kolesterol': 1 if kolesterol == "Tinggi" else 0,
        'periksa_kolesterol': 1 if cek_kolesterol == "Ya" else 0,
        'pernah_merokok': 1 if merokok == "Ya" else 0,
        'aktivitas_fisik': 1 if aktif == "Ya" else 0,
        'konsumsi_alkohol': 1 if alkohol == "Ya" else 0,
        'tidak_ke_dokter_biaya': 1 if dokter == "Ya" else 0,
        'kondisi_kesehatan': ["Sempurna", "Sangat Baik", "Baik", "Cukup", "Buruk"].index(kesehatan) + 1,
        'kesehatan_mental': kesehatan_mental,
        'kesehatan_fisik': kesehatan_fisik,
        'pernah_stroke': 1 if stroke == "Ya" else 0,
        'penyakit_jantung': 1 if jantung == "Ya" else 0,
        'kesulitan_berjalan': 1 if berjalan == "Ya" else 0,
    }
    
    input_data['BMI'] = input_data['berat_badan'] / ((input_data['tinggi_badan'] / 100) ** 2)
    
    model_input = pd.DataFrame([{
        'Sex': input_data['jenis_kelamin'],
        'Age': input_data['usia'],
        'BMI': input_data['BMI'],
        'HighBP': input_data['tekanan_darah'],
        'HighChol': input_data['kolesterol'],
        'CholCheck': input_data['periksa_kolesterol'],
        'Smoker': input_data['pernah_merokok'],
        'PhysActivity': input_data['aktivitas_fisik'],
        'HvyAlcoholConsump': input_data['konsumsi_alkohol'],
        'NoDocbcCost': input_data['tidak_ke_dokter_biaya'],
        'GenHlth': input_data['kondisi_kesehatan'],
        'MentHlth': input_data['kesehatan_mental'],
        'PhysHlth': input_data['kesehatan_fisik'],
        'Stroke': input_data['pernah_stroke'],
        'HeartDiseaseorAttack': input_data['penyakit_jantung'],
        'DiffWalk': input_data['kesulitan_berjalan']
    }])

    return model_input

st.markdown("""
    <style>
    .center-text {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown(
    '<link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.5.0/font/bootstrap-icons.min.css" rel="stylesheet">',
    unsafe_allow_html=True
)

st.image("https://raw.githubusercontent.com/kayelaisya/TSDN_DiReject/main/header%20diabet%20(3).png", width=1024)

with st.sidebar:
    selected = option_menu(
        "Di-Reject", 
        ["Beranda", "Tentang Diabetes", "Cek Diabetes"], 
        icons=['house-fill', 'question-circle-fill', 'calculator-fill'], 
        menu_icon="droplet-half", 
        default_index=0
    )

if selected == "Beranda":
    st.markdown('<h3 style="color:#263487;">Layanan Pengecekan Risiko Diabetes Anda</h3>', unsafe_allow_html=True)
    
    st.markdown('<h2 style="color:#263487; font-weight: bold;">🩸 Apa itu Diabetes?</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        <p style="color:#263487;">
            Diabetes (atau dikenal dengan diabetes melitus) adalah penyakit yang ditandai
            dengan peningkatan kadar glukosa darah (atau gula darah), yang seiring waktu
            menyebabkan kerusakan serius pada organ-organ tubuh.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    
    st.markdown('<h2 style="color:#263487; font-weight: bold;">💡 Fitur Utama Di-Reject</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True, height=150):
            st.markdown('<h3 style="color:#263487;">❓ Tentang Diabetes</h3>', unsafe_allow_html=True)
            st.markdown('<p style="color:#263487;">Pelajari lebih lanjut tentang jenis, gejala, dan pencegahan diabetes.</p>', unsafe_allow_html=True) 
    
    with col2:
        with st.container(border=True, height=150):
            st.markdown('<h3 style="color:#263487;">📱 Cek Risiko Diabetes</h3>', unsafe_allow_html=True)
            st.markdown('<p style="color:#263487;">Cek risiko diabetes Anda dengan cepat.</p>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown('<h2 style="color:#263487; font-weight: bold; ">🤔 Kenapa Di-Reject?</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown(
                '<div style="text-align: center; color:#263487; font-size: 55px;"><i class="bi bi-patch-check-fill"></i></div>',
                unsafe_allow_html=True
            ) 
            st.markdown('<p style="text-align: center; color:#263487; font-size: 19px; line-height: 1.25;">Penilaian Risiko<br>yang Akurat</p>', unsafe_allow_html=True)
    
    with col2:
        with st.container(border=True):
            st.markdown(
                '<div style="text-align: center; color:#263487; font-size: 55px;"><i class="bi bi-lightbulb-fill"></i></div>',
                unsafe_allow_html=True
            ) 
            st.markdown('<p style="text-align: center; color:#263487; font-size: 19px; line-height: 1.25;">Informasi Terkini<br>tentang Diabetes</p>', unsafe_allow_html=True)

    with col3:
        with st.container(border=True, height=162):
            st.markdown(
                '<div style="text-align: center; color:#263487; font-size: 55px;"><i class="bi bi-hand-thumbs-up-fill"></i></div>',
                unsafe_allow_html=True
            ) 
            st.markdown('<p style="text-align: center; color:#263487; font-size: 19px; line-height: 1.25;">Penggunaan<br>Mudah</p>', unsafe_allow_html=True)

    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    
    st.image("https://raw.githubusercontent.com/kayelaisya/TSDN_DiReject/main/header%20diabet%20(4).png", width=1024)
    
elif selected == "Tentang Diabetes": 
    tab1, tab2, tab3 = st.tabs(["💡 Tentang Diabetes", "🧬 Tipe Diabetes", "🔎 Gejala"])
    
    with tab1:
        st.markdown('<h1 style="color:#263487;">Apa Itu Diabetes?</h1>', unsafe_allow_html=True)
        
        st.image("https://raw.githubusercontent.com/kayelaisya/TSDN_DiReject/main/hand-holding-blood-glucose-meter-measuring-blood-sugar-background-is-stethoscope-chart-file.jpg", width=500)
        
        st.markdown(
            """
            <p style="color:#263487;">
                Dilansir dari World Health Organization (WHO), diabetes mellitus adalah penyakit 
                metabolik kronis yang ditandai dengan peningkatan kadar glukosa darah (atau gula darah), 
                yang seiring waktu menyebabkan kerusakan serius pada jantung, pembuluh darah, mata, 
                ginjal, dan saraf.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        st.write('')
        
        st.markdown(
            """
            <p style="color:#263487;">
                Diabetes mellitus merupakan penyakit yang disertai dengan gejala yang dapat dilihat dari 
                beberapa kondisi antara lain seringnya merasa lelah tanpa adanya aktivitas fisik, sering 
                merasa haus padahal sudah minum cukup air, berat badan turun tanpa sebab yang jelas, 
                sering merasa lapar yang ekstrem, sulit sembuhnya luka di tubuh, pandangan kabur, sering 
                buang air kecil, dan sering mengalami infeksi pada kulit, gusi, dan organ intim.
            </p>
            """,
            unsafe_allow_html=True
        )
        
    
    with tab2:
        st.markdown('<h1 style="color:#263487;">Tipe-tipe Diabetes</h1>', unsafe_allow_html=True)
        st.markdown('<h3 style="color:#263487;">1. Diabetes Tipe 1</h3>', unsafe_allow_html=True)
        
        st.image("https://raw.githubusercontent.com/kayelaisya/TSDN_DiReject/main/tipe%20diabet.png", width=400)
        
        st.markdown(
            """
            <p style="text-align: justify; color:#263487; font-size: 18px ;">
                Jika Anda mengidap diabetes tipe 1, kadar gula darah Anda terlalu tinggi karena 
                tubuh tidak dapat memproduksi hormon insulin. Penyebab pasti diabetes tipe 1 belum 
                diketahui, dan tidak ada cara untuk mencegah seseorang mengidapnya.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        st.write('')
        
        st.markdown(
            """
            <p style="text-align: justify; color:#263487; font-size: 18px ;">
                Diabetes tipe 1 sering terdiagnosis pada masa kanak-kanak, namun bisa berkembang 
                pada usia berapa pun. Anda berisiko lebih tinggi mengidap diabetes tipe 1 jika 
                orangtua, saudara kandung, atau anggota keluarga dekat lainnya mengidapnya.<br>
                Insulin adalah pengobatan utama untuk diabetes tipe 1. Memeriksa dan mengelola 
                kadar gula darah sangat penting untuk mengurangi risiko komplikasi diabetes, 
                baik yang bersifat jangka pendek maupun jangka panjang.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        st.write('')
        
        st.markdown(
            """
            <p style="text-align: justify; color:#263487; font-size: 18px ;">
                Insulin adalah pengobatan utama untuk diabetes tipe 1. Memeriksa dan mengelola 
                kadar gula darah sangat penting untuk mengurangi risiko komplikasi diabetes, 
                baik yang bersifat jangka pendek maupun jangka panjang.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        with st.expander("🔴 Gejala"):
            st.markdown("""
            - Sering buang air kecil, terutama pada malam hari.
            - Rasa haus yang terus-menerus.
            - Merasa sangat lelah dan kekurangan energi.
            - Berat badan turun tanpa disengaja atau terlihat lebih kurus dari biasanya.
            """)

        with st.expander("🟡 Penyebab"):
            st.markdown("""
            1. **Genetik** – Riwayat keluarga dapat meningkatkan risiko, karena ada beberapa 
            gen yang terkait dengan diabetes tipe 1. Namun, kebanyakan orang dengan diabetes 
            tipe 1 tidak memiliki riwayat keluarga diabetes.
            2. **Faktor Lingkungan** – Beberapa faktor lingkungan, seperti infeksi virus, 
            diduga dapat memicu terjadinya diabetes tipe 1. 
            3. **Kondisi Autoimun** – Pada diabetes tipe 1, sistem kekebalan tubuh menyerang 
            sel-sel penghasil insulin di pankreas (sel beta), yang menyebabkan tubuh tidak 
            bisa memproduksi insulin. 
            """)

        with st.expander("🟢 Pengobatan"):
            st.markdown("""
            - **Insulin** – Pengobatan utama untuk diabetes tipe 1.
            - **Menghitung Karbohidrat** – Membantu mengelola kadar gula darah.
            - **Aktivitas Fisik** – Menjaga kebugaran fisik untuk mengelola kadar gula darah. 
            - **Menjaga Berat Badan Sehat** – Mempertahankan berat badan yang sehat.
            - **Kunjungan Kesehatan Rutin** – Pemeriksaan diabetes untuk memantau kondisi Anda.
            """)

        st.divider()
        
        st.markdown('<h3 style="color:#263487;">2. Diabetes Tipe 2</h3>', unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/kayelaisya/TSDN_DiReject/main/tipe%20diabet%20(1).png", width=480)
        st.markdown(
            """
            <p style="text-align: justify; color:#263487; font-size: 18px ;">
                Diabetes tipe 2 terjadi ketika kadar gula darah tinggi akibat tubuh tidak 
                menghasilkan cukup insulin atau insulin yang diproduksi tidak berfungsi dengan 
                baik, yang dikenal sebagai resistensi insulin.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        st.write('')
        
        st.markdown(
            """
            <p style="text-align: justify; color:#263487; font-size: 18px ;">
                Kadar gula darah yang tinggi dalam jangka panjang dapat menyebabkan masalah 
                kesehatan lainnya, seperti serangan jantung, stroke, serta gangguan pada mata, 
                ginjal, dan kaki. Masalah-masalah ini disebut komplikasi diabetes.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        st.write('')
        
        st.markdown(
            """
            <p style="text-align: justify; color:#263487; font-size: 18px ;">
                Pengobatan untuk diabetes tipe 2 meliputi pemeriksaan kesehatan secara rutin 
                serta dukungan untuk aktif bergerak, makan dengan pola makan sehat, dan menjaga 
                berat badan yang sehat. Anda mungkin juga perlu mengonsumsi obat-obatan, termasuk 
                insulin, serta memeriksa kadar gula darah secara teratur.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        st.write('')
        
        st.markdown(
            """
            <p style="text-align: justify; color:#263487; font-size: 18px ;">
                Diabetes tipe 2 bisa tidak terdiagnosis selama bertahun-tahun jika Anda 
                tidak merasakan gejala atau jika gejala Anda terlewatkan.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        st.write('')
        
        st.markdown(
            """
            <p style="text-align: justify; color:#263487; font-size: 18px ;">
                Ada banyak alasan mengapa diabetes tipe 2 dapat berkembang, namun penyakit 
                ini lebih sering terjadi pada orang yang berusia di atas 25 tahun, terutama 
                yang memiliki riwayat keluarga.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        with st.expander("🔴 Gejala"):
            st.markdown("""
            - Sering buang air kecil, terutama pada malam hari.
            - Rasa haus yang terus-menerus.
            - Merasa lebih lelah dari biasanya.
            - Luka dan bekas luka yang memerlukan waktu lebih lama untuk sembuh.
            - Penglihatan kabur.
            """)
            
            st.caption(""" 
            **Catatan**
            - Gejala diabetes tipe 2 dapat berlangsung tanpa terasa atau terabaikan, 
            sehingga seringkali lebih sulit dideteksi dibandingkan diabetes tipe 1.    
            - Pada anak-anak atau remaja (di bawah 18 tahun), gejala ini bisa lebih 
            jelas terlihat, meskipun diabetes tipe 2 pada anak lebih jarang dibandingkan tipe 1.
            - Faktor risiko untuk diabetes tipe 2 pada anak meliputi riwayat keluarga, 
            faktor etnis, dan obesitas atau kelebihan berat badan.   
            """)
            
        with st.expander("🟡 Penyebab"):
            st.markdown("""
            1. **Kurangnya Insulin atau Resistensi Insulin** – Menyebabkan kadar gula darah meningkat.
            2. **Faktor Berat Badan** – Meningkatkan risiko karena tubuh sulit mengelola gula darah, 
            terutama dengan adanya lemak di sekitar hati dan pankreas, bahkan pada orang dengan berat badan normal. 
            3. **Lingkar Pinggang Berlebihan** – Lingkar pinggang yang tinggi dapat meningkatkan risiko 
            resistensi insulin dan diabetes tipe 2. 
            4. **Faktor Risiko Lainnya** – Tekanan Darah Tinggi, Usia, Riwayat Keluarga.
            5. **Kurangnya Aktivitas Fisik** – Tidak aktif secara fisik dapat memperburuk 
            resistensi insulin dan meningkatkan risiko.
            6. **Makanan Berisiko Tinggi** – Minuman manis dan karbohidrat olahan, daging merah dan 
            olahan, serta makanan tinggi garam.
            """)

        with st.expander("🟢 Pengobatan"):
            st.markdown("""
            - **Pola Makan Sehat dan Aktivitas Fisik** – Mengonsumsi makanan sehat dan meningkatkan 
            aktivitas fisik secara teratur.
            - **Penurunan Berat Badan** – Penurunan berat badan membantu menurunkan kadar gula darah.
            - **Pengelolaan Kesehatan Emosional** – Mendukung kesehatan emosional untuk membantu 
            mengelola stres yang dapat memengaruhi kontrol gula darah.
            """)
            
    with tab3:
        st.markdown('<h1 style="color:#263487;">Gejala yang Perlu Diwaspadai</h1>', unsafe_allow_html=True)
        st.markdown("""
            <ul style="font-size:18px; color:#263487;">
                <li><b>Sering Buang Air Kecil</b> - terutama pada malam hari.</li>
                <li><b>Sering Haus</b> - merasa sangat haus, lebih dari biasanya.</li>
                <li><b>Kelelahan</b> - mudah lelah atau merasa lelah secara berlebihan.</li>
                <li><b>Penurunan Berat Badan</b> - kehilangan berat badan tanpa sebab yang jelas.</li>
                <li><b>Luka yang Lama Sembuh</b> - luka atau goresan yang memerlukan waktu lebih lama untuk sembuh.</li>
                <li><b>Penglihatan Kabur</b> - pandangan menjadi buram.</li>
                <li><b>Rasa Lapar yang Meningkat</b> - merasa lebih sering lapar.</li>
            </ul>
            """, unsafe_allow_html=True)
        
        st.markdown(
            """
            <p style="text-align: justify; color:#263487;">
                Ada banyak alasan mengapa diabetes tipe 2 dapat berkembang, namun penyakit 
                ini lebih sering terjadi pada orang yang berusia di atas 25 tahun, terutama 
                yang memiliki riwayat keluarga.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        st.write('')
        
        st.markdown('<h3 style="color:#263487;">Apa yang Terjadi Ketika Diabetes Tidak Terdiagnosis?</h3>', unsafe_allow_html=True)
        st.markdown(
            """
            <p style="text-align: justify; color:#263487; ">
                Beberapa orang merasa sangat lelah, haus, atau sering buang air kecil sebelum 
                akhirnya didiagnosis diabetes. Tingginya kadar glukosa dalam darah yang tidak 
                digunakan tubuh sebagai sumber energi dapat menyebabkan gejala-gejala ini.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        st.write('')
        
        st.markdown('<h3 style="color:#263487;">Kapan Harus Menghubungi Dokter?</h3>', unsafe_allow_html=True)
        st.markdown(
            """
            <ul style="font-size:18px; color:#263487;">
                <li>Anda atau anak Anda mengalami gejala diabetes.</li>
                <li>Anda yakin atau anak Anda berisiko tinggi mengalami diabetes.</li>
            </ul>
            """,
            unsafe_allow_html=True
        )
        
        st.write('')
        
        st.markdown('<h3 style="color:#263487;">Faktor Risiko Diabetes</h3>', unsafe_allow_html=True)
        st.markdown(
            """
            <p style="text-align: justify; color:#263487; ">
                Beberapa orang memiliki risiko lebih tinggi terkena diabetes karena faktor-
                faktor tertentu seperti etnis, genetik, atau pilihan gaya hidup. Memahami 
                faktor risiko ini dapat membantu Anda mengambil langkah yang tepat untuk 
                mengurangi risiko tersebut.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <p style="text-align: justify; color:#263487; ">
                Pastikan untuk menjaga kesehatan dan perhatikan gejala-gejala yang mungkin 
                muncul, serta konsultasikan dengan dokter untuk pemeriksaan lebih lanjut 
                jika diperlukan.
            </p>
            """,
            unsafe_allow_html=True
        )

elif selected == "Cek Diabetes":
    st.markdown('<h1 style="color:#263487;">Cek Risiko Diabetes Anda</h1>', unsafe_allow_html=True)

    input_method = st.selectbox("Pilih metode input:", ["Masukkan Data Manual", "Unggah File Excel"])

    if input_method == "Masukkan Data Manual":
        st.subheader("Masukkan Data Anda")
        jenis_kelamin = st.radio(
            "1. Jenis Kelamin",
            ["Laki-laki", "Perempuan"],
            index=None,
        )
        
        usia = st.selectbox(
            "2. Usia",
            ["18 hingga 24 tahun",
                "25 hingga 29 tahun",
                "30 hingga 34 tahun",
                "35 hingga 39 tahun",
                "40 hingga 44 tahun",
                "45 hingga 49 tahun",
                "50 hingga 54 tahun",
                "55 hingga 59 tahun",
                "60 hingga 64 tahun",
                "65 hingga 69 tahun",
                "70 hingga 74 tahun",
                "75 hingga 79 tahun",
                "80 tahun ke atas"
            ],
            index=None
        )
        
        tinggi_badan = st.number_input(
            "3. Tinggi Badan (cm)"
        )
        
        berat_badan = st.number_input(
            "4. Berat Badan (Kg)"
        )
        
        tekanan_darah = st.radio(
            "5. Tekanan Darah",
            ["Rendah", "Tinggi"],
            index=None
        )
        
        kolesterol = st.radio(
            "6. Kolesterol",
            ["Rendah", "Tinggi"],
            index=None
        )
        
        cek_kolesterol = st.radio(
            "7. Apakah pasien pernah periksa kolesterol dalam 5 tahun terakhir?",
            ["Ya", "Tidak"],
            index=None,
        )
        
        merokok = st.radio(
            "8. Apakah pasien pernah merokok setidaknya 100 batang dalam hidupnya?",
            ["Ya", "Tidak"],
            index=None,
        )
        
        aktif = st.radio(
            "9. Apakah pasien aktif beraktivitas fisik di luar pekerjaan dalam 30 hari terakhir?",
            ["Ya", "Tidak"],
            index=None,
        )
        
        alkohol = st.radio(
            "10. Apakah pasien mengkonsumsi lebih dari 14 Alkohol per minggu (Pria) atau lebih dari 7 Alkohol per minggu (Wanita)?",
            ["Ya", "Tidak"],
            index=None,
        )
        
        dokter = st.radio(
            "11. Dalam 12 bulan terakhir, apakah pernah perlu ke dokter tapi tidak bisa karena biaya?",
            ["Ya", "Tidak"],
            index=None
        )
        
        kesehatan = st.radio(
            "12. Bagaimana kondisi kesehatan umum pasien?",
            options=[
                "Sempurna",
                "Sangat Baik",
                "Baik",
                "Cukup",
                "Buruk"
            ],
            index=None
        )

        kesehatan_mental = st.number_input(
            "13. Dalam 30 hari terakhir, berapa hari kesehatan mental pasien tidak baik?",
            min_value=0,
            step=1,
            format="%d"
        )
        
        kesehatan_fisik = st.number_input(
            "14. Dalam 30 hari terakhir, berapa hari kesehatan fisik pasien tidak baik?",
            min_value=0,
            step=1,
            format="%d"
        )
        
        stroke = st.radio(
            "15. Apakah pernah terkena stroke?",
            ["Ya", "Tidak"],
            index=None
        )
        
        jantung = st.radio(
            "16. Apakah memiliki riwayat  penyakit jantung koroner (PJK) atau infark miokard (MI)?",
            ["Ya", "Tidak"],
            index=None
        )
        
        berjalan = st.radio(
            "17. Apakah pasien kesulitan berjalan atau menaiki tangga?",
            ["Ya", "Tidak"],
            index=None
        )
        
        url = "https://raw.githubusercontent.com/kayelaisya/TSDN_DiReject/main/nb_tsdn.pkl"
        local_filename = "nb_tsdn.pkl"
        
        # Periksa apakah file sudah diunduh
        if not os.path.exists(local_filename):
            try:
                # Unduh file dari URL
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Periksa jika ada error HTTP
                with open(local_filename, 'wb') as f:
                    f.write(response.content)
                print("File model berhasil diunduh.")
            except requests.exceptions.RequestException as e:
                print(f"Gagal mengunduh file model: {e}")
                raise
        
        # Muat model
        model = joblib.load(local_filename)

        
        if st.button("Prediksi Risiko Diabetes"):
                    df_input = preprocess_inputs(jenis_kelamin, usia, tinggi_badan, berat_badan, tekanan_darah, kolesterol,
                                                cek_kolesterol, merokok, aktif, alkohol, dokter, kesehatan,
                                                kesehatan_mental, kesehatan_fisik, stroke, jantung, berjalan)
                    
                    prediction = model.predict(df_input)
                    
                    if prediction[0] == 0:
                        st.success("Hasil Prediksi: Tidak Mengidap Diabetes")
                    else:
                        st.warning("Hasil Prediksi: Prediabetes atau Diabetes")

    elif input_method == "Unggah File Excel":
        st.write("Contoh format file Excel yang dapat diunggah:")
        sample_df = pd.DataFrame({
                "Jenis Kelamin": ["Pria", "Wanita", "Pria"],
                "Usia": [50, 60, 70],
                "Tinggi Badan": [150, 160, 170],
                "Berat Badan": [60, 70, 80],
                "Tekanan Darah": ["Ya", "Tidak", "Tidak"],
                "Kolesterol": ["Ya", "Tidak", "Tidak"],
                "Pernah Periksa Kolesterol": ["Ya", "Tidak", "Tidak"],
                "Pernah Merokok": ["Ya", "Tidak", "Tidak"],
                "Aktivitas Fisik": ["Ya", "Tidak", "Tidak"],
                "Konsumsi Alkohol": ["Ya", "Tidak", "Tidak"],
                "Tidak Ke Dokter": ["Ya", "Tidak", "Tidak"],
                "Kondisi Kesehatan": ["Sempurna", "Sangat Baik", "Baik"],
                "Kesehatan Mental": [3, 5, 7],
                "Kesehatan Fisik": [3, 5, 7],
                "Pernah Stroke": ["Ya", "Tidak", "Tidak"],
                "Penyakit Jantung": ["Ya", "Tidak", "Tidak"],
                "Kesulitan Berjalan": ["Ya", "Tidak", "Tidak"]
            })
        
        st.write(sample_df)

        url = "https://raw.githubusercontent.com/kayelaisya/TSDN_DiReject/main/nb_tsdn.pkl"
        local_filename = "nb_tsdn.pkl"
        
        # Periksa apakah file sudah diunduh
        if not os.path.exists(local_filename):
            try:
                # Unduh file dari URL
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Periksa jika ada error HTTP
                with open(local_filename, 'wb') as f:
                    f.write(response.content)
                print("File model berhasil diunduh.")
            except requests.exceptions.RequestException as e:
                print(f"Gagal mengunduh file model: {e}")
                raise
        
        # Muat model
        model = joblib.load(local_filename)

        uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx"])
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            predictions = [] 
            
            for _, row in df.iterrows():
                df_input = preprocess_inputs(
                    row['Jenis Kelamin'], row['Usia'], row['Tinggi Badan'], row['Berat Badan'],
                    row['Tekanan Darah'], row['Kolesterol'], row['Pernah Periksa Kolesterol'],
                    row['Pernah Merokok'], row['Aktivitas Fisik'], row['Konsumsi Alkohol'],
                    row['Tidak Ke Dokter'], row['Kondisi Kesehatan'], row['Kesehatan Mental'],
                    row['Kesehatan Fisik'], row['Pernah Stroke'], row['Penyakit Jantung'],
                    row['Kesulitan Berjalan']
                )
                
                prediction = model.predict(df_input)
                result = "Tidak Mengidap Diabetes" if prediction[0] == 0 else "Prediabetes atau Diabetes"
                
                predictions.append(result)
            
            df['Prediksi'] = predictions
            
            st.write("Data dengan Hasil Prediksi:")
            st.dataframe(df)
