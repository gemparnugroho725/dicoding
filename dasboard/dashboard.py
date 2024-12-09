import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚴‍♂️",
    layout="wide"
)

@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    return day_df, hour_df

day_df, hour_df = load_data()

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    #==========Judul Dashboard==========
    st.title("🚴‍♂️ Bike Sharing Dashboard")
    st.markdown("""
    Dashboard ini memberikan gambaran mengenai pola penyewaan sepeda berdasarkan waktu, musim, cuaca, dan kategori lainnya.
    """)

    st.sidebar.title("🔧 Filter Data")
    season_filter = st.sidebar.multiselect("Pilih Musim:", ["Spring", "Summer", "Fall", "Winter"], default=["Spring", "Summer", "Fall", "Winter"])
    weather_filter = st.sidebar.multiselect("Pilih Cuaca:", ["Clear", "Mist", "Light Snow/Rain", "Heavy Rain"], default=["Clear", "Mist", "Light Snow/Rain", "Heavy Rain"])

    filtered_data = hour_df[hour_df["season"].isin([{"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}[season] for season in season_filter])]
    filtered_data = filtered_data[filtered_data["weathersit"].isin([{"Clear": 1, "Mist": 2, "Light Snow/Rain": 3, "Heavy Rain": 4}[weather] for weather in weather_filter])]

    avg_rentals_weather_season = hour_df.groupby(["mnth", "season", "weathersit"], observed=False).agg({
        "cnt": "mean"
    }).reset_index()

    avg_rentals_weather_season["mnth"] = avg_rentals_weather_season["mnth"].astype("category")

    avg_rentals_weather_season["mnth"] = avg_rentals_weather_season["mnth"].cat.rename_categories({
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
    })

    pivot_table = avg_rentals_weather_season.pivot_table(
        values="cnt", 
        index=["mnth"], 
        columns=["season", "weathersit"], 
        aggfunc="mean", 
        observed=False  
    )

    weather_rentals = hour_df.groupby("weathersit", observed=False)["cnt"].mean()
    hourly_rentals = hour_df.groupby("hr")["cnt"].mean().reset_index()
    holiday_rentals = hour_df.groupby("holiday", observed=False)["cnt"].mean().reset_index()


    #==========Navigasi Tab==========
    tab1, tab2, tab3, tab4 = st.tabs(["📑 Analisis", "📋 Kesimpulan",  "📊 Ringkasan data", "📈 Visualisasi" ])

with tab1:
    st.title("Penyewaan Sepeda Berdasarkan Musim dan Cuaca")

    st.subheader("1. Pola Musiman Penyewaan Sepeda:")
    st.markdown("""
    **1.1. Pola Musiman Penyewaan Sepeda:**

    - **Spring (Musim Semi):** Penyewaan sepeda pada musim semi menunjukkan kecenderungan meningkat pada bulan Maret hingga Mei, dengan rata-rata penyewaan tertinggi tercatat pada bulan Maret (149.7 penyewaan) dan sedikit menurun di bulan April dan Mei. Pada bulan-bulan lainnya, data penyewaan tidak tersedia.
    
    - **Summer (Musim Panas):** Pada musim panas, data penyewaan terlihat lebih konsisten, dengan rata-rata penyewaan tinggi pada bulan Juni hingga Agustus, terutama di bulan Juni dan Juli yang mencatatkan angka sekitar 240 penyewaan. Hal ini menunjukkan bahwa musim panas adalah periode dengan jumlah penyewaan sepeda yang tinggi.
    
    - **Fall (Musim Gugur):** Musim gugur menunjukkan penyewaan sepeda yang relatif stabil pada bulan Juni hingga September, dengan angka penyewaan mencapai sekitar 240-238 sepeda per hari pada bulan-bulan tersebut. Namun, data untuk bulan lainnya tidak tersedia, yang mungkin mencerminkan pengurangan penyewaan pada bulan-bulan lainnya.
    
    - **Winter (Musim Dingin):** Pada musim dingin, penyewaan sepeda menunjukkan angka yang lebih rendah, dengan puncaknya tercatat pada bulan September (251.0 penyewaan), yang kemudian menurun pada bulan Oktober hingga Desember, dengan rata-rata sekitar 175-222 penyewaan sepeda. Ini menunjukkan bahwa meskipun musim dingin memiliki penyewaan sepeda yang lebih rendah dibandingkan musim lainnya, beberapa bulan seperti September tetap menunjukkan angka tinggi.

    **1.2. Tren Bulanan:**
    - **Bulan dengan Penyewaan Tertinggi:** Penyewaan sepeda cenderung lebih tinggi pada bulan-bulan musim panas (Juni dan Juli) serta beberapa bulan musim gugur seperti September.
    - **Bulan dengan Penyewaan Terendah:** Penyewaan sepeda sangat rendah pada bulan-bulan musim semi dan musim dingin, terutama pada bulan-bulan yang tidak tercatat dalam data.

    **1.3. Pengaruh Musim Terhadap Penyewaan:**
    - Penyewaan sepeda secara umum lebih tinggi pada musim panas dan gugur, yang merupakan periode cuaca lebih hangat dan lebih kondusif untuk beraktivitas luar ruangan.
    - Pada musim dingin, meskipun masih ada beberapa penyewaan, angka tersebut lebih rendah, mengindikasikan bahwa cuaca dingin mengurangi minat orang untuk menyewa sepeda.
    - Musim semi menunjukkan fluktuasi yang lebih besar, dengan bulan-bulan tertentu yang menunjukkan penyewaan tinggi (Maret), namun berkurang di bulan-bulan lainnya.
    """)

    st.subheader("2. Pengaruh Cuaca terhadap Penyewaan Sepeda:")
    st.markdown("""
    **2.1 Pengaruh Cuaca terhadap Penyewaan Sepeda:**

    - **Cuaca Jernih (Weathersit 1):** Secara umum, cuaca jernih (weathersit 1) cenderung memiliki jumlah penyewaan sepeda tertinggi dibandingkan kategori cuaca lainnya. Penyewaan tertinggi tercatat pada bulan September (271.95 penyewaan), diikuti oleh bulan Juni (250.86 penyewaan), dan Agustus (237.89 penyewaan). Hal ini menunjukkan bahwa cuaca cerah sangat mendukung penyewaan sepeda yang lebih tinggi, terutama di bulan-bulan musim panas dan awal musim gugur.

    - **Cuaca Kabut (Weathersit 2):** Cuaca kabut (weathersit 2) menunjukkan angka penyewaan yang lebih rendah dibandingkan cuaca cerah, namun masih relatif tinggi. Bulan Agustus mencatatkan penyewaan yang tinggi (249.21 penyewaan), diikuti oleh bulan Juli (224.98 penyewaan) dan Juni (223.48 penyewaan). Penyewaan pada bulan-bulan ini mungkin sedikit terpengaruh oleh kabut, tetapi masih tinggi karena cuaca yang relatif baik.

    - **Hujan Ringan (Weathersit 3):** Cuaca hujan ringan (weathersit 3) menunjukkan angka penyewaan yang lebih rendah dibandingkan dua kategori cuaca di atas. Bulan Agustus masih menunjukkan angka yang lebih tinggi (202.08 penyewaan), tetapi bulan-bulan lainnya, seperti Januari, Februari, dan Maret, memiliki penyewaan yang jauh lebih rendah. Penyewaan sepeda pada cuaca hujan ringan cenderung lebih terbatas.

    - **Hujan Lebat (Weathersit 4):** Pada cuaca hujan lebat (weathersit 4), data tidak tersedia untuk sebagian besar bulan, dan hanya tercatat pada bulan Januari dengan rata-rata 74.33 penyewaan sepeda. Ini mengindikasikan bahwa hujan lebat sangat membatasi minat orang untuk menyewa sepeda, yang sesuai dengan harapan bahwa hujan lebat akan mengurangi aktivitas luar ruangan.

    **2.2 Pola Penyewaan Berdasarkan Bulan:**
    - Bulan dengan penyewaan tertinggi secara umum adalah bulan-bulan dengan cuaca cerah (weathersit 1), seperti September, Juni, dan Agustus, yang biasanya berada di musim panas dan awal musim gugur.
    - Penyewaan terendah biasanya terjadi pada bulan dengan cuaca lebih buruk, seperti Januari, yang menunjukkan lebih banyak penyewaan di cuaca cerah tetapi sangat sedikit saat hujan lebat.

    **2.3 Kesimpulan Umum:**
    - Cuaca cerah (weathersit 1) cenderung mendorong jumlah penyewaan sepeda tertinggi, terutama pada bulan-bulan musim panas dan awal musim gugur, yang menunjukkan bahwa orang lebih cenderung untuk bersepeda ketika cuaca cerah.
    - Cuaca kabut (weathersit 2) masih memberikan penyewaan yang cukup tinggi, meskipun lebih rendah dibandingkan cuaca cerah, namun tetap mendukung aktivitas bersepeda.
    - Cuaca hujan ringan (weathersit 3) menyebabkan penurunan jumlah penyewaan, tetapi tidak terlalu signifikan, dan penyewaan masih dapat terjadi, terutama pada bulan-bulan yang lebih hangat.
    - Cuaca hujan lebat (weathersit 4) sangat membatasi penyewaan sepeda, dengan penyewaan yang hampir tidak terjadi pada kondisi hujan lebat.
    """)

with tab2:
    st.title("Insight Penyewaan Sepeda Berdasarkan Musim dan Cuaca")

    st.subheader("1. Pengaruh Musim terhadap Penyewaan Sepeda")
    st.markdown("""
    - Penyewaan sepeda dipengaruhi oleh faktor musiman, dengan musim panas dan gugur cenderung memiliki angka penyewaan yang lebih tinggi, sedangkan musim dingin dan musim semi menunjukkan angka yang lebih rendah.
    - Musim panas dan gugur (Spring dan Summer) cenderung memiliki jumlah penyewaan tertinggi, terutama dengan cuaca cerah, diikuti oleh musim gugur dan musim semi dengan penurunan sedikit.
    """)

    st.subheader("2. Pengaruh Cuaca terhadap Penyewaan Sepeda")
    st.markdown("""
    - Penyewaan sepeda dipengaruhi secara signifikan oleh kondisi cuaca, dengan cuaca cerah mendorong penyewaan yang lebih tinggi, sedangkan hujan lebat sangat membatasi penyewaan sepeda.
    - Cuaca cerah memiliki pengaruh besar dalam meningkatkan jumlah penyewaan sepeda, dengan beberapa bulan menunjukkan penyewaan tertinggi seperti bulan Juni, Agustus, dan September.
    - Cuaca hujan dan kabut cenderung menurunkan jumlah penyewaan sepeda, tetapi masih dapat terjadi, terutama pada bulan-bulan yang lebih hangat.
    - Cuaca hujan lebat mengurangi jumlah penyewaan secara drastis, menunjukkan bahwa penyewaan sepeda sangat terpengaruh oleh kondisi cuaca yang ekstrem.
    """)

with tab3:
    col1, col2, col3 = st.columns([1, 8, 1])

    with col2:
        st.subheader("Data Overview")
        st.write("**Data dalam format Harian:**")
        st.dataframe(day_df.head())
        st.dataframe(day_df.tail())
        st.write("**Data dalam format Jam:**")
        st.dataframe(filtered_data.head())
        st.dataframe(filtered_data.tail())

        st.write("**Deskripsi Statistik (Data dalam format Harian):**")
        st.dataframe(day_df.describe())

        st.write("**Deskripsi Statistik (Data dalam format Jam):**")
        st.dataframe(filtered_data.describe())

        st.write("**Rata-rata Penyewaan Sepeda per Bulan, Musim, dan Cuaca**")
        st.dataframe(pivot_table)

        st.write("**Korelasi antara Cuaca dan Jumlah Penyewaan Sepeda**")
        st.dataframe(weather_rentals)

        st.write("**Perbedaan Penyewaan Sepeda Berdasarkan Jam**")
        st.dataframe(hourly_rentals)    

        st.write("**Dampak Hari Libur terhadap Penyewaan Sepeda**")
        st.dataframe(holiday_rentals) 

with tab4:

    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.write("### Rata-rata Penyewaan Sepeda per Bulan")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="mnth", y="cnt", data=avg_rentals_weather_season, palette="viridis", ax=ax)
        ax.set_title("Average Bike Rentals per Month", fontsize=12)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Average Rentals (cnt)", fontsize=10)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    #==========Penyewaan Sepeda Berdasarkan Bulan dan Cuaca==========
        st.write("### Penyewaan Sepeda Berdasarkan Bulan dan Cuaca")
        plt.figure(figsize=(16, 8))
        sns.barplot(x="season", y="cnt", hue="weathersit", data=avg_rentals_weather_season, palette="coolwarm")

        plt.title("Average Bike Rentals per Month by Weather", fontsize=16)
        plt.xlabel("Month", fontsize=12)
        plt.ylabel("Average Rentals (cnt)", fontsize=12)
        plt.xticks(rotation=45)  # Rotasi label bulan agar lebih mudah dibaca
        plt.legend(title="Weather Situation", fontsize=10)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt)

#==========Penyewaan Sepeda Berdasarkan Bulan dan Cuaca==========
        st.write("### Penyewaan Sepeda Berdasarkan Bulan dan Cuaca")
        plt.figure(figsize=(16, 8))
        sns.barplot(x="mnth", y="cnt", hue="weathersit", data=avg_rentals_weather_season, palette="coolwarm")

        plt.title("Average Bike Rentals per Month by Weather", fontsize=16)
        plt.xlabel("Month", fontsize=12)
        plt.ylabel("Average Rentals (cnt)", fontsize=12)
        plt.xticks(rotation=45)  
        plt.legend(title="Weather Situation", fontsize=10)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt)

#=========Korelasi antara Cuaca dan Jumlah Penyewaan Sepeda==========
        st.write("### Korelasi antara Cuaca dan Jumlah Penyewaan Sepeda")
        plt.figure(figsize=(4, 4))
        labels = weather_rentals.index
        sizes = weather_rentals.values
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"])
        plt.title("Korelasi antara Cuaca dan Jumlah Penyewaan Sepeda", fontsize=16)
        plt.axis("equal")  
        st.pyplot(plt)

#=========Heat Map==========
        st.write("### Penyewaan Sepeda Berdasarkan Bulan dan Cuaca")
        plt.figure(figsize=(16, 8))
        plt.plot(hourly_rentals["hr"], hourly_rentals["cnt"], marker='o', color="b", linestyle='-', linewidth=2, markersize=6)
        plt.title("Perbedaan Penyewaan Sepeda Berdasarkan Jam", fontsize=16)
        plt.xlabel("Jam", fontsize=12)
        plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
        plt.xticks(hourly_rentals["hr"], rotation=45)
        plt.grid(True)
        st.pyplot(plt)
#=========Heat Map==========
        st.write("### Penyewaan Sepeda Berdasarkan Bulan dan Cuaca")
        plt.figure(figsize=(16, 8))
        plt.bar(holiday_rentals["holiday"].astype(str), holiday_rentals["cnt"], color=["blue", "orange"])
        plt.title("Dampak Hari Libur terhadap Penyewaan Sepeda", fontsize=16)
        plt.xlabel("Hari Libur (0 = Bukan Libur, 1 = Libur)", fontsize=12)
        plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
        plt.xticks([0, 1], ["Bukan Libur", "Libur"], rotation=0)
        plt.grid(True, axis="y", linestyle="--", alpha=0.7)
        st.pyplot(plt)

#=========Heat Map==========
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt=".1f", cbar_kws={'label': 'Average Rentals (cnt)'}, ax=ax)

        ax.set_title("Rata-rata Sewa Sepeda per Bulan Berdasarkan Musim dan Cuaca", fontsize=16)
        ax.set_xlabel("Season and Weather", fontsize=12)
        ax.set_ylabel("Month", fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='y', rotation=0)

        st.write("### Rata-rata Sewa Sepeda per Bulan Berdasarkan Musim dan Cuaca")
        st.pyplot(fig)




st.sidebar.info("Gunakan filter untuk melihat visualisasi berdasarkan musim dan kategori cuaca.")

