# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This is a visual app for picture ranking
#
# - Rank pictures in the selected folder
# - Memorize last ranked picture and start from there
# - 'labels.csv' is the output file responsible for saving every label for a given set
#
# Assumes a static folder, with a fixed number of immutable images with the same dimensions.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk

from utilities import *


class Ranker:

    def __init__(self):

        self.fold_path = None
        self.labels_path = None

        self.root = tk.Tk()
        self.root.title('FMK')

        self.image_panel = tk.Label(self.root, text="Welcome to the chick ranker", image=None)
        self.image_panel.pack(side='left')

        self.get_folder = tk.Button(self.root, text="Pick a folder to label", command=self.label_folder)
        self.get_folder.pack(side='right')

        self.close_button = tk.Button(self.root, text="Close", command=self.root.quit)
        self.close_button.pack(side='right')

        self.root.mainloop()

    def iterate_photos(self):

        image_filenames = [f for f in os.listdir(self.fold_path)
                           if os.path.isfile(os.path.join(self.fold_path, f))
                           and f.endswith('.jpg')]
        image_filenames.sort(key=filenumber)

        # iterates through pictures
        for image_name in image_filenames:
            image_path = os.path.join(self.fold_path, image_name)
            if os.path.isfile(image_path):

                # hash current picture and check if it's in .csv
                # TODO
                image_hash = file_hash(image_path)

                # loads unlabelled image to the frame
                image_frame = ImageTk.PhotoImage(Image.open(image_path))
                self.image_panel.config(image=image_frame)

                # waits for scores to be input - or check if user quits (close button)
                # TODO
                input()

                # updates received scores to .csv along with hash and filename
                # TODO

        return

    def save_entry(self):
        # given image and scores, adds new line to .csv file
        return

    def label_folder(self):

        self.fold_path = tk.filedialog.askdirectory()  # ask which folder to label
        fold_name = os.path.split(self.fold_path)[1]  #

        labels_name = fold_name+"_labels.csv"
        self.labels_path = os.path.join(self.fold_path, labels_name)

        assert os.path.isdir(self.fold_path), "Specified folder does not exist"
        assert os.listdir(self.fold_path), "Specified folder is empty"
        # missing condition to check if there are pictures in said folder

        # remove the load folder button and reassing the close button
        self.get_folder.pack_forget()

        if os.path.isfile(self.labels_path):
            print("Found a labels file "+labels_name)
        else:
            print("No labels found. Making "+labels_name)
            # make .csv

        self.iterate_photos()


        # check for <folder>_label.csv
        # if not exists:
        #   - create .csv
        #   - open picture 0.jpg
        # if exists:
        #   - find latest k entry labelled
        #   - open picture k+1.kpg


