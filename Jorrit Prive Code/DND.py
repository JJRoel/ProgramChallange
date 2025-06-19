import tkinter as tk

class CharacterSheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("D&D 5e Character Sheet")

        # Kopbanner (bovenaan) inclusief 2x3 grid
        self.header_frame = tk.Frame(root, borderwidth=2, relief="ridge")
        self.header_frame.pack(fill="x", padx=5, pady=5)

        # Character Name en invoerveld
        tk.Label(self.header_frame, text="Character Name", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, sticky="w")
        self.character_name_entry = tk.Entry(self.header_frame, width=20)
        self.character_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # 2x3 grid voor basisinformatie
        info_labels = ["Class & Level", "Background", "Player Name", "Race", "Alignment", "XP"]
        self.info_entries = {}

        for i, label in enumerate(info_labels):
            row, col = divmod(i, 3)  
            tk.Label(self.header_frame, text=label).grid(row=row+1, column=col*2, padx=10, pady=5, sticky="w")
            entry = tk.Entry(self.header_frame, width=15)
            entry.grid(row=row+1, column=col*2+1, padx=10, pady=5)
            self.info_entries[label] = entry

        # Combat Stats naast elkaar met invoervelden eronder
        self.middle_top_frame = tk.Frame(root, borderwidth=2, relief="ridge")
        self.middle_top_frame.pack(fill="x", padx=5, pady=5)
        
        stats = ["Armor Class", "Initiative", "Speed"]
        self.stat_entries = {}
        
        for i, stat in enumerate(stats):
            tk.Label(self.middle_top_frame, text=stat).grid(row=0, column=i, padx=10, pady=5, sticky="w")
            entry = tk.Entry(self.middle_top_frame, width=10)
            entry.grid(row=1, column=i, padx=10, pady=5)  # Invoervelden direct onder labels
            self.stat_entries[stat] = entry

        # Ability Scores (linkerkolom)
        self.left_frame = tk.Frame(root, borderwidth=2, relief="ridge")
        self.left_frame.pack(side="left", fill="y", padx=5, pady=5)
        tk.Label(self.left_frame, text="Ability Scores", font=("Arial", 12, "bold")).pack()
        
        abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        self.ability_entries = {}
        for ability in abilities:
            row = tk.Frame(self.left_frame)
            row.pack(fill="x")
            tk.Label(row, text=f"{ability}:", width=15, anchor="w").pack(side="left")
            entry = tk.Entry(row, width=10)
            entry.pack(side="left")
            self.ability_entries[ability] = entry

        # Hit Points & Death Saves
        self.middle_frame = tk.Frame(root, borderwidth=2, relief="ridge")
        self.middle_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(self.middle_frame, text="Hit Point Max | Current HP | Temp HP").pack()
        tk.Label(self.middle_frame, text="Hit Dice | Death Saves").pack()

        # Attacks & Spellcasting
        self.attack_frame = tk.Frame(root, borderwidth=2, relief="ridge")
        self.attack_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(self.attack_frame, text="Attacks | Spellcasting").pack()

        # Roleplay Details
        self.roleplay_frame = tk.Frame(root, borderwidth=2, relief="ridge")
        self.roleplay_frame.pack(side="right", fill="y", padx=5, pady=5)
        tk.Label(self.roleplay_frame, text="Personality Traits | Ideals | Bonds | Flaws").pack()

        # Features & Traits
        self.features_frame = tk.Frame(root, borderwidth=2, relief="ridge")
        self.features_frame.pack(side="right", fill="y", padx=5, pady=5)
        tk.Label(self.features_frame, text="Features & Traits").pack()

        # Proficiencies & Languages
        self.prof_frame = tk.Frame(root, borderwidth=2, relief="ridge")
        self.prof_frame.pack(side="left", fill="y", padx=5, pady=5)
        tk.Label(self.prof_frame, text="Proficiencies & Languages").pack()

        # Equipment & Money
        self.equip_frame = tk.Frame(root, borderwidth=2, relief="ridge")
        self.equip_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(self.equip_frame, text="Equipment | CP, SP, EP, GP, PP").pack()

        # Passive Wisdom
        self.passive_frame = tk.Frame(root, borderwidth=2, relief="ridge")
        self.passive_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(self.passive_frame, text="Passive Wisdom").pack()

root = tk.Tk()
app = CharacterSheetApp(root)
root.mainloop()