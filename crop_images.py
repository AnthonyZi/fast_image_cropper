#!/usr/bin/env python3

from fast_image_cropper import Editor
import sys
import os
from collections import defaultdict

def exit_app(editor):
    editor.close_window()

def close_image(editor):
    pass

return_state_dict_editor = dict()
return_state_dict_editor["quit"] = close_image
return_state_dict_editor["exit"] = exit_app

def crop_image(editor, img_path_edit):
    editor.set_image(img_path_edit)
    returnstate = editor.open()
    return_state_dict_editor[returnstate](editor)


if __name__ == "__main__":
    editor = Editor()

    folder = "."

    imgs = [f for f in sorted(os.listdir(folder)) if any(ending in f for ending in [".png",".jpg"])]

    for img in imgs:
        crop_image(editor, img)
