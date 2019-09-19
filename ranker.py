# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This is a visual app for picture ranking
#
# - Rank pictures in the selected folder
# - Memorize last ranked picture and start from there
# - 'labels.csv' is the output file responsible for saving every label for a given set
# - Could have a function to clear latest entry in .csv if defective, and start from there
#
# Assumes a static folder, with a fixed number of immutable images with the same dimensions.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import csv
import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk

from utilities import *


class Ranker:

    def __init__(self, root):

        # binding main frame
        self.root = root

        # basic appearence setup
        self.image_panel = tk.Label(self.root, text="Welcome to the chick ranker.\nPick a folder and start labelling", image=None)
        self.image_panel.bind("<Key>", self.key_press)
        self.image_panel.grid(row=4, column=0)

        self.close_button = tk.Button(self.root, text="Close", command=self.root.quit)
        self.close_button.grid(row=0, column=1)

        # setting up the folder to be labelled
        self.fold_path = None
        while self.fold_path is None:
            try:
                self.fold_path = tk.filedialog.askdirectory()  # ask which folder to label
            except:
                print("Invalid folder")
                # folder is empty
                # folder does not exist
                # no pictures in folder
        """ TODO temporary assertions """
        assert os.path.isdir(self.fold_path), "Specified folder does not exist"
        assert os.listdir(self.fold_path), "Specified folder is empty"

        # list and sort all the pictures in folder
        self.image_filenames = [f for f in os.listdir(self.fold_path) if
                                os.path.isfile(os.path.join(self.fold_path, f)) and f.endswith('.jpg')]
        self.image_filenames.sort(key=filenumber)
        self.image_filenames_length = len(self.image_filenames)
        print("Labelling " + str(self.image_filenames_length) + " pictures")

        self.fold_name = os.path.split(self.fold_path)[1]
        self.foldername_label = tk.Label(self.root, text="Labelling folder -> "+self.fold_name+"\n\n"+str(self.image_filenames_length)+" pictures", bg="blue", fg="white")
        self.foldername_label.grid(row=0, column=0)

        # setting up the labels file
        self.labels_path = None
        self.labels_name = self.fold_name + "_labels.csv"  # computes the expected labels file
        self.labels_path = os.path.join(self.fold_path, self.labels_name)
        if os.path.isfile(self.labels_path):
            print("Found a labels file " + self.labels_name)
        else:
            print("No labels found. Making " + self.labels_name)
            with open(self.labels_name, mode='w+') as labels_file:
                fieldnames = ['File name', 'Hash', 'Girl score', 'Misc score']
                writer = csv.DictWriter(labels_file, fieldnames=fieldnames)
                writer.writeheader()

            # TODO make .csv

        # setting up previous score displays
        self.prev_girl_score_display = tk.Label(self.root, text="Previous girl score: ")
        self.prev_girl_score_display.grid(row=0, column=2)
        self.prev_girl_score_display_value = tk.Label(self.root, text="None")
        self.prev_girl_score_display_value.grid(row=0, column=3)

        self.prev_misc_score_display = tk.Label(self.root, text="Previous misc score: ")
        self.prev_misc_score_display.grid(row=1, column=2)
        self.prev_misc_score_display_value = tk.Label(self.root, text="None")
        self.prev_misc_score_display_value.grid(row=1, column=3)

        # setting up current score displays
        self.girl_score_display = tk.Label(self.root, text="Girl score: ")
        self.girl_score_display.grid(row=2, column=2)
        self.girl_score_display_value = tk.Label(self.root, text="None")
        self.girl_score_display_value.grid(row=2, column=3)

        self.misc_score_display = tk.Label(self.root, text="Misc score: ")
        self.misc_score_display.grid(row=3, column=2)
        self.misc_score_display_value = tk.Label(self.root, text="None")
        self.misc_score_display_value.grid(row=3, column=3)

        # load first picture to frame [load_to_frame(frame, image)]
        self.i = 0
        self.load_to_frame()
        self.image_panel.focus_set()

    def key_press(self, event):

        """
        3 possible cases
            a. clicked a valid number and nothing is ranked yet
                - add a score to the girl label
            b. clicked a valid number and girl is already ranked
                - add a score to the misc label
                - save image_filename, image_hash, gscore and mscore to .csv file
                - load next figure
            c. clicked 'R' triggering a reset on anything labelled yet
        """

        # extract the pressed key from the event
        kp = str(event.char)

        try:
            kp = float(kp)
            if kp > 5:
                print("Invalid score (1 to 5 expected)")
                return
            score = float(kp) / 5
            g_cur = self.girl_score_display_value.cget("text")
            m_cur = self.misc_score_display_value.cget("text")

            # a. clicked a valid number and nothing is ranked yet
            if g_cur == "None" and m_cur == "None":
                self.girl_score_display_value.config(text=str(score))

            # b. clicked a random number and girl is already ranked
            elif g_cur is not "None" and m_cur == "None":
                self.misc_score_display_value.config(text=str(score))
                # TODO save image_filename, image_hash, gscore and mscore to .csv file [save_entry()]
                self.clear_scores()
                self.load_to_frame()

        except ValueError:
            print("Invalid scoring key")

        # test print for the current pressed key
        print("Pressed", kp)  # repr(event.char))

    def clear_scores(self):
        """ clears scores for current picture and loads it to scores for previous picture"""
        self.prev_girl_score_display_value.config(text=self.girl_score_display_value.cget("text"))
        self.prev_misc_score_display_value.config(text=self.misc_score_display_value.cget("text"))

        self.girl_score_display_value.config(text="None")
        self.misc_score_display_value.config(text="None")

    def load_to_frame(self):

        if self.i+1 > self.image_filenames_length:
            self.foldername_label.config(text="Done labelling folder "+self.fold_name, bg="green", fg="black")
            self.image_panel.unbind("<Key>")

        else:
            image_path = os.path.join(self.fold_path, self.image_filenames[self.i])
            if os.path.isfile(image_path):
                image_hash = file_hash(image_path)
                # TODO check if it's in .csv
                resized = Image.open(image_path).resize((320, 400), Image.ANTIALIAS)
                image_frame = ImageTk.PhotoImage(resized)
                self.image_panel.config(image=image_frame)
                self.image_panel.image = image_frame
            self.i += 1

    def save_entry(self):
        # given image and scores, adds new line to .csv file
        return


def run():

    # load the frame and wait for the user to pick a folder to label
    r = tk.Tk()
    r.title('FMK')
    rh = Ranker(r)
    r.mainloop()

    return
