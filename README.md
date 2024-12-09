# Bike Rental Analysis Dashboard 🚲📊

## Setup Environment - Anaconda
Jika kamu menggunakan Anaconda, ikuti langkah-langkah berikut untuk menyiapkan lingkungan:

1. **Buat lingkungan conda baru:**
    ```bash
    conda create --name bike-rental-ds python=3.9
    ```

2. **Aktifkan lingkungan yang baru dibuat:**
    ```bash
    conda activate bike-rental-ds
    ```

3. **Install semua dependensi yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

## Setup Environment - Shell/Terminal
Jika kamu lebih suka menggunakan Shell/Terminal tanpa Anaconda, ikuti langkah-langkah ini:

1. **Buat direktori proyek:**
    ```bash
    mkdir bike-rental-analysis
    cd bike-rental-analysis
    ```

2. **Install dependensi menggunakan venv:**
    - Buat environment virtual:
      ```bash
      python -m venv env
      ```
    - Untuk mengaktifkan environment:
      - **Windows:**
        ```bash
        .\env\Scripts\activate
        ```
      - **Linux/Mac:**
        ```bash
        source env/bin/activate
        ```

    - Install dependensi yang diperlukan:
      ```bash
      pip install -r requirements.txt
      ```

## Menjalankan Streamlit App
Setelah lingkungan siap, kamu bisa menjalankan aplikasi Streamlit dengan perintah berikut:
```bash
streamlit run dashboard.py
