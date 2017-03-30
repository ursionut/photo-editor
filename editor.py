__author__ = "6066886: Esma Toptas, 6167662: Ionut Petre Urs"
__copyright__ = "Copyright 2015/2016 – PRG1-Goethe-Uni"
__credits__ = "Prof. Dr. Visvanathan Ramesh and Trainer Andres Fernandez"
__email__ = "topes.14@hotmail.de, ursionut@live.com"


import os
import tkinter as tk
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from scipy import ndimage
import numpy as np
#import cv2
from matplotlib import pyplot as plt
from tkinter import colorchooser
import tkinter.filedialog
import tkinter.messagebox


THEME_COLOR = "#FFFFFF"  # sets the constant to a default hex color value
# stores the manipulated images
undo_list = []
# stores the manipulated images popped out from the undo list
redo_list = []


class Editor(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.configure(background=THEME_COLOR)
        # creates an empty instance variable
        # used to store the last manipulated image
        self.image_reference = None
        # creates an intVar
        # used to change the theme color
        self.theme_variable = tk.IntVar()
        # sets the intValue to 0
        self.theme_variable.set(1)

        # main frame
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack()
        self.main_frame.configure(background=THEME_COLOR)

        # creates the frame which will hold the menu buttons
        self.menubar_frame = tk.Frame(self.main_frame)
        self.menubar_frame.grid(row=0, column=0)
        self.menubar_frame.configure(background=THEME_COLOR)

        # creates the frame which will hold the image
        self.image_holder_frame = tk.Frame(self.main_frame)
        self.image_holder_frame.grid(row=1, column=0)
        self.image_holder_frame.configure(background=THEME_COLOR)

        # creates the top-level menu-bar which holds the drop-down buttons
        self.menubar = tk.Menu(self.menubar_frame)
        self.master.config(menu=self.menubar)
        self.menubar.configure(background=THEME_COLOR)

        # creates the label which will hold the image
        self.image_label = tk.Label(self.image_holder_frame)
        self.image_label.pack()
        self.image_label.configure(background=THEME_COLOR)

        # sets the label width and height
        # equal to the screen width and height
        # subtracts 150 pixels from screen height
        self.label_width = self.image_holder_frame.winfo_screenwidth()
        self.label_height = self.image_holder_frame.winfo_screenheight() - 150

        # constructing the 'File' drop-down menu
        # imports the images which appear on every file-menu button
        self.open_icon = tk.PhotoImage(file="Icons/open.png")
        self.save_icon = tk.PhotoImage(file="Icons/save.png")
        self.save_as_icon = tk.PhotoImage(file="Icons/save_as.png")
        self.settings_icon = tk.PhotoImage(file="Icons/settings.png")
        # creates the drop-down button 'File' and adds it to the menu-bar
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.configure(background=THEME_COLOR)
        # adds the 'Open' command button to the 'File' drop-down menu
        # has the keyboard shortcut 'Ctrl + O'
        self.file_menu.add_command(label=" Open", accelerator='Ctrl + O',
                                   compound="left", image=self.open_icon,
                                   command=self.open_image)
        # adds the 'Save' command button to the 'File' drop-down menu
        # has the keyboard shortcut 'Ctrl + S'
        self.file_menu.add_command(label=" Save", accelerator='Ctrl + S',
                                   compound="left", image=self.save_icon,
                                   command=self.save_image)
        # adds the 'Save as...' command button to the 'File' drop-down menu
        # has the keyboard shortcut 'Ctrl+ Shift + O'
        self.file_menu.add_command(label=" Save As...", compound="left",
                                   accelerator='Ctrl + Shift + S',
                                   image=self.save_as_icon,
                                   command=self.save_as)
        # creates the 'Settings' drop-down menu
        # adds the radio buttons which help the user to change the color theme
        self.themes_menu = tk.Menu(self.file_menu, tearoff=0)
        self.themes_menu.configure(background=THEME_COLOR)
        # adds the 'Default White' radio button
        self.themes_menu.add_radiobutton(label="Default White",
                                         variable=self.theme_variable,
                                         value=1, command=self.theme_color)
        # adds the 'Gray' radio button
        self.themes_menu.add_radiobutton(label="Gray",
                                         variable=self.theme_variable,
                                         value=2, command=self.theme_color)
        # adds the 'Green' radio button
        self.themes_menu.add_radiobutton(label="Green",
                                         variable=self.theme_variable,
                                         value=3, command=self.theme_color)
        # adds the 'Blue' radio button
        self.themes_menu.add_radiobutton(label="Blue",
                                         variable=self.theme_variable,
                                         value=4, command=self.theme_color)
        # adds the 'Pink' radio button
        self.themes_menu.add_radiobutton(label="Pink",
                                         variable=self.theme_variable,
                                         value=5, command=self.theme_color)
        # adds the 'Custom theme' radio button
        self.themes_menu.add_radiobutton(label="Custom theme",
                                         variable=self.theme_variable,
                                         value=6, command=self.custom_theme)
        # adds the 'Settings' cascade button to the 'File' drop-down menu
        self.file_menu.add_cascade(label=" Settings", image=self.settings_icon,
                                   compound="left", menu=self.themes_menu)
        # adds a separator between the 'Settings' and 'Exit' buttons
        self.file_menu.add_separator()
        # adds the 'Exit' command button to the 'File' drop-down menu
        self.file_menu.add_command(label=" Exit", command=self.exit_program)
        # ending the construction of the 'File' drop-down menu 

        # constructing the 'Edit' drop-down menu 
        # imports the images which appear on every edit-menu button
        self.undo_icon = tk.PhotoImage(file="Icons/undo.png")
        self.redo_icon = tk.PhotoImage(file="Icons/redo.png")
        self.flip_horizontally_icon = tk.PhotoImage(file="Icons/flip_hor.png")
        self.flip_vertically_icon = tk.PhotoImage(file="Icons/flip_vert.png")
        self.turn_right_icon = tk.PhotoImage(file="Icons/turn_right.png")
        self.turn_left_icon = tk.PhotoImage(file="Icons/turn_left.png")
        self.turn_180_icon = tk.PhotoImage(file="Icons/turn_180.png")
        # creates the drop-down button 'Edit' and adds it to the menu-bar
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.configure(background=THEME_COLOR)
        # adds the 'Undo' command button to the 'Edit' drop-down menu
        # has the keyboard shortcut 'Ctrl + Z'
        self.edit_menu.add_command(label=" Undo", accelerator='Ctrl + Z',
                                   compound="left", image=self.undo_icon,
                                   command=self.undo)
        # adds the 'Redo' command button to the 'Edit' drop-down menu
        # has the keyboard shortcut 'Ctrl + Shift + Z'
        self.edit_menu.add_command(label=" Redo", image=self.redo_icon,
                                   accelerator='Ctrl + Shift + Z',
                                   compound="left",  command=self.redo)
        # adds a separator between the 'Redo' and 'Flip Horizontally' buttons
        # separates the undo-redo buttons block from the flip buttons block
        self.edit_menu.add_separator()
        # adds the 'Flip Horizontally' command button
        # to the 'Edit' drop-down menu
        self.edit_menu.add_command(label=" Flip Horizontally", compound="left",
                                   image=self.flip_horizontally_icon,
                                   command=self.flip_horizontally)
        # adds the 'Flip Vertically' command button
        # to the 'Edit' drop-down menu
        self.edit_menu.add_command(label=" Flip Vertically", compound="left",
                                   image=self.flip_vertically_icon,
                                   command=self.flip_vertically)
        # adds a separator between
        # the 'Flip Vertically' and 'Rotate 90' buttons
        # separates the flip buttons block from the rotate buttons block
        self.edit_menu.add_separator()
        # adds the 'Rotate 90 clockwise' command button
        #  to the 'Edit' drop-down menu
        self.edit_menu.add_command(label=" Rotate 90\u00b0 clockwise",
                                   compound="left", image=self.turn_right_icon,
                                   command=self.rotate_right)
        # adds the 'Rotate 90 counter - clockwise' command button
        #  to the 'Edit' drop-down menu
        self.edit_menu.add_command(label=" Rotate 90\u00b0 counter-clockwise",
                                   compound="left", image=self.turn_left_icon,
                                   command=self.rotate_left)
        # adds the 'Rotate 180' command button to the 'Edit' drop-down menu
        self.edit_menu.add_command(label=" Rotate 180\u00b0", compound="left",
                                   image=self.turn_180_icon,
                                   command=self.rotate_180)
        # ending the construction of the 'Edit' drop-down menu 

        # constructing the 'Image' drop-down menu 
        # imports the images which appear on every image-menu button
        self.sclae_icon = tk.PhotoImage(file="Icons/scale_image.png")
        self.crop_icon = tk.PhotoImage(file="Icons/invert.png")
        self.contrast_icon = tk.PhotoImage(file="Icons/contrast.png")
        self.graysclae_icon = tk.PhotoImage(file="Icons/grayscale.png")
        # creates the drop-down button 'Image' and adds it to the menu-bar
        self.image_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Image", menu=self.image_menu)
        self.image_menu.configure(background=THEME_COLOR)
        # adds the 'Scale Image' command button to the 'Image' drop-down menu
        self.image_menu.add_command(label=" Scale Image", compound="left",
                                    image=self.sclae_icon,
                                    command=self.scale_image_window)
        # adds the 'Crop' command button to the 'Image' drop-down menu
        self.image_menu.add_command(label=" Invert", compound="left",
                                    image=self.crop_icon, command=self.invert)
        # adds the 'Contrast' command button to the 'Image' drop-down menu
        self.image_menu.add_command(label=" Contrast", compound="left",
                                    image=self.contrast_icon,
                                    command=self.contrast)
        # adds the 'Grayscale' command button to the 'Image' drop-down menu
        self.image_menu.add_command(label=" Grayscale", compound="left",
                                    image=self.graysclae_icon,
                                    command=self.to_grayscale)
        # adds a separator between the 'Grayscale'
        # and 'Image Histogram' buttons
        self.image_menu.add_separator()
        # adds the 'Image Histogram' command button to the 'Image'
        # drop-down menu
        self.image_menu.add_command(label=" Image Histogram", compound="left",
                                    command=self.image_histogram)
        # adds the 'Image Thresholding' command button to the 'Image'
        # drop-down menu
        self.image_menu.add_command(label=" Image Thresholding",
                                    compound="left",
                                    command=self.thresholding_frame)
        # adds the 'Fourier-Transformation' command button to the 'Image'
        # drop-down menu
        self.image_menu.add_command(label=" Fourier-Transformation",
                                    compound="left",
                                    command=self.fourier_transformation)
        # ending the construction of the 'Image' drop-down menu 

        # constructing the 'Filters' drop-down menu
        # creates the drop-down button 'Filters' and adds it to the menu-bar
        self.filters_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Filters", menu=self.filters_menu)
        self.filters_menu.configure(background=THEME_COLOR)
        # adds the 'Blur' command button to the 'Filters' drop-down menu
        self.filters_menu.add_command(label="Blur", command=self.blur_image)
        # adds the 'Gaussian Blur' command button to the
        # 'Filters' drop-down menu
        self.filters_menu.add_command(label="Gaussian Blur",
                                      command=self.gaussian_frame)
        # adds the 'Smooth' command button to the 'Filters' drop-down menu
        self.filters_menu.add_command(label="Smooth",
                                      command=self.smooth_image)
        # adds a separator between the 'Smooth' and 'Find Edges' buttons
        self.filters_menu.add_separator()
        # adds the 'Find Edges' command button to the 'Filters' drop-down menu
        self.filters_menu.add_command(label="Find Edges",
                                      command=self.find_edges)
        # adds the 'Contour' command button to the 'Filters' drop-down menu
        self.filters_menu.add_command(label="Contour",
                                      command=self.image_contour)
        # ending the construction of the 'Filters' drop-down menu 

        # constructing the 'Help' drop-down menu
        # creates the drop-down button 'Help' and adds it to the menu-bar
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.configure(background=THEME_COLOR)
        # adds the 'Help' command button to the 'Help' drop-down menu
        # has the keyboard shortcut 'F1'
        self.help_menu.add_command(label="Help", accelerator='F1',
                                   command=self.help)
        # adds the 'About' command button to the 'Help' drop-down menu
        self.help_menu.add_command(label="About", command=self.about)
        # ending the construction of the 'Help' drop-down menu 

        # performs the same action as the 'Open' button from 'File'
        # drop-down menu and creates a keyboard shortcut which
        # calls the open_image() method
        self.master.bind('<Control-o>', lambda e: self.open_image())
        self.master.bind('<Control-O>', lambda e: self.open_image())
        # performs the same action as the 'Save' button from 'File'
        # drop-down menu and creates a keyboard shortcut which
        # calls the save_image() method
        self.master.bind('<Control-s>', lambda e: self.save_image())
        self.master.bind('<Control-S>', lambda e: self.save_image())
        # performs the same action as the 'Save as...' button from 'File'
        # drop-down menu and creates a keyboard shortcut which
        # calls the save_as() method
        self.master.bind('<Control-Shift-s>', lambda e: self.save_as())
        self.master.bind('<Control-Shift-S>', lambda e: self.save_as())
        # performs the same action as the 'Undo' button from 'Edit'
        # drop-down menu and creates a keyboard shortcut which
        # calls the undo() method
        self.master.bind('<Control-z>', lambda e: self.undo())
        self.master.bind('<Control-Z>', lambda e: self.undo())
        # performs the same action as the 'Redo' button from 'Edit'
        # drop-down menu and creates a keyboard shortcut which
        # calls the redo() method


        self.master.bind('<Control-Shift-z>', lambda e: self.redo())
        self.master.bind('<Control-Shift-Z>', lambda e: self.redo())
        # performs the same action as the 'Help' button from 'Help'
        # drop-down menu and creates a keyboard shortcut which
        # calls the help() method
        self.master.bind('<KeyPress-F1>', lambda e: self.help())

    def open_image(self):
        """
        these function returns the path to image, opens the image
        as a numpy image, converts the image into a PIL Image resize
        the image and displays it with tkinter PhotoImage
        """
        self.file_types = [('All files', '*'), ('GIF Image', '*.gif'),
                           ('JPEG Image', '*.jpg *.jpeg *.jpe'),
                           ('PNG Image', '*.png'), ('BMP Image', '*.bmp'),
                           ('TIFF Image', '*.tiff *.tif')]
        # returns a string which include the image name and path
        self.file_name = tkinter.filedialog.askopenfilename(
            parent=self.master, title='Choose a file',
            filetypes=self.file_types)

        # if the file isn't a image, a warning message appears
        # opens only images
        if self.file_name != "":
            try:
                # opens the image as a scipy image
                self.img = ndimage.imread(self.file_name)
                # converts the image into a PIL Image
                self.image = Image.fromarray(self.img)
                # saves the image in an instance variable
                self.image_reference = self.image
                # sets the height and width variables equal to the
                # height and width of the image
                width, height = self.image.size
                # runs the resize image() function and returns the new image
                self.image_resized = self.resize_image(width, height,
                                                       self.label_width,
                                                       self.label_height,
                                                       self.image)
                # puts the PIL image into a TK PhotoImage to display it
                image_tk = ImageTk.PhotoImage(image=self.image_resized)
                # keeps a reference of the PhotoImage
                self.image_label.image = image_tk
                self.image_label.configure(image=image_tk)
                # adds the PIL image into a list so that it can be later
                # by the undo function used
                undo_list.append(self.image_reference)
            except:
                # a warning message box appears when the user tries to
                # open a file which isn't an image
                tkinter.messagebox.showwarning(title='Open file',
                                               message='Cannot open this file',
                                               icon='error')
        else:
            pass

        return self.file_name

    def resize_image(self, width, height, label_width, label_height, image):
        """
        these function resize a PIL Image so it can fit into a label
        that has the width and height of screen but retain aspect ratio.

        if the image has the resolution smaller than the resolution
        of the screen, the function returns the original image,
        otherwise the function resize the image and returns it

        :param width: int image width
        :param height: int image height
        :param label_width: int label width
        :param label_height: int label height
        :param image: PIL Image
        :returns: resized image
        """

        # divides the label width and height to the width respectively
        # height of the image, and turns the result into a float number
        # helps to retain the aspect ratio of the image
        self.factor_one = 1.0 * label_width / width
        self.factor_two = 1.0 * label_height / height
        # resize the image according to its longer side
        self.factor = min([self.factor_one, self.factor_two])
        # if the image resolution is smaller as the label resolution
        # the function returns the original image
        # otherwise the function resize the image
        if self.factor_one > 1 and self.factor_two > 1:
            return image
        else:
            # sets the new height and width values so that the
            # image will fit into the label and retain the aspect ratio
            self.width_resized = int(width * self.factor)
            self.height_resized = int(height * self.factor)
            # returns the resized image
            return image.resize((self.width_resized, self.height_resized),
                                 Image.ANTIALIAS)

    def save_image(self):
        """
        these function replace the old image with the image
        modified by user
        """
        try:
            # takes the image path and name
            image_name = self.file_name
            # saves the new image with the same name old image
            # and replaces it
            self.image.save(image_name)
        except:
            # if the file doesn't exist, the save as function runs
            self.save_as()

    def save_as(self):
        """
        these function save the image in a chosen location
        with the name and extension entered by user
        """
        try:
            self.file_types = [('All files', '*'), ('GIF Image', '*.gif'),
                               ('JPEG Image', '*.jpg *.jpeg *.jpe'),
                               ('PNG Image', '*.png'), ('BMP Image', '*.bmp'),
                               ('TIFF Image', '*.tiff *.tif')]
            # returns a string which include the image name and path
            # sets a default image title and extension
            self.save_img_as = tkinter.filedialog.asksaveasfilename\
                    (initialfile='Untitled.png', filetypes=self.file_types)
            # saves the image into the desired location
            self.image.save(self.save_img_as)
        except:
            pass

    def theme_color(self):
        """
        these function changes the programs theme color. It changes
        the the color in accordance to a int variable set earlier
        """
        # sets the variable equal with a number from 1 to 5
        self.variable = self.theme_variable.get()
        self.background_color = "#FFFFFF"  # default white

        # changes the theme color in accordance with the variable number
        if self.variable == 1:
            self.background_color = "#FFFFFF"  # Default white
        elif self.variable == 2:
            self.background_color = "#D1D1D1"  # Gray
        elif self.variable == 3:
            self.background_color = "#C1E0C3"  # Green
        elif self.variable == 4:
            self.background_color = "#BFD9F2"  # Blue
        elif self.variable == 5:
            self.background_color = "#F7DEFA"  # Pink
        else:
            pass

        # applies the made changes to the program
        self.master.configure(background=self.background_color)
        self.main_frame.configure(background=self.background_color)
        self.image_holder_frame.configure(background=self.background_color)
        self.menubar.configure(background=self.background_color)
        self.file_menu.configure(background=self.background_color)
        self.themes_menu.configure(background=self.background_color)
        self.edit_menu.configure(background=self.background_color)
        self.image_menu.configure(background=self.background_color)
        self.filters_menu.configure(background=self.background_color)
        self.help_menu.configure(background=self.background_color)
        self.image_label.configure(background=self.background_color)

    def custom_theme(self):
        """
        these function lets the user to personalize the color theme
        """
        # opens a top-level window where the user can choose the
        # desired color and returns the hex color value
        self.color = colorchooser.askcolor()
        # sets the background color to the returned hex color value
        self.color_choice = self.color[1]
        # applies the made changes to the program
        self.master.configure(background=self.color_choice)
        self.main_frame.configure(background=self.color_choice)
        self.image_holder_frame.configure(background=self.color_choice)
        self.menubar.configure(background=self.color_choice)
        self.file_menu.configure(background=self.color_choice)
        self.themes_menu.configure(background=self.color_choice)
        self.edit_menu.configure(background=self.color_choice)
        self.image_menu.configure(background=self.color_choice)
        self.filters_menu.configure(background=self.color_choice)
        self.help_menu.configure(background=self.color_choice)
        self.image_label.configure(background=self.color_choice)

    def exit_program(self):
        """
        displays a tkinter message box which asks the user if
        he really wants to quit

        returns True if answer is 'yes' and exits the program
        returns False if the answer is 'no' and pass
        """
        if tkinter.messagebox.askyesno(title="Quit", message="Are you " +
                                       "sure you want to quit?\n"
                                       "\nAll unsaved data will be lost."):
            self.master.destroy()  # exits the main program
            # if there is a temp image in the temp folder, deletes it
            try:
                os.remove('temp/temp.png')
            except:
                pass

    def undo(self):
        """
        these function lets the user to go back one step at a time
        after every image manipulation

        when the function runs the program goes back one step and
        displays the second least image manipulation and so on
        until the original image appears
        """
        # runs only if the list, where the manipulated images are
        # stored, isn't empty
        if len(undo_list) != 0:
            try:
                # uses the second least manipulated PIL image
                self.image = undo_list[-2]
                # saves the image in an instance variable
                self.image_reference = self.image
                # sets the height and width variables equal to the
                # height and width of the image
                width, height = self.image.size
                # runs the resize image() function and returns the new image
                self.image_resized = self.resize_image(width, height,
                                                       self.label_width,
                                                       self.label_height,
                                                       self.image)
                # puts the PIL image into a TK PhotoImage to display it
                image_tk_undo = ImageTk.PhotoImage(image=self.image_resized)
                # keeps a reference of the PhotoImage
                self.image_label.image = image_tk_undo
                self.image_label.configure(image=image_tk_undo)
                # appends the least manipulated photo to the redo list
                # if it isn't already stored there
                if undo_list[-1] not in redo_list:
                    redo_list.append(undo_list[-1])
                else:
                    pass
                # appends the second least manipulated image to the undo list
                redo_list.append(undo_list[-2])
                # removes the least manipulated image from the list
                undo_list.pop()
            except:
                pass
        else:
            pass

    def redo(self):
        """
        these function lets the user to go a step forward after every
        backward step maid trough undo function
        """
        # runs only if the list isn't empty
        if len(redo_list) != 0:
            try:
                # uses the image from which the user get a backward step
                self.image = redo_list[-1]
                # saves the image in an instance variable
                self.image_reference = self.image
                # sets the height and width variables equal to the
                # height and width of the image
                width, height = self.image.size
                # runs the resize image() function and returns the new image
                self.image_resized = self.resize_image(width, height,
                                                       self.label_width,
                                                       self.label_height,
                                                       self.image)
                # puts the PIL image into a TK PhotoImage to display it
                image_tk_redo = ImageTk.PhotoImage(image=self.image_resized)
                # keeps a reference of the PhotoImage
                self.image_label.image = image_tk_redo
                self.image_label.configure(image=image_tk_redo)
                undo_list.append(redo_list[-1])
                redo_list.pop()
            except:
                pass
        else:
            pass

    def flip_horizontally(self):
        """
        these function generates a mirror-reversal of the original image
        across a horizontal axis
        """
        try:
            # modifies the image stored in the instance variable
            # flips the image horizontally
            self.image = self.image_reference.transpose(Image.FLIP_TOP_BOTTOM)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_flip_horiz = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_flip_horiz
            self.image_label.configure(image=image_tk_flip_horiz)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def flip_vertically(self):
        """
        these function generates a mirror-reversal of the original image
        across a vertical axis
        """
        try:
            # modifies the image stored in the instance variable
            # flips the image vertically
            self.image = self.image_reference.transpose(Image.FLIP_LEFT_RIGHT)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_flip_vert = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_flip_vert
            self.image_label.configure(image=image_tk_flip_vert)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def rotate_right(self):
        """
        these function rotates the image 90 degree to right
        """
        try:
            # modifies the image stored in the instance variable
            # rotates the image 90 degree to right
            self.image = self.image_reference.rotate(-90)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_rotate_right = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_rotate_right
            self.image_label.configure(image=image_tk_rotate_right)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def rotate_left(self):
        """
        these function rotates the image 90 degree to left
        """
        try:
            # modifies the image stored in the instance variable
            # rotates the image 90 degree to left
            self.image = self.image_reference.rotate(90)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_rotate_left = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_rotate_left
            self.image_label.configure(image=image_tk_rotate_left)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def rotate_180(self):
        """
        these function rotates the image 180 degree
        """
        try:
            # modifies the image stored in the instance variable
            # rotates the image 180 degree
            self.image = self.image_reference.rotate(180)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_rotate_180 = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_rotate_180
            self.image_label.configure(image=image_tk_rotate_180)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def scale_image_window(self):
        """
        these function creates a top-level menu where the desired
        width and height can be set
        """
        # crates the top-level frame
        self.scale_frame = tk.Toplevel()
        self.scale_frame.title("Scale Image")
        self.scale_frame.geometry('250x120')
        # creates a label inside the top-level frame
        self.label = tk.Label(self.scale_frame, text='Image Size',
                              font="Helvetica 12 bold")
        self.label.grid(row=0, column=0, padx=20)
        # crates the width label inside top-level frame
        self.width_label = tk.Label(self.scale_frame, text='Width:')
        self.width_label.grid(row=1, column=0)
        # creates the entry widget for width value
        self.width_entry = tk.Entry(self.scale_frame, width='10',
                                    font="Helvetica 11", justify="right")
        self.width_entry.grid(row=1, column=1)
        # creates the height label inside the toplevel frame
        self.height_label = tk.Label(self.scale_frame, text='Height:')
        self.height_label.grid(row=2, column=0)
        # creates the entry widget for height value
        self.height_entry = tk.Entry(self.scale_frame, width='10',
                                     font="Helvetica 11", justify="right")
        self.height_entry.grid(row=2, column=1)
        # creates the buttons frame inside the top-level frame
        self.button_frame = tk.Frame(self.scale_frame)
        self.button_frame.grid(row=3, column=0, columnspan=2)
        # creates the 'ok' button
        self.ok_button = tk.Button(self.button_frame, text='  OK  ',
                                   command=self.get_scale_size)
        self.ok_button.grid(row=0, column=1, sticky='e', pady=10, padx=20)
        # creates the 'cancel' button
        self.cancel_button = tk.Button(self.button_frame, text='Cancel',
                                       command=lambda: \
                                           self.scale_frame.destroy())
        self.cancel_button.grid(row=0, column=0, sticky='e', pady=10, padx=5)

    def get_scale_size(self):
        """
        these function retrieves the values for width and height
        entered by user into the entry widgets from the top-level frame
        """
        try:
            # retrieves an int value for new image width
            self.new_width = int(self.width_entry.get())
            # retrieves an int value for new image height
            self.new_height = int(self.height_entry.get())
            # quits the top level frame after retrieving the values
            # for width an height
            self.scale_frame.destroy()
            # runs the scale image function, which applies the changes
            # to the image
            self.scale_image()
        except:
            # a warning message box appears when the entry widgets
            # doesn't return a integer
            tkinter.messagebox.showwarning(title='Contrast',
                                           message='Please enter a valid ' +
                                           'width and height value',
                                           icon='error')

    def scale_image(self):
        """
        these function changes the image resolution, by setting the
        image width and height equal to the width and height values
        entered by user
        """
        try:
            # modifies the image stored in the instance variable
            # changes the image width and height
            self.image = self.image_reference.resize((self.new_width,
                                                      self.new_height),
                                                      Image.ANTIALIAS)
            # saves the image in an instance variable
            self.image_reference = self.image
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_scale = ImageTk.PhotoImage(image=self.image)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_scale
            self.image_label.configure(image=image_tk_scale)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def contrast(self):
        """
        these function creates a top-level frame with a scale bar,
        where the user can enter a desired contrast value
        the scale bar returns values between -100 and 100
        """
        self.value = tk.DoubleVar()
        # creates a top-level frame
        self.contrast_frame = tk.Toplevel()
        self.contrast_frame.title("Contrast")
        self.contrast_frame.geometry('305x120')
        # creates a frame for buttons
        self.button_frame = tk.Frame(self.contrast_frame)
        self.button_frame.grid(row=1, column=0)
        # creates the 'ok' button inside the top-level frame
        self.ok_button = tk.Button(self.button_frame, text='  OK  ',
                                   command=self.get_contrast_value)
        self.ok_button.grid(row=0, column=1, sticky='e', pady=10)
        # creates the 'cancel' button inside the top-level frame
        self.cancel_button = tk.Button(self.button_frame, text='Cancel',
                                       command=lambda: \
                                           self.contrast_frame.destroy())
        self.cancel_button.grid(row=0, column=0, sticky='e', pady=10)
        # creates a scale bar inside the top-level frame
        # helps to set the desired contrast value
        self.scale_bar = tk.Scale(self.contrast_frame, length=300,
                                  from_=-100, to=100, orient='horizontal',
                                  tickinterval=50, width=20, sliderlength=20,
                                  variable = self.value)
        self.scale_bar.grid(row=0, column=0)
        # sets the default scale bar value to 0
        self.scale_bar.set(0)

    def get_contrast_value(self):
        """
        these function get the value from the scale bar widget when
        the ok button is pressed

        sets the contrast value between 0 and 2, where 0 is the
        minimum value, 2 is the maximum and 1 doesn't change the image
        """
        try:
            # gets the value from the scale bar widget
            self.contrast_value = self.value.get()
            # closes the top-level after the user chooses a value and
            # presses the 'OK' button
            self.contrast_frame.destroy()
            # transforms the values between -99 an 0 into values
            # between 0.01 and 0.99 and sets the contrast value accordingly
            if -99 < self.contrast_value < 0:
                self.new_contrast_value = 1 - self.contrast_value / -100
            # if the returned value is -100, sets the contrast value at 0
            elif self.contrast_value == -100:
                self.new_contrast_value = 0
            # transforms the values between 0 an 99 into values
            # between 1.01 and 0.99 and sets the contrast value accordingly
            elif 0 < self.contrast_value < 99:
                self.new_contrast_value = 1 + self.contrast_value / 100
            # if the returned value is 100, sets the contrast value at 2
            elif self.contrast_value == 100:
                self.new_contrast_value = 2
            elif self.contrast_value == 1:
                self.new_contrast_value = 0.01
            # if the returned value is 0, sets the contrast value at 1
            # no change is applied to the image
            elif self.contrast_value == 0:
                self.new_contrast_value = 1
            else:
                pass
            # runs the change contrast function which applies the
            # chances to the image
            self.change_contrast()
        except:
            pass

    def change_contrast(self):
        """
        these function changes the image contrast using the
        contrast values entered by user
        """
        try:
            # modifies the image stored in the instance variable
            # changes the image contrast
            self.enhancer = ImageEnhance.Contrast(self.image_reference)
            self.image = self.enhancer.enhance(self.new_contrast_value)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_contrast = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_contrast
            self.image_label.configure(image=image_tk_contrast)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:

            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def invert(self):
        """
        these function inverts all the pixel colors and brightness
        values in the current layer
        dark areas become bright and bright areas become dark
        """
        try:
            # uses the image stored in the instance variable
            self.image = self.image_reference
            # verifies if the image is a gray-scale image or a rgb image
            # splits and merge the image, so that the alfa channel
            # can be removed
            if self.image.mode == 'RGBA':
                self.image.load()
                r, g, b, a = self.image.split()
                self.image = Image.merge('RGB', (r, g, b))
            # modifies the image stored in the instance variable
            # inverts the image colors
            self.image = ImageOps.invert(self.image)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_invert = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_invert
            self.image_label.configure(image=image_tk_invert)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def to_grayscale(self):
        """
        these function changes the image colors in to shades of gray
        """
        try:
            # modifies the image stored in the instance variable
            # modifies the image
            self.image = self.image_reference.convert('L')
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_gray = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_gray
            self.image_label.configure(image=image_tk_gray)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def image_histogram(self):
        """
        these function displays the image histogram
        3 channel histogram for rgb images and 1 channel histogram
        for gray-scale images
        """
        try:
            # saves the PIL image in a temporary file
            self.temp_image = self.image_reference
            self.temp_image.save('temp/temp.png')
            # loads the image as a cv2 image
            self.img = cv2.imread('temp/temp.png')
            self.color = ('b', 'g', 'r')
            # calculates the histogram for each channel and plots it
            # by using the matplotlib library
            for i, col in enumerate(self.color):
                self.histogram = cv2.calcHist([self.img], [i], None,
                                              [256], [0, 256])
                plt.plot(self.histogram, color=col)
                plt.xlim([0, 256])
            # displays the histogram
            plt.show()
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def thresholding_frame(self):
        """
        these function creates a top-level frame with a scale bar,
        where the user can enter a desired contrast value
        the scale bar returns values between 50 and 200
        """
        self.thres_value = tk.IntVar()
        # creates a top-level frame
        self.thres_frame = tk.Toplevel()
        self.thres_frame.title("Thresholding Value")
        self.thres_frame.geometry('305x120')
        # creates a frame for buttons
        self.button_frame = tk.Frame(self.thres_frame)
        self.button_frame.grid(row=1, column=0)
        # creates the 'ok' button inside the top-level frame
        self.ok_button = tk.Button(self.button_frame, text='  OK  ',
                                   command=self.get_thres_value)
        self.ok_button.grid(row=0, column=1, sticky='e', pady=10)
        # creates the 'cancel' button inside the top-level frame
        self.cancel_button = tk.Button(self.button_frame, text='Cancel',
                                       command=lambda: \
                                           self.thres_frame.destroy())
        self.cancel_button.grid(row=0, column=0, sticky='e', pady=10)
        # creates a scale bar inside the top-level frame
        # helps to set the desired thresholding value
        self.scale_bar = tk.Scale(self.thres_frame, length=300,
                                  from_=50, to=200, orient='horizontal',
                                  tickinterval=25, width=20, sliderlength=20,
                                  variable = self.thres_value)
        self.scale_bar.grid(row=0, column=0)
        # sets the default scale bar value to 125
        self.scale_bar.set(125)

    def get_thres_value(self):
        """
        these function retrieves the value from the scale bar and
        runs the image thresholding function which applies the changes
        to the image
        """
        try:
            # gets the value from the scale bar widget
            self.thres = self.thres_value.get()
            # closes the top-level after the user chooses a value and
            # presses the 'OK' button
            self.thres_frame.destroy()
            # applies the changes
            self.image_thresholding()
        except:
            pass

    def image_thresholding(self):
        """
        these function converts a gray-scale image into a binary image
        """
        try:
            # saves the PIL image in a temporary file
            self.temp_image = self.image_reference
            self.temp_image.save('temp/temp.png')
            # loads the image as a gray-scale cv2 image
            self.img = cv2.imread('temp/temp.png', 0)
            # sets the type of thresholding
            ret,thresh = cv2.threshold(self.img, self.thres, 255,
                                       cv2.THRESH_BINARY
                                       # cv2.THRESH_BINARY_INV
                                       # cv2.THRESH_TRUNC
                                       # cv2.THRESH_TOZERO
                                       # cv2.THRESH_TOZERO_INV
                                        )
            # plots and shows the image by using the matplotlib library
            plt.imshow(thresh, 'gray')
            plt.show()
        except:

            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def fourier_transformation(self):
        """
        these function decompose an image into its sine and cosine
        components. The output of the transformation represents the
        image in the Fourier or frequency domain
        """
        try:
            # saves the PIL image in a temporary file
            self.temp_image = self.image_reference
            self.temp_image.save('temp/temp.png')
            # loads the image as a gray-scale cv2 image
            self.img = cv2.imread('temp/temp.png', 0)
            self.fourier = np.fft.fft2(self.img)
            self.fourier_shift = np.fft.fftshift(self.fourier)
            magnitude_spectrum = 20*np.log(np.abs(self.fourier_shift))
            # plots the image and displays it
            plt.imshow(magnitude_spectrum, cmap='gray')
            plt.show()
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def blur_image(self):
        """
        these function applies a blur filter to the image
        """
        try:
            # modifies the image stored in the instance variable
            # applies the blur filter to the image
            self.image = self.image_reference.filter(ImageFilter.BLUR)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_blur = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_blur
            self.image_label.configure(image=image_tk_blur)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def gaussian_frame(self):
        """
        these function creates a top-level menu with a scale bar
        which returns a value between 0 and 100
        """
        self.gaussian_radius = tk.DoubleVar()
        # creates the top-level frame
        self.gaussian_frame = tk.Toplevel()
        self.gaussian_frame.title("Gaussian Blur")
        self.gaussian_frame.geometry('305x120')
        # creates the buttons frame inside the top-level frame
        self.button_frame = tk.Frame(self.gaussian_frame)
        self.button_frame.grid(row=1, column=0)
        # creates the 'ok' button inside the top-level frame
        self.ok_button = tk.Button(self.button_frame, text='  OK  ',
                                   command=self.get_gaussian_value)
        self.ok_button.grid(row=0, column=1, sticky='e', pady=10)
        # creates the 'cancel' button inside the top-level frame
        self.cancel_button = tk.Button(self.button_frame, text='Cancel',
                                       command=lambda: \
                                       self.gaussian_frame.destroy())
        self.cancel_button.grid(row=0, column=0, sticky='e', pady=10)
        # creates a scale bar inside the top-level frame
        # helps to set the desired contrast value
        self.gaussian_bar = tk.Scale(self.gaussian_frame, length=300,
                                     from_=0, to=100, orient='horizontal',
                                     tickinterval=25, width=20, sliderlength=20,
                                     variable = self.gaussian_radius)
        self.gaussian_bar.grid(row=0, column=0)
        # sets the default scale bar value to 0
        self.gaussian_bar.set(0)

    def get_gaussian_value(self):
        """
        these function retrieves the value from the scale bar and
        runs the gaussian blur function which applies the changes
        to the image
        """
        try:
            # gets the value from the scale bar widget
            self.radius = self.gaussian_radius.get()
            # closes the top-level after the user chooses a value and
            # presses the 'OK' button
            self.gaussian_frame.destroy()
            # applies the changes
            self.gaussian_blur()
        except:
            pass

    def gaussian_blur(self):
        """
        these function applies a gaussian blur filter to the image
        the difference between the blur filter and gaussian blur
        filter is that the gaussian blur radius is changeable
        """
        try:
            # modifies the image stored in the instance variable
            # applies the filter to the image
            self.image = self.image_reference.filter(ImageFilter.GaussianBlur
                                                     (radius=self.radius))
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_gaussian = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_gaussian
            self.image_label.configure(image=image_tk_gaussian)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def smooth_image(self):
        """
        these function applies a smoothing filter to the image
        """
        try:
            # modifies the image stored in the instance variable
            # applies the filter
            self.image = self.image_reference.filter(ImageFilter.SMOOTH)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_smooth = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_smooth
            self.image_label.configure(image=image_tk_smooth)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def find_edges(self):
        """
        these function identify the points in a digital image where
        the image brightness changes sharply
        """
        try:
            # modifies the image stored in the instance variable
            # detects the image edges
            self.image = self.image_reference.filter(ImageFilter.FIND_EDGES)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_edge = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_edge
            self.image_label.configure(image=image_tk_edge)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def image_contour(self):
        """
        these function detects the image contours
        """
        try:
            # modifies the image stored in the instance variable
            # detects the image contours
            self.image = self.image_reference.filter(ImageFilter.CONTOUR)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_contur = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_contur
            self.image_label.configure(image=image_tk_contur)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def help(self):
        """
        these function opens a .txt file and displays the
        text stored inside it
        """
        self.help_text = open('help.txt', 'r')
        text = self.help_text.read()
        tkinter.messagebox.showinfo(title="Help", message=text, icon="info")

    def about(self):
        """
        these function opens a .txt file and displays the
        text stored inside it
        """
        self.about_text = open('about.txt', 'r')
        text = self.about_text.read()
        tkinter.messagebox.showinfo(title="About", message=text, icon='info')




