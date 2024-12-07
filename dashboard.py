import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚴‍♂️",
    layout="wide"
)

# Fungsi untuk membaca dataset
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    return day_df, hour_df

# Memuat data
day_df, hour_df = load_data()

# Judul dashboard
st.title("🚴‍♂️ Bike Sharing Dashboard")
st.markdown("""
Dashboard ini memberikan gambaran mengenai pola penyewaan sepeda berdasarkan waktu, musim, cuaca, dan kategori lainnya.
""")

# Tab navigasi
tab1, tab2, tab3 = st.tabs(["📊 Data Overview", "📈 Visualizations", "📋 Insights"])

# Tab 1: Data Overview
with tab1:
    st.subheader("Data Overview")
    st.write("**Data Harian:**")
    st.dataframe(day_df.head())
    st.write("**Data Jam-jaman:**")
    st.dataframe(hour_df.head())

    st.write("**Deskripsi Statistik (Data Harian):**")
    st.dataframe(day_df.describe())

    st.write("**Deskripsi Statistik (Data Jam-jaman):**")
    st.dataframe(hour_df.describe())

        # Mengelompokkan data berdasarkan bulan, cuaca, dan musim dengan observed=False
    avg_rentals_weather_season = hour_df.groupby(["mnth", "season", "weathersit"], observed=False).agg({
        "cnt": "mean"
    }).reset_index()

    # Mengonversi kolom 'mnth' ke kategori jika belum
    avg_rentals_weather_season["mnth"] = avg_rentals_weather_season["mnth"].astype("category")

    # Mengganti angka bulan dengan nama bulan menggunakan rename_categories
    avg_rentals_weather_season["mnth"] = avg_rentals_weather_season["mnth"].cat.rename_categories({
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
    })

    # Membuat pivot table dengan 'mnth' sebagai indeks, 'season' dan 'weathersit' sebagai kolom
    pivot_table = avg_rentals_weather_season.pivot_table(
        values="cnt", 
        index=["mnth"], 
        columns=["season", "weathersit"], 
        aggfunc="mean", 
        observed=False
    )

    # Menampilkan tabel di Streamlit
    st.write("### Rata-rata Penyewaan Sepeda Per Bulan Berdasarkan Cuaca dan Musim")
    st.write("Pivot table ini menunjukkan rata-rata jumlah penyewaan sepeda per bulan berdasarkan kategori cuaca dan musim.")
    st.dataframe(pivot_table)  # Menampilkan tabel interaktif


# Tab 2: Visualizations
with tab2:
    st.subheader("Visualizations")

    # Rata-rata penyewaan sepeda per bulan
    monthly_avg_rentals = hour_df.groupby("mnth").agg({"cnt": "mean"}).reset_index()
    monthly_avg_rentals["mnth"] = monthly_avg_rentals["mnth"].astype(str).replace({
        "1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June",
        "7": "July", "8": "August", "9": "September", "10": "October", "11": "November", "12": "December"
    })

    st.write("### Rata-rata Penyewaan Sepeda per Bulan")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="mnth", y="cnt", data=monthly_avg_rentals, palette="viridis", ax=ax)
    ax.set_title("Average Bike Rentals per Month", fontsize=14)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Average Rentals (cnt)", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Penyewaan sepeda berdasarkan musim dan cuaca
    avg_rentals_weather = hour_df.groupby(["season", "weathersit"]).agg({"cnt": "mean"}).reset_index()
    avg_rentals_weather["season"] = avg_rentals_weather["season"].astype(str).replace({
        "1": "Spring", "2": "Summer", "3": "Fall", "4": "Winter"
    })

    st.write("### Penyewaan Sepeda Berdasarkan Musim dan Cuaca")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x="season", y="cnt", hue="weathersit", data=avg_rentals_weather, palette="coolwarm", ax=ax)
    ax.set_title("Average Bike Rentals by Season and Weather", fontsize=14)
    ax.set_xlabel("Season", fontsize=12)
    ax.set_ylabel("Average Rentals (cnt)", fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title="Weather Situation", fontsize=10)
    st.pyplot(fig)

    # Penyewaan sepeda per bulan berdasarkan kategori cuaca
    avg_rentals_weather = hour_df.groupby(["mnth", "weathersit"]).agg({"cnt": "mean"}).reset_index()
    avg_rentals_weather["mnth"] = avg_rentals_weather["mnth"].astype(str).replace({
        "1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June",
        "7": "July", "8": "August", "9": "September", "10": "October", "11": "November", "12": "December"
    })

    # Lebar bar
    bar_width = 0.2

    # Posisi unik untuk setiap kategori cuaca
    categories = avg_rentals_weather["weathersit"].unique()
    positions = range(len(avg_rentals_weather["mnth"].unique()))

    # Membuat figure
    fig, ax = plt.subplots(figsize=(16, 8))

    # Loop melalui setiap kategori cuaca
    for i, category in enumerate(categories):
        category_data = avg_rentals_weather[avg_rentals_weather["weathersit"] == category]
        ax.bar(
            [p + i * bar_width for p in positions], 
            category_data["cnt"], 
            width=bar_width, 
            label=f"Weather {category}"
        )

    # Penyesuaian sumbu X
    ax.set_xticks([p + (len(categories) - 1) * bar_width / 2 for p in positions])
    ax.set_xticklabels(avg_rentals_weather["mnth"].unique(), rotation=45)

    # Menambahkan elemen grafis
    ax.set_title("Average Bike Rentals per Month by Weather", fontsize=16)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Average Rentals (cnt)", fontsize=12)
    ax.legend(title="Weather Situation", fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Menampilkan grafik di Streamlit
    st.write("### Penyewaan Sepeda Bulanan Berdasarkan Cuaca")
    st.pyplot(fig)

    # Membuat heatmap dari pivot table
    fig, ax = plt.subplots(figsize=(16, 8))

    # Visualisasi menggunakan heatmap
    sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt=".1f", cbar_kws={'label': 'Average Rentals (cnt)'}, ax=ax)

    # Menambahkan elemen grafis
    ax.set_title("Average Bike Rentals per Month by Season and Weather", fontsize=16)
    ax.set_xlabel("Season and Weather", fontsize=12)
    ax.set_ylabel("Month", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', rotation=0)

    # Menampilkan heatmap di Streamlit
    st.write("### Heatmap: Average Bike Rentals per Month by Season and Weather")
    st.pyplot(fig)


# Tab 3: Insights
with tab3:
    st.subheader("Insights")
    st.markdown("""
    - **Pola Penyewaan Sepeda:** Bulan-bulan musim panas memiliki jumlah penyewaan tertinggi.
    - **Dampak Cuaca:** Cuaca yang lebih buruk (hujan atau salju) cenderung menurunkan jumlah penyewaan.
    - **Penggunaan Hari Kerja vs Libur:** Penyewaan lebih tinggi pada hari kerja dibandingkan dengan hari libur.
    """)

st.sidebar.title("🔧 Filter Data")
season_filter = st.sidebar.multiselect("Pilih Musim:", ["Spring", "Summer", "Fall", "Winter"], default=["Spring", "Summer"])
weather_filter = st.sidebar.multiselect("Pilih Cuaca:", ["Clear", "Mist", "Light Snow/Rain", "Heavy Rain"], default=["Clear", "Mist"])

st.sidebar.info("Gunakan filter untuk melihat visualisasi berdasarkan musim dan kategori cuaca.")
