import tkinter.filedialog
# Imports the file dialog module from Tkinter, used here to open file selection dialogs.

from unreal import (ToolMenuContext,
                    ToolMenus,
                    uclass,
                    ufunction,
                    ToolMenuEntryScript)
# Imports Unreal Engine's modules for tool menus and decorators. 
# These help create custom Unreal menu entries and define their behavior.

import os
import sys
import importlib
import tkinter
# Imports modules for path management, dynamic importing, and creating a Tkinter root window.

srcPath = os.path.dirname(os.path.abspath(__file__))
if srcPath not in sys.path:
    sys.path.append(srcPath)
# Sets the source path of the script and adds it to Python's search path (sys.path), 
# ensuring that any dependencies in the script's folder can be imported easily.

import UnrealUtilities
importlib.reload(UnrealUtilities)
# Imports a custom utility module (`UnrealUtilities`) and reloads it to ensure the latest version is used.

@uclass()
class BuilBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context: ToolMenuContext) -> None:
        UnrealUtilities.UnrealUtility().FindOrBuildBaseMaterial()
# Defines a class `BuilBaseMaterialEntryScript`, which inherits from `ToolMenuEntryScript`.
# The `execute` function overrides the parent class method to run `FindOrBuildBaseMaterial` from `UnrealUtilities`,
# which creates or finds a base material in Unreal.

@uclass()
class LoadMeshEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context) -> None:
        window = tkinter.Tk()
        window.withdraw()
        importDir = tkinter.filedialog.askdirectory()
        window.destroy()
        UnrealUtilities.UnrealUtility().ImportFromDir(importDir)
# Defines the `LoadMeshEntryScript` class to handle importing meshes.
# The `execute` function opens a file dialog for the user to select a directory of meshes to import.
# `UnrealUtilities.UnrealUtility().ImportFromDir(importDir)` then processes the directory for mesh importation.

class UnrealSubstancePlugin:
    def __init__(self):
        self.submenuName="UnrealSubatancePlugin"
        self.submenuLabel="Unreal Substance Plugin"
        self.CreateMenu()
# Initializes the main plugin class `UnrealSubstancePlugin` with a submenu name and label.
# Calls `CreateMenu` to set up the menu in the Unreal Engine editor.

    def CreateMenu(self):
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")
        # Retrieves the main menu from Unreal's `LevelEditor`.

        existing = ToolMenus.get().find_menu(f"LevelEditor.MainMenu.{self.submenuName}")
        if existing:
            ToolMenus.get().remove_menu(existing.menu_name)
        # Checks if a submenu with the same name already exists. 
        # If it does, it removes it to avoid duplicates.

        self.submenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", self.submenuName, self.submenuLabel)
        # Adds a new submenu to the main menu with the specified name and label.

        self.AddEntryScript("BuildBaseMaterail", "Build Base Material", BuilBaseMaterialEntryScript())
        self.AddEntryScript("LoadFromDirectory", "Load From Directory", LoadMeshEntryScript())
        # Adds two custom entries to the submenu by calling `AddEntryScript` for each functionality.

        ToolMenus.get().refresh_all_widgets()
        # Refreshes all tool menu widgets to ensure the new submenu and options are displayed.

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):
        script.init_entry(self.submenu.menu_name, self.submenu.menu_name, "", name, label)
        script.register_menu_entry()
# The `AddEntryScript` method sets up a menu entry within the submenu by initializing it with a name and label,
# and then registering it so that it appears in the menu.

UnrealSubstancePlugin()
# This Initializes the plugin.