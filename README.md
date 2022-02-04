# upsidedown-postman
GGJ2022 postman game

## Credits
Thanks to Tim Pulin for sprite graphics!

Thanks to Thomas M for sound effects!

## Creating a Class/Library file
Create the file in lib such as `lib/example_class_file.py`.  Then add to the `lib/__init__.py` the name of the file to the import line.
Fore example `from . import utility, loader, player, example_class_file`.  This will allow you to use:
`from lib import example_class_file` in any other file.

## Saving Assets
save assets to `[project_root]/assets` (can be sub folders)

## Loading Assets
We are going to need to load assets in a special way for the building of the exe.  The `create_resource_path` in `lib/utility.py` 
will do the needful to accomplish this.  To simplify loading assets back down to one line a `lib/loader.py` was implemented to 
wrap this functionality.  Currently only `load_image` is implemented but as we need to load different assets (sprites, sounds, etc...) 
just make a new method in `lib/loader.py` for that type.  For example:
```python
def load_image(image_path):
    image = util.create_resource_path(image_path)
    return pygame.image.load(image).convert()
```
Then call it similar to how `load_image` is called:
```python
from lib import loader
background_image = loader.load_image("assets/images/paperboy.jpg")
```

## Building into an exe
Execute the following commands from the `[project_root]`
```
pyinstaller --onefile .\__init__.py --paths '.\' --exclude-module _bootlocale --add-data 'assets/;assets/' --name 'StarCrash'
```
This will generate the executable. 
If you want to further edit the build without running the whole command, you can edit the spec file that is created and run it like so:
```
pyinstaller .\__init__.spec
```
[Here](https://stackoverflow.com/questions/54210392/how-can-i-convert-pygame-to-exe) is the stack overflow for all of the above process
