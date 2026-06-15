import customtkinter as ctk
from PIL import Image

# Configuration de base
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class KalyxUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Fenêtre principale
        self.title("Kalyx")
        self.geometry("1200x700")
        self.configure(fg_color="#1a1a1a")  # Fond exact de l'image

        # Configuration du layout (Grid)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- BARRE LATÉRALE (SIDEBAR) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#121212", border_width=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        # Logo / Titre
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="K  Kalyx", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="w")

        # Boutons d'actions
        self.new_chat_btn = ctk.CTkButton(self.sidebar_frame, text="+ Nouvelle discussion", fg_color="#252525", hover_color="#333", corner_radius=10)
        self.new_chat_btn.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

        self.notebook_btn = ctk.CTkButton(self.sidebar_frame, text="📓 Nouveau notebook", fg_color="#252525", hover_color="#333", corner_radius=10)
        self.notebook_btn.grid(row=2, column=0, padx=15, pady=5, sticky="ew")

        # Section Récents
        self.recent_label = ctk.CTkLabel(self.sidebar_frame, text="Récents", font=ctk.CTkFont(size=12), text_color="gray")
        self.recent_label.grid(row=3, column=0, padx=20, pady=(20, 5), sticky="w")

        self.hist1 = ctk.CTkButton(self.sidebar_frame, text="• achat casquettes", fg_color="transparent", hover_color="#252525", anchor="w")
        self.hist1.grid(row=4, column=0, padx=15, pady=2, sticky="ew")

        self.hist2 = ctk.CTkButton(self.sidebar_frame, text="• bonjour", fg_color="transparent", hover_color="#252525", anchor="w")
        self.hist2.grid(row=5, column=0, padx=15, pady=2, sticky="ew")

        # --- ZONE PRINCIPALE ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew")
        
        # Barre d'outils haut (Share, Star, etc.)
        self.top_tools = ctk.CTkLabel(self.main_content, text="Share  ☆  ✎  ⋮", font=ctk.CTkFont(size=14), text_color="gray")
        self.top_tools.place(relx=0.95, rely=0.05, anchor="ne")

        # Titre central
        self.center_label = ctk.CTkLabel(self.main_content, text="De nouvelles idées à explorer ?", 
                                         font=ctk.CTkFont(size=32, weight="normal"), text_color="white")
        self.center_label.place(relx=0.5, rely=0.4, anchor="center")

        # --- BARRE DE SAISIE (INPUT BAR) ---
        self.input_container = ctk.CTkFrame(self.main_content, fg_color="#262626", corner_radius=25, height=60)
        self.input_container.place(relx=0.5, rely=0.85, relwidth=0.7, anchor="center")

        self.plus_btn = ctk.CTkButton(self.input_container, text="+", width=30, fg_color="transparent", font=("Arial", 20))
        self.plus_btn.place(x=15, rely=0.5, anchor="w")

        self.entry = ctk.CTkEntry(self.input_container, placeholder_text="Demander à Kalyx", 
                                  fg_color="transparent", border_width=0, font=ctk.CTkFont(size=16))
        self.entry.place(x=50, rely=0.5, relwidth=0.7, anchor="w")

        self.flash_btn = ctk.CTkButton(self.input_container, text="Flash ⌵", width=60, fg_color="transparent", text_color="gray")
        self.flash_btn.place(relx=0.85, rely=0.5, anchor="center")

        self.mic_btn = ctk.CTkLabel(self.input_container, text="🎤", font=("Arial", 18))
        self.mic_btn.place(relx=0.95, rely=0.5, anchor="center")

        # Icône étincelle à droite
        self.sparkle = ctk.CTkLabel(self.main_content, text="✦", font=("Arial", 40), text_color="#444")
        self.sparkle.place(relx=0.88, rely=0.85, anchor="center")

if __name__ == "__main__":
    app = KalyxUI()
    app.mainloop()
