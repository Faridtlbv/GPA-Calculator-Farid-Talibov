import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# --- FONT QEYDİ (Windows) ---
# Sistemdə mövcud Arial fontundan istifadə
font_path = r"C:\Windows\Fonts\arial.ttf"  # Windows font qovluğu
if not os.path.exists(font_path):
    messagebox.showerror("Xəta", "Arial fontu tapılmadı! Sistemdə Arial mövcud olmalıdır.")
pdfmetrics.registerFont(TTFont("ArialSys", font_path))

# --- STATUS HESABLANMASI ---
def calc_status(entrance, exam):
    final_score = entrance + exam
    if exam < 17:
        return "F (İmtahan balı 17-dən aşağıdır)"
    elif final_score < 51:
        return "F (Ümumi bal 51-dən aşağıdır)"
    elif 91 <= final_score <= 100:
        return "A"
    elif 71 <= final_score <= 90:
        return "B"
    elif 51 <= final_score <= 70:
        return "C"
    else:
        return "F"

# --- DƏRS ƏLAVƏ FUNKSIYASI ---
def add_lesson():
    global lessons
    lesson = entry_lesson.get().strip()

    if not lesson:
        messagebox.showerror("Xəta", "Dərs adını daxil edin!")
        return

    try:
        entrance = float(entry_entrance.get())
        exam = float(entry_exam.get())

        if entrance > 50 or exam > 50:
            messagebox.showerror("Xəta", "Hər iki bal 50-dən çox ola bilməz!")
            return
        if entrance < 0 or exam < 0:
            messagebox.showerror("Xəta", "Bal mənfi ola bilməz!")
            return

        status = calc_status(entrance, exam)
        final_score = entrance + exam

        lessons.append({
            "lesson": lesson,
            "entrance": entrance,
            "exam": exam,
            "final": final_score,
            "status": status
        })

        messagebox.showinfo(
            "Dərs Əlavə Edildi",
            f"Dərs: {lesson}\n"
            f"Giriş Balı: {entrance}\n"
            f"İmtahan Balı: {exam}\n"
            f"Final Balı: {final_score}\n"
            f"Status: {status}"
        )

        text_result.insert(
            tk.END,
            f"{lesson}: Giriş={entrance}, İmtahan={exam}, Final={final_score}, Status={status}\n"
        )

        entry_lesson.delete(0, tk.END)
        entry_entrance.delete(0, tk.END)
        entry_exam.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Xəta", "Zəhmət olmasa düzgün rəqəm daxil edin!")

# --- ORTALAMA HESABLAMA ---
def calc_average():
    if not lessons:
        messagebox.showwarning("Diqqət", "Heç bir dərs əlavə edilməyib!")
        return

    avg = sum([l["final"] for l in lessons]) / len(lessons)
    status = calc_status(0, avg)
    messagebox.showinfo("Ortalama Nəticə", f"Ortalama Bal: {avg:.2f}\nStatus: {status}")

# --- PDF YARATMA (SİSTEM FONTU) ---
def export_to_pdf():
    if not lessons:
        messagebox.showwarning("Diqqət", "PDF üçün məlumat yoxdur!")
        return

    file_name = "GPA_Report.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    c.setFont("ArialSys", 16)
    c.drawString(180, height - 80, "GPA Hesabatı - Made by Farid Talibov")

    c.setFont("ArialSys", 12)
    y = height - 120

    for i, l in enumerate(lessons, 1):
        line = (f"{i}. {l['lesson']}  |  Giriş: {l['entrance']}  |  "
                f"İmtahan: {l['exam']}  |  Final: {l['final']}  |  Status: {l['status']}")
        c.drawString(50, y, line)
        y -= 20
        if y < 60:
            c.showPage()
            c.setFont("ArialSys", 12)
            y = height - 80

    avg = sum([l["final"] for l in lessons]) / len(lessons)
    c.setFont("ArialSys", 12)
    c.drawString(50, y - 30, f"Ortalama Bal: {avg:.2f}")

    c.save()
    messagebox.showinfo("PDF Hazırdır", f"PDF faylı yaradıldı: {file_name}")

# --- SIFIRLA FUNKSIYASI ---
def reset_all():
    global lessons
    lessons.clear()
    text_result.delete("1.0", tk.END)
    messagebox.showinfo("Təmizləndi", "Bütün məlumatlar silindi!")

# --- TKINTER GUI ---
root = tk.Tk()
root.title("🎓 GPA Kalkulyatoru (Sistem Fontu + PDF)")
root.geometry("550x500")
root.resizable(False, False)

lessons = []

lbl_title = tk.Label(root, text="🎓 GPA Kalkulyatoru", font=("Arial", 16, "bold"))
lbl_title.pack(pady=10)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=5)

tk.Label(frame_inputs, text="Dərs Adı:").grid(row=0, column=0, padx=5, pady=5)
entry_lesson = tk.Entry(frame_inputs, width=25)
entry_lesson.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Giriş Balı (50):").grid(row=1, column=0, padx=5, pady=5)
entry_entrance = tk.Entry(frame_inputs, width=25)
entry_entrance.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="İmtahan Balı (50):").grid(row=2, column=0, padx=5, pady=5)
entry_exam = tk.Entry(frame_inputs, width=25)
entry_exam.grid(row=2, column=1, padx=5, pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Dərs Əlavə Et", command=add_lesson, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Ortalama", command=calc_average, bg="#2196F3", fg="white", width=15).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="PDF Yarat", command=export_to_pdf, bg="#9C27B0", fg="white", width=15).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Sıfırla", command=reset_all, bg="#E91E63", fg="white", width=15).grid(row=1, column=1, padx=5, pady=5)

lbl_result = tk.Label(root, text="Əlavə olunmuş dərslər:", font=("Arial", 12, "bold"))
lbl_result.pack()
text_result = tk.Text(root, height=12, width=65)
text_result.pack(pady=5)

root.mainloop()
