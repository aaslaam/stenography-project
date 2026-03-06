import os
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image

class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STEGO-PRO // NEON")
        self.root.geometry("600x500")
        self.root.configure(bg="#0f172a")

 
        self.colors = {"bg": "#0f172a", "card": "#1e293b", "accent": "#22d3ee", "success": "#4ade80", "text": "#f8fafc"}
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=self.colors["card"], foreground=self.colors["text"], padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", self.colors["accent"])], foreground=[("selected", "#000000")])
        style.configure("TFrame", background=self.colors["bg"])

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=1, fill="both", padx=10, pady=10)

        self.hide_tab = ttk.Frame(self.tabs)
        self.extract_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.hide_tab, text="  HIDE MESSAGE  ")
        self.tabs.add(self.extract_tab, text="  EXTRACT MESSAGE  ")

        self.build_hide_ui()
        self.build_extract_ui()

    def browse_file(self, var_target):
        fn = filedialog.askopenfilename(filetypes=[("Images", "*.png *.bmp")])
        if fn: var_target.set(fn)

    def handle_drop(self, event, var_target):
       
        path = event.data.strip('{}')
        var_target.set(path)

    def build_hide_ui(self):
        container = tk.Frame(self.hide_tab, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(container, text="IMAGE PATH (DRAG & DROP HERE)", bg=self.colors["bg"], fg=self.colors["accent"], font=("Consolas", 10, "bold")).pack(anchor="w")
        
        self.hide_path = tk.StringVar()
        f_frame = tk.Frame(container, bg=self.colors["bg"])
        f_frame.pack(fill="x", pady=5)
        
       
        h_ent = tk.Entry(f_frame, textvariable=self.hide_path, bg=self.colors["card"], fg=self.colors["text"], relief="flat", font=("Consolas", 10))
        h_ent.pack(side="left", expand=True, fill="x", ipady=8, padx=(0, 5))
        
        
        h_ent.drop_target_register(DND_FILES)
        h_ent.dnd_bind('<<Drop>>', lambda e: self.handle_drop(e, self.hide_path))
        
        tk.Button(f_frame, text="BROWSE", command=lambda: self.browse_file(self.hide_path), bg=self.colors["accent"], font=("Consolas", 8, "bold"), relief="flat").pack(side="right")

        tk.Label(container, text="SECRET MESSAGE", bg=self.colors["bg"], fg=self.colors["accent"], font=("Consolas", 10, "bold")).pack(anchor="w", pady=(15, 0))
        self.secret_text = tk.Text(container, height=10, bg=self.colors["card"], fg=self.colors["text"], insertbackground="white", relief="flat", font=("Consolas", 10), padx=10, pady=10)
        self.secret_text.pack(fill="x", pady=5)

        tk.Button(container, text="EMBED & SAVE", bg=self.colors["success"], font=("Consolas", 10, "bold"), relief="flat", pady=12, command=self.run_hide).pack(fill="x", pady=20)

    def build_extract_ui(self):
        container = tk.Frame(self.extract_tab, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(container, text="STEGO IMAGE (DRAG & DROP HERE)", bg=self.colors["bg"], fg=self.colors["accent"], font=("Consolas", 10, "bold")).pack(anchor="w")
        self.ext_path = tk.StringVar()
        e_frame = tk.Frame(container, bg=self.colors["bg"])
        e_frame.pack(fill="x", pady=5)
        
        e_ent = tk.Entry(e_frame, textvariable=self.ext_path, bg=self.colors["card"], fg=self.colors["text"], relief="flat", font=("Consolas", 10))
        e_ent.pack(side="left", expand=True, fill="x", ipady=8, padx=(0, 5))
        
        e_ent.drop_target_register(DND_FILES)
        e_ent.dnd_bind('<<Drop>>', lambda e: self.handle_drop(e, self.ext_path))
        
        tk.Button(e_frame, text="BROWSE", command=lambda: self.browse_file(self.ext_path), bg=self.colors["accent"], font=("Consolas", 8, "bold"), relief="flat").pack(side="right")

        tk.Button(container, text="EXTRACT MESSAGE", bg="#8b5cf6", fg="white", font=("Consolas", 10, "bold"), relief="flat", pady=12, command=self.run_extract).pack(fill="x", pady=15)

        self.extracted_view = tk.Text(container, height=10, bg=self.colors["card"], fg=self.colors["success"], relief="flat", font=("Consolas", 10), state="disabled", padx=10, pady=10)
        self.extracted_view.pack(fill="x", pady=5)

    def run_hide(self):
        path = self.hide_path.get()
        msg = self.secret_text.get("1.0", tk.END).strip()
        if not path or not msg: return
        
        try:
            img = Image.open(path).convert('RGB')
            bin_msg = ''.join([format(ord(i), "08b") for i in msg]) + '1111111111111110'
            pixels = img.load()
            idx = 0
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    if idx < len(bin_msg):
                        r, g, b = pixels[x, y]
                        r = (r & ~1) | int(bin_msg[idx]); idx += 1
                        if idx < len(bin_msg): g = (g & ~1) | int(bin_msg[idx]); idx += 1
                        if idx < len(bin_msg): b = (b & ~1) | int(bin_msg[idx]); idx += 1
                        pixels[x, y] = (r, g, b)
            
            out = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
            if out:
                img.save(out)
                messagebox.showinfo("Success", "Message Hidden.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def run_extract(self):
        path = self.ext_path.get()
        if not path: return
        try:
            img = Image.open(path).convert('RGB')
            pixels = img.load()
            binary = ""
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    r, g, b = pixels[x, y]
                    binary += str(r & 1) + str(g & 1) + str(b & 1)
            
            marker = '1111111111111110'
            if marker in binary:
                clean_bin = binary[:binary.find(marker)]
                msg = "".join([chr(int(clean_bin[i:i+8], 2)) for i in range(0, len(clean_bin), 8)])
                self.extracted_view.config(state="normal")
                self.extracted_view.delete("1.0", tk.END)
                self.extracted_view.insert(tk.END, msg)
                self.extracted_view.config(state="disabled")
            else: messagebox.showwarning("Failed", "No message found.")
        except Exception as e: messagebox.showerror("Error", str(e))

if __name__ == "__main__":
  
    root = TkinterDnD.Tk()
    app = StegoApp(root)
    root.mainloop()
