import customtkinter as ctk

# Set up the appearance of the application
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FlashcardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CodeAlpha - Flashcard Learning App")
        self.geometry("550x650")
        self.resizable(False, False)
        
        # Sample Initial Flashcards Data
        self.flashcards = [
            {"question": "What is the primary programming language for Android development?", "answer": "Kotlin (and Java)"},
            {"question": "What does RAM stand for?", "answer": "Random Access Memory"},
            {"question": "What is the primary backend language used for automation & AI?", "answer": "Python"},
            {"question": "What AWS service is used to deploy serverless backend logic?", "answer": "AWS Lambda"},
            {"question": "What does GUI stand for?", "answer": "Graphical User Interface"}
        ]
        
        self.current_index = 0
        self.showing_answer = False
        
        self.create_widgets()
        self.update_ui()

    def create_widgets(self):
        # --- TITLE HEADER ---
        self.title_label = ctk.CTkLabel(
            self, text="FLASHCARD LEARNER", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=(20, 10))
        
        # --- FLASHCARD DISPLAY AREA ---
        self.card_frame = ctk.CTkFrame(
            self, width=460, height=220, 
            corner_radius=15, border_width=2, cursor="hand2"
        )
        self.card_frame.pack(pady=15)
        self.card_frame.pack_propagate(False)
        
        self.card_text = ctk.CTkLabel(
            self.card_frame, text="", 
            font=ctk.CTkFont(size=16, weight="normal"), 
            wraplength=400
        )
        self.card_text.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Bind clicking to flip the card
        self.card_frame.bind("<Button-1>", lambda event: self.toggle_answer())
        self.card_text.bind("<Button-1>", lambda event: self.toggle_answer())
        
        # Hint text below the card
        self.hint_label = ctk.CTkLabel(
            self, 
            text="(Click the card to flip it)", 
            font=ctk.CTkFont(size=12, slant="italic"), 
            text_color="gray"
        )
        self.hint_label.pack(pady=(0, 20))
        
        # --- NAVIGATION BUTTONS ---
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(pady=10)
        
        self.prev_btn = ctk.CTkButton(
            self.nav_frame, text="Previous", width=120, 
            command=self.prev_card, font=ctk.CTkFont(size=13, weight="bold")
        )
        self.prev_btn.grid(row=0, column=0, padx=15)
        
        self.card_counter = ctk.CTkLabel(
            self.nav_frame, text="1 / 5", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.card_counter.grid(row=0, column=1, padx=15)
        
        self.next_btn = ctk.CTkButton(
            self.nav_frame, text="Next", width=120, 
            command=self.next_card, font=ctk.CTkFont(size=13, weight="bold")
        )
        self.next_btn.grid(row=0, column=2, padx=15)
        
        # --- MANAGEMENT SECTION ---
        self.manage_frame = ctk.CTkFrame(self, corner_radius=10)
        self.manage_frame.pack(pady=25, padx=40, fill="x")
        
        self.manage_title = ctk.CTkLabel(
            self.manage_frame, text="Deck Manager", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.manage_title.pack(pady=(10, 5))
        
        # Input Fields
        self.q_entry = ctk.CTkEntry(self.manage_frame, placeholder_text="Enter new question...")
        self.q_entry.pack(fill="x", padx=20, pady=5)
        
        self.a_entry = ctk.CTkEntry(self.manage_frame, placeholder_text="Enter answer...")
        self.a_entry.pack(fill="x", padx=20, pady=5)
        
        # Action Buttons
        self.btn_frame = ctk.CTkFrame(self.manage_frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        
        self.add_btn = ctk.CTkButton(
            self.btn_frame, text="Add Card", 
            fg_color="#2ecc71", hover_color="#27ae60", width=130, command=self.add_card
        )
        self.add_btn.grid(row=0, column=0, padx=10)
        
        self.del_btn = ctk.CTkButton(
            self.btn_frame, text="Delete Current", 
            fg_color="#e74c3c", hover_color="#c0392b", width=130, command=self.delete_card
        )
        self.del_btn.grid(row=0, column=1, padx=10)

    def update_ui(self):
        total_cards = len(self.flashcards)
        
        if total_cards == 0:
            self.card_text.configure(text="No cards left in the deck!\nAdd some below.")
            self.card_counter.configure(text="0 / 0")
            self.card_frame.configure(border_color="#3a3a3a")
            return
            
        current_card = self.flashcards[self.current_index]
        self.card_counter.configure(text=f"{self.current_index + 1} / {total_cards}")
        
        if self.showing_answer:
            self.card_text.configure(text=current_card["answer"], text_color="#2ecc71")
            self.card_frame.configure(border_color="#2ecc71")
        else:
            self.card_text.configure(text=current_card["question"], text_color="#ffffff")
            self.card_frame.configure(border_color="#3a3a3a")

    def toggle_answer(self):
        if self.flashcards:
            self.showing_answer = not self.showing_answer
            self.update_ui()

    def next_card(self):
        if self.flashcards:
            self.current_index = (self.current_index + 1) % len(self.flashcards)
            self.showing_answer = False
            self.update_ui()

    def prev_card(self):
        if self.flashcards:
            self.current_index = (self.current_index - 1) % len(self.flashcards)
            self.showing_answer = False
            self.update_ui()

    def add_card(self):
        question = self.q_entry.get().strip()
        answer = self.a_entry.get().strip()
        
        if question and answer:
            self.flashcards.append({"question": question, "answer": answer})
            self.current_index = len(self.flashcards) - 1
            self.showing_answer = False
            
            self.q_entry.delete(0, 'end')
            self.a_entry.delete(0, 'end')
            self.update_ui()

    def delete_card(self):
        if self.flashcards:
            self.flashcards.pop(self.current_index)
            
            if self.current_index >= len(self.flashcards) and self.flashcards:
                self.current_index = len(self.flashcards) - 1
            elif not self.flashcards:
                self.current_index = 0
                
            self.showing_answer = False
            self.update_ui()

if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()
