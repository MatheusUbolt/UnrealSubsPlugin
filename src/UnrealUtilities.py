from unreal import(AssetToolsHelpers,
                   EditorAssetLibrary,
                   AssetTools,
                   Material,
                   MaterialFactoryNew,
                   MaterialEditingLibrary,
                   MaterialExpressionTextureSampleParameter2D as TexSample2D,
                   MaterialProperty,
                   AssetImportTask,
                   FbxImportUI)
# Imports Unreal Engine modules and classes for asset tools, materials, material editing, import tasks, and FBX import settings.

import os
# Imports the `os` module for file and directory operations.

class UnrealUtility:
    def __init__(self):
        self.substanceRooDir='/game/Substance/'
        self.substanceBaseMatName = 'M_SubstanceBase'
        self.substanceBaseMatPath = self.substanceRooDir + self.substanceBaseMatName
        self.substanceTempFolder='/game/Substance/temp'
        self.baseColorName = "BaseColor"
        self.normalName = "Nomral"
        self.occRoughnessMetalic = "OcclusionRoughnessMetalic"
# Initializes the `UnrealUtility` class with various paths and parameter names, setting up default paths for materials and temporary files.

    def GetAssetTools(self)->AssetTools:
        return AssetToolsHelpers.get_asset_tools()
    # Defines a helper function to retrieve the Unreal Asset Tools, a utility for handling asset creation, import, and modification.

    def ImportFromDir(self, dir):
        for file in os.listdir(dir):
            if ".fbx" in file:
                self.LoadMeshFromPath(os.path.join(dir, file))
    # Loops through all files in the provided directory (`dir`). If an `.fbx` file is found, it calls `LoadMeshFromPath` to import the mesh.

    def LoadMeshFromPath(self, meshPath):
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "")
        # Extracts the file name without extension for the asset name in Unreal.

        importTask = AssetImportTask()
        importTask.replace_existing = True
        importTask.filename = meshPath
        importTask.destination_path = '/game/' + meshName
        importTask.automated=True
        importTask.save=True
        # Configures an `AssetImportTask` for importing the mesh. Sets properties like destination, automation, and saving behavior.

        fbxImportOption = FbxImportUI()
        fbxImportOption.import_mesh=True
        fbxImportOption.import_as_skeletal=False
        fbxImportOption.import_materials=False
        fbxImportOption.static_mesh_import_data.combine_meshes=True
        importTask.options = fbxImportOption
        # Sets up `FbxImportUI` options for the import task, configuring the import to treat the file as a static mesh without materials.

        self.GetAssetTools().import_asset_tasks([importTask])
        # Executes the import task using Unreal's asset tools.

        return importTask.get_objects()[0]
# Returns the imported mesh object.

    def FindOrBuildBaseMaterial(self):
        if EditorAssetLibrary.does_asset_exist(self.substanceBaseMatPath):
            return EditorAssetLibrary.load_asset(self.substanceBaseMatPath)
        # Checks if the base material asset already exists. If it does, loads and returns the existing asset.

        baseMat = self.GetAssetTools().create_asset(self.substanceBaseMatName, self.substanceRooDir, Material, MaterialFactoryNew())
        # Creates a new base material asset in the Substance directory if it doesn’t exist.

        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0)
        baseColor.set_editor_property("parameter_name", self.baseColorName)
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)
        # Adds a `BaseColor` parameter to the material. Sets its position in the material editor and connects it to the `BaseColor` property.

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400)
        normal.set_editor_property("parameter_name", self.normalName)
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)
        # Adds a `Normal` map parameter. Sets the default normal texture and connects it to the material’s normal property.

        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800)
        occRoughnessMetalic.set_editor_property("parameter_name", self.occRoughnessMetalic)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC)
        # Adds an `OcclusionRoughnessMetallic` map to the material, with RGB channels corresponding to ambient occlusion, roughness, and metallic properties.

        EditorAssetLibrary.save_asset(baseMat.get_path_name())
        return baseMat
    # Saves the new base material asset and returns it.