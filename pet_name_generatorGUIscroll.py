import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
from datetime import datetime

class PetNameGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Pet Name Generator")
        self.root.geometry("800x900")
        self.root.configure(bg='#f0f8ff')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables to store pet information
        self.pet_info = {}
        self.generated_names = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(self.root, bg='#f0f8ff')
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f8ff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Title
        title_label = tk.Label(scrollable_frame, text="🐾 Pet Name Generator 🐾", 
                              font=('Arial', 24, 'bold'), bg='#f0f8ff', fg='#2c3e50')
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(scrollable_frame, text="Find the perfect name for your furry friend!", 
                                 font=('Arial', 12), bg='#f0f8ff', fg='#34495e')
        subtitle_label.pack(pady=(0, 30))
        
        # Create all sections in one scrollable form
        self.create_basic_info_section(scrollable_frame)
        self.create_details_section(scrollable_frame)
        self.create_preferences_section(scrollable_frame)
        
        # Generate button
        generate_btn = tk.Button(scrollable_frame, text="🎲 Generate Names", 
                               command=self.generate_names, font=('Arial', 14, 'bold'),
                               bg='#3498db', fg='white', padx=30, pady=10)
        generate_btn.pack(pady=20)
        
        # Results frame
        self.results_frame = tk.Frame(scrollable_frame, bg='#f0f8ff')
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_basic_info_section(self, parent):
        # Basic Info Section
        basic_frame = tk.LabelFrame(parent, text="Basic Information", font=('Arial', 14, 'bold'), 
                                   bg='#f0f8ff', fg='#2c3e50', padx=20, pady=15)
        basic_frame.pack(fill=tk.X, pady=10)
        
        # Pet Type
        tk.Label(basic_frame, text="Pet Type:", font=('Arial', 12, 'bold'), bg='#f0f8ff').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.pet_type_var = tk.StringVar(value="Dog")
        pet_types = ["Dog", "Cat", "Bird", "Fish", "Rabbit", "Hamster", "Reptile", "Other"]
        self.pet_type_combo = ttk.Combobox(basic_frame, textvariable=self.pet_type_var, values=pet_types, state="readonly", width=20)
        self.pet_type_combo.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        # Breed
        tk.Label(basic_frame, text="Breed (optional):", font=('Arial', 12, 'bold'), bg='#f0f8ff').grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.breed_var = tk.StringVar()
        breed_entry = tk.Entry(basic_frame, textvariable=self.breed_var, width=25)
        breed_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        # Gender
        tk.Label(basic_frame, text="Gender:", font=('Arial', 12, 'bold'), bg='#f0f8ff').grid(row=2, column=0, sticky='w', padx=10, pady=10)
        self.gender_var = tk.StringVar(value="Unknown")
        gender_frame = tk.Frame(basic_frame, bg='#f0f8ff')
        gender_frame.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="male", bg='#f0f8ff').pack(side=tk.LEFT)
        tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="female", bg='#f0f8ff').pack(side=tk.LEFT)
        tk.Radiobutton(gender_frame, text="Unknown", variable=self.gender_var, value="unknown", bg='#f0f8ff').pack(side=tk.LEFT)
        
    def create_details_section(self, parent):
        # Details Section
        details_frame = tk.LabelFrame(parent, text="Appearance & Personality", font=('Arial', 14, 'bold'), 
                                     bg='#f0f8ff', fg='#2c3e50', padx=20, pady=15)
        details_frame.pack(fill=tk.X, pady=10)
        
        # Personality traits
        tk.Label(details_frame, text="Personality Traits (select up to 3):", font=('Arial', 12, 'bold'), bg='#f0f8ff').grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=10)
        
        self.personality_vars = {}
        traits = ["Playful", "Calm", "Energetic", "Shy", "Friendly", "Independent", "Curious", "Mischievous"]
        
        personality_frame = tk.Frame(details_frame, bg='#f0f8ff')
        personality_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        for i, trait in enumerate(traits):
            var = tk.BooleanVar()
            self.personality_vars[trait] = var
            cb = tk.Checkbutton(personality_frame, text=trait, variable=var, command=self.limit_personality_selection, bg='#f0f8ff')
            cb.grid(row=i//4, column=i%4, sticky='w', padx=5, pady=2)
        
        # Appearance
        tk.Label(details_frame, text="Color:", font=('Arial', 12, 'bold'), bg='#f0f8ff').grid(row=2, column=0, sticky='w', padx=10, pady=10)
        self.color_var = tk.StringVar()
        color_entry = tk.Entry(details_frame, textvariable=self.color_var, width=25)
        color_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        tk.Label(details_frame, text="Size:", font=('Arial', 12, 'bold'), bg='#f0f8ff').grid(row=3, column=0, sticky='w', padx=10, pady=10)
        self.size_var = tk.StringVar(value="Medium")
        sizes = ["Tiny", "Small", "Medium", "Large", "Extra Large"]
        size_combo = ttk.Combobox(details_frame, textvariable=self.size_var, values=sizes, state="readonly", width=20)
        size_combo.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        tk.Label(details_frame, text="Special Features:", font=('Arial', 12, 'bold'), bg='#f0f8ff').grid(row=4, column=0, sticky='w', padx=10, pady=10)
        self.special_var = tk.StringVar()
        special_entry = tk.Entry(details_frame, textvariable=self.special_var, width=25)
        special_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        
    def create_preferences_section(self, parent):
        # Preferences Section
        prefs_frame = tk.LabelFrame(parent, text="Name Preferences", font=('Arial', 14, 'bold'), 
                                   bg='#f0f8ff', fg='#2c3e50', padx=20, pady=15)
        prefs_frame.pack(fill=tk.X, pady=10)
        
        # Name length
        tk.Label(prefs_frame, text="Preferred Name Length:", font=('Arial', 12, 'bold'), bg='#f0f8ff').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.length_var = tk.StringVar(value="No preference")
        lengths = ["Short (1-4 letters)", "Medium (5-8 letters)", "Long (9+ letters)", "No preference"]
        length_combo = ttk.Combobox(prefs_frame, textvariable=self.length_var, values=lengths, state="readonly", width=25)
        length_combo.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        # Name style
        tk.Label(prefs_frame, text="Name Style:", font=('Arial', 12, 'bold'), bg='#f0f8ff').grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.style_var = tk.StringVar(value="All styles")
        styles = ["Human names", "Food-inspired", "Nature-inspired", "Mythological", "Pop culture", "Funny/Quirky", "All styles"]
        style_combo = ttk.Combobox(prefs_frame, textvariable=self.style_var, values=styles, state="readonly", width=25)
        style_combo.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        # Starting letter
        tk.Label(prefs_frame, text="Starts with letter (optional):", font=('Arial', 12, 'bold'), bg='#f0f8ff').grid(row=2, column=0, sticky='w', padx=10, pady=10)
        self.starts_with_var = tk.StringVar()
        starts_entry = tk.Entry(prefs_frame, textvariable=self.starts_with_var, width=5)
        starts_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
    def limit_personality_selection(self):
        selected = [trait for trait, var in self.personality_vars.items() if var.get()]
        if len(selected) > 3:
            # Find the last selected and deselect it
            for trait, var in self.personality_vars.items():
                if var.get() and trait not in selected[:3]:
                    var.set(False)
                    break
            messagebox.showwarning("Selection Limit", "You can only select up to 3 personality traits.")
    
    def collect_pet_info(self):
        """Collect all pet information from the GUI"""
        # Get selected personality traits
        personality = [trait for trait, var in self.personality_vars.items() if var.get()]
        
        # Get appearance info
        appearance = {
            "color": self.color_var.get(),
            "size": self.size_var.get(),
            "special_feature": self.special_var.get()
        }
        
        # Get preferences
        preferences = {
            "length": self.length_var.get(),
            "style": self.style_var.get(),
            "starts_with": self.starts_with_var.get().upper()
        }
        
        self.pet_info = {
            "type": self.pet_type_var.get(),
            "breed": self.breed_var.get() if self.breed_var.get() else "Unknown",
            "gender": self.gender_var.get(),
            "personality": personality,
            "appearance": appearance,
            "preferences": preferences
        }
    
    def generate_pet_names(self, pet_info):
        """Generate name suggestions based on the pet information."""
        # Name databases by category
        male_names = ["Max", "Charlie", "Cooper", "Buddy", "Oliver", "Leo", "Milo", "Jack", "Toby", "George", "Winston", "Henry", "Sam", "Theodore"]
        female_names = ["Luna", "Bella", "Lucy", "Daisy", "Lily", "Zoe", "Rosie", "Sophie", "Ruby", "Chloe", "Stella", "Emma", "Penny", "Olive"]
        neutral_names = ["Alex", "Riley", "Jordan", "Jamie", "Quinn", "Avery", "Casey", "Morgan", "Taylor", "Dakota", "Reese", "Harper"]

        human_names_combined = male_names + female_names + neutral_names
        food_names = ["Cookie", "Pepper", "Ginger", "Oreo", "Mochi", "Biscuit", "Pretzel", "Peanut", "Waffles", "Mocha", "Kiwi", "Taco", "Nacho", "Pickle", "Bean"]
        nature_names = ["River", "Sky", "Storm", "Willow", "Moss", "Sierra", "Autumn", "Ember", "Aspen", "Blaze", "Frost", "Maple", "Sunny", "Brook", "Iris", "Cedar"]
        mythological_names = ["Zeus", "Apollo", "Athena", "Thor", "Loki", "Odin", "Artemis", "Freya", "Luna", "Phoenix", "Atlas", "Persephone", "Clio", "Gaia", "Orion"]
        pop_culture_names = ["Yoda", "Dobby", "Simba", "Nala", "Elsa", "Groot", "Chewie", "Stitch", "Arya", "Khaleesi", "Groot", "Frodo", "Gizmo", "Neo", "Zelda"]
        quirky_names = ["Pickles", "Bubbles", "Noodle", "Wigglebutt", "Fluffernutter", "Sir Barksalot", "Captain Whiskers", "Professor Purrington", "Señor Snuggles", "Fuzzy Wuzzy", "Tiny", "Tank", "Meatball", "Zoom"]

        # Style mapping
        style_mapping = {
            "Human names": human_names_combined,
            "Food-inspired": food_names,
            "Nature-inspired": nature_names,
            "Mythological": mythological_names,
            "Pop culture": pop_culture_names,
            "Funny/Quirky": quirky_names,
            "All styles": human_names_combined + food_names + nature_names + mythological_names + pop_culture_names + quirky_names
        }

        name_pool = []

        # Handle human names with gender consideration
        if pet_info["preferences"]["style"] == "Human names":
            if pet_info["gender"] == "male":
                name_pool.extend(male_names + neutral_names)
            elif pet_info["gender"] == "female":
                name_pool.extend(female_names + neutral_names)
            else:  # unknown
                name_pool.extend(human_names_combined)
        else:
            name_pool.extend(style_mapping[pet_info["preferences"]["style"]])

        # Filter by first letter if specified
        if pet_info["preferences"]["starts_with"]:
            name_pool = [name for name in name_pool if name.startswith(pet_info["preferences"]["starts_with"])]

        # Filter by length preference
        if pet_info["preferences"]["length"] == "Short (1-4 letters)":
            name_pool = [name for name in name_pool if len(name) <= 4]
        elif pet_info["preferences"]["length"] == "Medium (5-8 letters)":
            name_pool = [name for name in name_pool if 5 <= len(name) <= 8]
        elif pet_info["preferences"]["length"] == "Long (9+ letters)":
            name_pool = [name for name in name_pool if len(name) >= 9]

        # Add personality-based names
        personality_names = {
            "Playful": ["Bounce", "Zippy", "Jet", "Dash", "Pogo"],
            "Calm": ["Zen", "Serene", "Peace", "Gentle", "Harmony"],
            "Energetic": ["Spark", "Flash", "Bolt", "Rocket", "Zoom"],
            "Shy": ["Shadow", "Whisper", "Shy", "Misty", "Ghost"],
            "Friendly": ["Buddy", "Pal", "Joy", "Happy", "Sunny"],
            "Independent": ["Solo", "Rebel", "Rogue", "Maverick", "Lone"],
            "Curious": ["Scout", "Quest", "Sherlock", "Wonder", "Seek"],
            "Mischievous": ["Trouble", "Rascal", "Bandit", "Trickster", "Imp"]
        }
        
        for trait in pet_info["personality"]:
            if trait in personality_names:
                name_pool.extend(personality_names[trait])

        # Add appearance-based names
        color = pet_info["appearance"]["color"].lower()
        if color in ["black", "dark"]:
            name_pool.extend(["Shadow", "Midnight", "Onyx", "Raven", "Jet"])
        elif color in ["white", "cream", "ivory"]:
            name_pool.extend(["Snow", "Pearl", "Cloud", "Ghost", "Frost"])
        elif color in ["orange", "ginger", "red"]:  
            name_pool.extend(["Rusty", "Amber", "Blaze", "Flame", "Copper"])
        elif color in ["grey", "gray", "silver"]:
            name_pool.extend(["Ash", "Silver", "Smoke", "Steel", "Mist"])
        elif color in ["brown", "tan"]:
            name_pool.extend(["Cocoa", "Mocha", "Fudge", "Toffee", "Hazel"])

        # Add size-based names
        size = pet_info["appearance"]["size"].lower()
        if size in ["tiny", "small"]:
            name_pool.extend(["Peanut", "Tiny", "Button", "Pip", "Mini"])
        elif size in ["large", "extra large"]:
            name_pool.extend(["Tank", "Goliath", "Chunk", "Titan", "Colossus"])

        # Remove duplicates and return selection
        name_pool = list(set(name_pool))
        
        if not name_pool:
            return ["Scout", "Buddy", "Luna", "Charlie", "Max"]
        
        random.shuffle(name_pool)
        return name_pool[:min(10, len(name_pool))]
    
    def generate_names(self):
        """Generate and display names"""
        self.collect_pet_info()
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Generate names
        self.generated_names = self.generate_pet_names(self.pet_info)
        
        # Display results
        results_title = tk.Label(self.results_frame, text="🎉 Suggested Names 🎉", 
                               font=('Arial', 16, 'bold'), bg='#f0f8ff', fg='#2c3e50')
        results_title.pack(pady=10)
        
        # Create frame for name buttons
        names_frame = tk.Frame(self.results_frame, bg='#f0f8ff')
        names_frame.pack(pady=10)
        
        # Display names as clickable buttons
        for i, name in enumerate(self.generated_names):
            name_btn = tk.Button(names_frame, text=name, font=('Arial', 12),
                               bg='#e8f4fd', fg='#2c3e50', padx=20, pady=5,
                               command=lambda n=name: self.select_name(n),
                               relief=tk.RAISED, borderwidth=2)
            name_btn.grid(row=i//3, column=i%3, padx=10, pady=5, sticky='ew')
        
        # Configure grid weights for even spacing
        for i in range(3):
            names_frame.grid_columnconfigure(i, weight=1)
        
        # Add buttons
        button_frame = tk.Frame(self.results_frame, bg='#f0f8ff')
        button_frame.pack(pady=15)
        
        more_btn = tk.Button(button_frame, text="🔄 Generate More", 
                           command=self.generate_names, font=('Arial', 10),
                           bg='#95a5a6', fg='white', padx=15, pady=5)
        more_btn.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(button_frame, text="🔄 Reset Form", 
                            command=self.reset_form, font=('Arial', 10),
                            bg='#e74c3c', fg='white', padx=15, pady=5)
        reset_btn.pack(side=tk.LEFT, padx=10)
    
    def select_name(self, name):
        """Handle name selection"""
        result = messagebox.askyesno("Name Selected!", 
                                   f"You selected '{name}'!\n\nWould you like to save this name?")
        
        if result:
            self.save_name(name)
        
        # Ask if they want to generate more names
        another = messagebox.askyesno("Continue?", 
                                    "Would you like to generate names for another pet?")
        if another:
            self.reset_form()
    
    def save_name(self, name):
        """Save the selected name to a file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile="pet_name.txt"
            )
            
            if filename:
                with open(filename, "w") as file:
                    file.write(f"Pet Type: {self.pet_info['type']}\n")
                    if self.pet_info['breed'] != "Unknown":
                        file.write(f"Breed: {self.pet_info['breed']}\n")
                    file.write(f"Pet Name: {name}\n")
                    file.write(f"Date Selected: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write(f"Gender: {self.pet_info['gender'].title()}\n")
                    file.write(f"Personality: {', '.join(self.pet_info['personality'])}\n")
                    file.write(f"Color: {self.pet_info['appearance']['color']}\n")
                    file.write(f"Size: {self.pet_info['appearance']['size']}\n")
                
                messagebox.showinfo("Saved!", f"Pet name saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")
    
    def reset_form(self):
        """Reset all form fields"""
        # Reset basic info
        self.pet_type_var.set("Dog")
        self.breed_var.set("")
        self.gender_var.set("Unknown")
        
        # Reset personality traits
        for var in self.personality_vars.values():
            var.set(False)
        
        # Reset appearance
        self.color_var.set("")
        self.size_var.set("Medium")
        self.special_var.set("")
        
        # Reset preferences
        self.length_var.set("No preference")
        self.style_var.set("All styles")
        self.starts_with_var.set("")
        
        # Clear results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Scroll to top
        canvas = self.root.children['!canvas']
        canvas.yview_moveto(0)

def main():
    root = tk.Tk()
    app = PetNameGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()