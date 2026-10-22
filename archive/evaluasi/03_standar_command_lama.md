# Standar Command Project — Save, Prepare Commit, dan Commit Progres

## Konteks

Percakapan ini membahas perbedaan fungsi command `save`, `prepare commit`, dan `commit progres` dalam proyek **Learn A.I Workflow for Data Science**, serta meluruskan workflow agar ketiganya tidak tumpang tindih.

---

## 1. Perbedaan Command

### `save`

Fungsi resmi:

> Menyimpan historis percakapan yang relevan dan meng-update memori proyek.

`save`:
- menyimpan historis percakapan yang relevan;
- memperbarui memory/state proyek;
- **tidak melakukan commit**;
- **tidak melakukan push ke GitHub**;
- tidak digunakan untuk project-save workflow ke repository.

---

### `prepare commit`

Fungsi resmi:

> **Menyiapkan seluruh isi yang akan di-push oleh command `commit progres`.**

`prepare commit` hanya tahap persiapan.

Yang dilakukan:
1. Mengecek milestone/progres yang sudah tervalidasi.
2. Mencocokkan progres dengan roadmap sebagai single source of truth.
3. Menentukan file repository yang perlu berubah.
4. Menentukan isi perubahan yang relevan.
5. Mengecek konsistensi dokumentasi.
6. Menentukan commit scope.
7. Menyiapkan commit message.
8. Menghasilkan status siap atau belum siap untuk `commit progres`.

`prepare commit`:
- **tidak melakukan commit**;
- **tidak melakukan push**;
- tidak membuat perubahan ke GitHub hanya karena sedang menyiapkan commit.

---

### `commit progres`

Fungsi resmi:

> **Melakukan commit dan push milestone/progres yang sudah tervalidasi berdasarkan hasil `prepare commit`.**

`commit progres`:
- menggunakan scope yang sudah disiapkan;
- memperbarui file repository yang relevan;
- melakukan commit;
- melakukan push ke GitHub.

---

## 2. Workflow Resmi

### Workflow progres → GitHub

```text
Progress tervalidasi
        ↓
prepare commit
        ↓
┌──────────────────────────────┐
│ 1. Cek milestone yang valid  │
│ 2. Cocokkan dengan roadmap   │
│ 3. Tentukan file yang berubah│
│ 4. Tentukan isi perubahan   │
│ 5. Cek konsistensi dokumentasi│
│ 6. Tentukan commit scope     │
│ 7. Siapkan commit message    │
└──────────────────────────────┘
        ↓
   READY TO COMMIT
        ↓
commit progres
        ↓
   Commit + Push
```

### Workflow memory

```text
Percakapan penting
Keputusan desain
Perubahan aturan
State pembelajaran
        ↓
      save
        ↓
Update memory proyek
```

---

## 3. Standar Final

| Command | Fungsi |
|---|---|
| `save` | Simpan historis + update memory proyek |
| `prepare commit` | **Menyiapkan apa yang akan di-push oleh `commit progres`** |
| `commit progres` | **Melakukan commit + push dari hasil `prepare commit`** |

---

## 4. Koreksi Workflow

Dalam percakapan ini ditemukan bahwa penggunaan `save` sebelumnya sempat menjalankan project-save workflow ke GitHub.

Hal tersebut dikoreksi.

Standar terbaru menetapkan bahwa:

> **`save` bukan command untuk GitHub.**

GitHub hanya disentuh oleh workflow `commit progres`, setelah persiapan dilakukan melalui `prepare commit`.

Dengan demikian, ketiga command memiliki batas fungsi yang jelas dan tidak saling tumpang tindih.

---

## 5. Prinsip Utama

`prepare commit` adalah **jembatan antara progres tervalidasi dan `commit progres`**.

Ia menentukan **apa yang akan di-push**, tetapi tidak melakukan push itu sendiri.

`commit progres` adalah tahap eksekusi.

`save` adalah tahap penyimpanan historis dan memory proyek, bukan tahap Git.
