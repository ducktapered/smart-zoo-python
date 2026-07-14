from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
import os

app = FastAPI()

# Hubungkan folder static dan templates agar bisa dibaca oleh Python
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)

app.mount("/static", StaticFiles(directory=os.path.join(project_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(project_dir, "templates"))

# DATABASE 30 HEWAN (Dipersempit 5 contoh untuk efisiensi kode, kamu bisa teruskan hingga 30)
database_hewan = [
    {
        "id": "anjing", "nama": "Anjing",
        "deskripsi": [
            "Aku adalah hewan penjaga rumah yang setia. Aku suka menggonggong.",
            "Manusia memanggilku sahabat terbaik mereka. Aku suka mengejar bola.",
            "Aku memiliki indra penciuman yang tajam dan suka mengibaskan ekorku saat senang.",
            "Makanan kesukaanku adalah tulang, dan suaraku terdengar seperti Guk Guk!",
            "Aku berkaki empat, berbulu, dan bisa dilatih untuk membantu polisi."
        ]
    },
    {
        "id": "kucing", "nama": "Kucing",
        "deskripsi": [
            "Aku suka mengejar tikus dan mengeong saat aku lapar.",
            "Hewan berkaki empat yang suka menjilati buluku sendiri agar bersih.",
            "Aku memiliki kumis dan cakar yang tajam, suaraku adalah Meong!",
            "Aku suka sekali memakan ikan dan tidur melingkar di tempat yang hangat.",
            "Hewan peliharaan yang sangat manja dan suka dielus bagian kepalanya."
        ]
    },
    {
        "id": "gajah", "nama": "Gajah",
        "deskripsi": [
            "Aku adalah hewan darat paling besar yang memiliki belalai panjang.",
            "Aku memiliki telinga yang lebar mirip seperti kipas besar.",
            "Badanku sangat besar, dan aku memiliki dua gading berwarna putih.",
            "Aku suka makan rumput serta buah-buahan, dan berjalan bersama rombonganku.",
            "Meskipun badanku sangat berat, aku adalah perenang yang cukup handal."
        ]
    },
    {
        "id": "singa", "nama": "Singa",
        "deskripsi": [
            "Aku dijuluki sebagai Raja Hutan karena penampilanku yang gagah.",
            "Hewan pemakan daging yang memiliki rambut lebat di sekitar leherku.",
            "Suara aumanku sangat keras hingga bisa terdengar dari jarak jauh.",
            "Aku termasuk dalam keluarga kucing besar yang hidup berkelompok di sabana.",
            "Aku berburu bersama kawanku untuk mencari makan di padang rumput."
        ]
    },
    {
        "id": "monyet", "nama": "Monyet",
        "deskripsi": [
            "Aku suka sekali memanjat pohon dan bergelantungan menggunakan ekorku.",
            "Makanan favoritku adalah buah pisang yang berwarna kuning.",
            "Aku hewan yang sangat lincah, cerdas, dan suaraku terdengar seperti Uu-aa-aa!",
            "Wajahku sekilas mirip manusia, dan aku suka hidup berkelompok di hutan.",
            "Aku sering menggaruk kepalaku saat sedang bingung atau bermain."
        ]
    },
    {
        "id": "jerapah", "nama": "Jerapah",
        "deskripsi": [
            "Saya adalah hewan darat tertinggi dengan leher yang sangat panjang untuk menjangkau daun pohon tinggi.",
            "Saya bisa mencapai ketinggian hingga 5-6 meter. Saya hidup di padang rumput Afrika.",
            "Saya memiliki lidah yang panjang hingga 50 cm untuk mengambil daun dari pohon akasia.",
            "Saya adalah hewan yang sangat tenang dan damai. Saya hanya makan tumbuhan dan tidak pernah menyerang."
        ]
    },
    {
        "id": "harimau", "nama": "Harimau",
        "deskripsi": [
            "Saya adalah kucing besar dengan garis-garis oranye dan hitam yang indah. Saya adalah predator yang sangat kuat!",
            "Saya hidup di hutan hujan Asia Tenggara. Saya adalah perenang yang sangat mahir.",
            "Saya memiliki gigi taring yang tajam dan cakar yang sangat kuat untuk berburu.",
            "Saya adalah pemburu malam hari yang sangat gesit. Saya bisa melompat hingga 10 meter!",
            "Saya adalah hewan yang soliter dan territorial. Saya sangat berbahaya bagi mangsa saya."
        ]
    }
    # ... Tambahkan 25 hewan lainnya dengan pola yang sama di sini
]

# Rute 1: Menampilkan halaman utama web saat diakses
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rute 2: API Python untuk mengacak dan membuat soal baru
@app.get("/api/baru")
async def ambil_soal_baru(jumlah_pilihan: int = 4):
    # 1. Pilih hewan jawaban benar
    hewan_benar = random.choice(database_hewan)
    deskripsi_terpilih = random.choice(hewan_benar["deskripsi"])
    
    # 2. Buat daftar pilihan jawaban
    pilihan_jawaban = [hewan_benar]
    sisa_hewan = [h for h in database_hewan if h["id"] != hewan_benar["id"]]
    
    # Ambil opsi salah secara acak sesuai request (2-4 pilihan)
    opsi_salah = random.sample(sisa_hewan, min(jumlah_pilihan - 1, len(sisa_hewan)))
    pilihan_jawaban.extend(opsi_salah)
    
    # Acak posisi jawaban agar tidak ketahuan
    random.shuffle(pilihan_jawaban)
    
    # Kirim data ke frontend berupa JSON
    return {
        "hewan_id_benar": hewan_benar["id"],
        "soal_deskripsi": deskripsi_terpilih,
        "opsi_gambar": [{"id": h["id"], "nama": h["nama"]} for h in pilihan_jawaban]
    }