# upsidedown-postman
GGJ2022 postman game

## Saving Assets
save assets to `[project_root]\assets` (can be sub folders)

## Loading Assets
We are going to need to load assets in a special way for the building of the exe.  The `create_resource_path` in `lib\utility.py` 
will do the needful to accomplish this.  To simplify loading assets back down to one line a `lib\loader.py` was implemented to 
wrap this functionality.  Currently only `load_image` is implemented but as we need to load different assets (sprites, sounds, etc...) 
just make a new method in `lib\loader.py` for that type.  For example:
```python
def load_image(image_path):
    image = util.create_resource_path(image_path)
    return pygame.image.load(image).convert()
```
Then call it similar to how `load_image` is called:
```python
from lib import loader
background_image = loader.load_image("assets\images\paperboy.jpg")
```

## Building into an exe
Execute the following commands from the `[project_root]`
```
pyinstaller --onefile .\__init__.py --exclude-module _bootlocale --add-data 'assets/;assets/'  
```
wait for this to complete.  Then execute:
```
pyinstaller .\__init__.spec
```
[Here](https://stackoverflow.com/questions/54210392/how-can-i-convert-pygame-to-exe) is the stack overflow for all of the above process