# swtor_mat_reader_addon
Python addon to read MAT files when importing an object in Blender

# SWTOR Material Linker

This add-on helps to automatically link a SWTOR model to its approprate textures, automatically adding the node set used for generic materials and populating it with the texture files found in the shader files. 

## So how does this work?

- Each SWTOR model is composed of one or more material slots
- Each material slot has a MAT shader of the same name present in the game files
- The MAT shader contains a list of textures and settings that form the model's appearance
- The add-on reads first the material name and goes off to find its MAT file in the directory you specified
- If it finds the MAT file, it will pull out the names of the diffuse, normal, and gloss map files (in-depth information here: https://github.com/SWTOR-Slicers/WikiPedia/wiki/swtor-materials-and-texture-files)
- It will go search for the DDS files whose names it got from the MAT files
- It will clean up the existing default shader from the Blender workspace, and instead re-create the material slot with the generic item node set that is created by the GR2 Importer (https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x)
- Lastly, it passes the file path of the textures to the appropriate node inputs, changing also some of the basic settings

## Installation

- Download the swtor_material_linker.zip from the repository. **Do NOT use Code > Download ZIP to get the contents of the repository**
- In Blender, go to Edit > Preferences > Add-Ons
- Select "Install" in the upper right corner. 
- Select the ZIP file you just downloaded and let Blender install the add-on
- You can find the add-on to enable by searching for "SWTOR" in Blender's add-on screen
- Once you enable the add-on, you will have the option to set your work directory. Your work directory is the directory where you extracted all the assets from the game archives. 

## Usage

Once you import a model, switch over to the **Shading** view, and then right click the node view. A menu entry for "Link Type" will give you the option to either run the add-on with the Principled Shader, or use the Uber Shader node set.

## Known Behavior And Recommendations

### Items only.

This add-on is suitable only for assets that contain non-wieldable items (furniture, decos, etc.) , architecture, environment, and vehicles. Nothing related to player characters is supported: weapons have been untested.

### This is a **full scene** process.

The add-on processes every model present on the scene. If you import characters alongside items, the character models will not have any textures, and, in fact, might lose those previously imported with it. 

There is a feature planned to implement the functionality to work only on selected models in a scehe. ETA: about two weeks (from 2021-12-07).

### Change the default work directory

Due to the fact my coding work is done on Windows, the default work directory has been set to C:\. Please change it for a faster look-up. Any look-ups done from the root of your drive is purely at your own risk (and at your patience): the look-up will take its time.

### No love for non-Windows users?

I haven't had the opportunity to test this add-on on a Linux or MacOS system. While theoretically it should work, I can't really guarantee it. Should you attempt to use this add-on on Linux or MacOS, and encounter problems, please reach out: I'd love to debug the use-case with you and make sure that this add-on works with other OSes as well.

### My Blender is freezing!

If there are a lot of materials, the Blender UI will freeze while the add-on works. It really doesn't seem to like this kind of bulk work, or I just made a bad job at optimizing for it. Either way, if you open the System Console via Window > Toggle System Console, you will see the add-on progress as the debug messages stream. As long as you get a steady stream of output, it's still working. If it stops, you either have a problem, or it finished. Go grab a cup of the beverage of your choice while it runs. :)

### There are no textures / no shader / insert other problem here!

The System Console is your friend (Window > Toggle System Console). The add-on outputs text messages for every step of work it does, so if there is any part of the process that encounters an error (no shaders found, no textures found, no node template, etc... ), it will be verbose about it. If in any doubt, feel free to reach out with an output from the system console, and possibly a screenshot or two of your work environment for troubleshooting.

### Principled or Uber?

The Principled Shader functionality is mostly there for historic reasons, as I had created this add-on before catching up to the work done by the others in the Slicer community in regards to replicating the accorate node sets. You *can* use it, but the results will be uglier, and will require more work before the item looks decent. This goes especially for items that have transparency on them.

### Pack external data for a happier asset transfer

Use File > External Data > Automatically Pack Into .blend to make sure that all the external textures that you fished out with the add-on get packed in the saved BLEND file. This means that, should you want to send an asset to another system, the BLEND comes with everything that makes up the asset.

## Support And Contact

Should you have any feedback, problem you need looked at, or general gripe, you can reach me over Discord at: Silver Ranger#5909
