import tkinter as tk
from rdkit import Chem
from rdkit.Chem import AllChem, Draw
from PIL import Image, ImageTk

class ChiralityAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("Chirality Analyzer")

        self.label = tk.Label(master, text="Enter Molfile or SMILES code:")
        self.label.pack()

        self.entry = tk.Entry(master, width=50)
        self.entry.pack()

        self.analyze_button = tk.Button(master, text="Analyze", command=self.analyze)
        self.analyze_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()

    def analyze(self):
        code = self.entry.get()
        if code:
            mol = None

            if code.startswith("Symyx"):  # Assume it's Molfile
                mol = Chem.MolFromMolBlock(code)
            else:  # Assume it's SMILES
                mol = Chem.MolFromSmiles(code)

            if mol:
                self.display_molecule(mol)
                self.identify_chiral_centers(mol)
            else:
                self.result_label.config(text="Failed to load molecule")

    def display_molecule(self, mol):
        img = Draw.MolToImage(mol, size=(500, 500), wedgeBonds=True)
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.config(width=img.width, height=img.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.img_tk = img_tk

    def identify_chiral_centers(self, mol):
        chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
        if chiral_centers:
            self.result_label.config(text=f"Number of chiral centers: {len(chiral_centers)}")
            for idx, (atom_idx, stereochemistry) in enumerate(chiral_centers, 1):
                self.result_label.config(text=self.result_label.cget("text") +
                                             f"\nChiral center {idx}: Atom {atom_idx}, Stereochemistry: {stereochemistry}")
        else:
            self.result_label.config(text="No chiral centers identified")


root = tk.Tk()
app = ChiralityAnalyzerApp(root)
root.mainloop()
