import tkinter as tk
import numpy as np
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2 as cv

#Fonction pour charger et afficher l'image
def load_image():
    global original_img, modified_img, original_tk_image, modified_tk_image
    path_img = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if path_img:
        original_img = cv.imread(path_img)
        modified_img = original_img.copy()
        original_img = cv.cvtColor(original_img, cv.COLOR_BGR2RGB)
        modified_img = cv.cvtColor(modified_img, cv.COLOR_BGR2RGB)
        original_tk_image = ImageTk.PhotoImage(image=Image.fromarray(original_img))
        modified_tk_image = ImageTk.PhotoImage(image=Image.fromarray(modified_img))
        # Afficher l'image chargée sur le premier label
        lbl_original.config(image=original_tk_image)
        # Afficher l'image modifiée sur le second label
        lbl_modified.config(image=modified_tk_image)
        
        
#Fonction pour mettre à jour l'image avec les nouvelles valeurs de RGB
def update_image(event=None):
    global modified_img, modified_tk_image
    if modified_img is not None:
        red = red_slider.get()
        green = green_slider.get()
        blue = blue_slider.get()
        # La formule de la manipulation : (255-x)*P'+x
        
        # Vérifier si les valeurs de rouge, vert et bleu sont toutes égales à 255
        if red == green == blue == 255:
            modified_img = np.full_like(original_img, (255, 255, 255))
        elif red == green == blue == -255 :
            modified_img = np.full_like(original_img, (0, 0, 0))
        elif red == green == blue == 0 :
            modified_img = original_img
        else:
           #Appliquer les transformations sur chaque canal de couleur
           modified_img = np.zeros_like(original_img, dtype=np.uint8)
           modified_img[:, :, 0] = original_img[:, :, 0] * blue
           modified_img[:, :, 1] = original_img[:, :, 1] * green
           modified_img[:, :, 2] = original_img[:, :, 2] * red

           #Clip les valeurs pour s'assurer qu'elles restent dans la plage 0-255
           modified_img = np.clip(modified_img, 0, 255)

    #Créer une image PIL à partir du tableau numpy modifié
    modified_img_pil = Image.fromarray(modified_img)

    #Convertir l'image PIL en image Tkinter
    modified_tk_image = ImageTk.PhotoImage(image=modified_img_pil)

    #Afficher l'image modifiée (supposons que lbl_modified est votre label Tkinter)
    lbl_modified.config(image=modified_tk_image)

#Fonction pour sauvegarder l'image modifiée     
def save_image():
    if modified_img is not None:
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if filename:
            cv.imwrite(filename, cv.cvtColor(modified_img, cv.COLOR_RGB2BGR))
            messagebox.showinfo("Save Image", "Image saved successfully!")       
        
#Création de la fenêtre principale
window = tk.Tk()
window.title("Image manipulation")
window.geometry("800x600")
window.resizable(False,False)

#Variables globales pour l'image originale, l'image modifiée et les images Tkinter
original_img = None
modified_img = None
original_tk_image = None
modified_tk_image = None

#Bouton pour charger l'image
btn_upload = tk.Button(window, text="Upload image", command=load_image, bg="#4CAF50", fg="white", font=("Arial", 12))
btn_upload.pack(pady=10)

# Label pour afficher l'image chargée
lbl_original = tk.Label(window)
lbl_original.pack()

#Création des barres de défilement pour les canaux RVB
red_slider = tk.Scale(window, from_=-255, to=255, orient=tk.HORIZONTAL, label="Blue", command=update_image, bg="#F0F0F0")
red_slider.pack()

green_slider = tk.Scale(window, from_=-255, to=255, orient=tk.HORIZONTAL, label="Green", command=update_image, bg="#F0F0F0")
green_slider.pack()

blue_slider = tk.Scale(window, from_=-255, to=255, orient=tk.HORIZONTAL, label="Red", command=update_image, bg="#F0F0F0")
blue_slider.pack()

#Label pour afficher l'image modifiée
lbl_modified = tk.Label(window)
lbl_modified.pack()

btn_save = tk.Button(window, text="Save image", command=save_image, bg="#008CBA", fg="white", font=("Arial", 12))
btn_save.pack(pady=10)

#Lancement de la boucle principale de Tkinter
window.mainloop()
