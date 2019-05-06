# Normalmap-Calculator
This python script is used to calculate a normal map from a 2D image.

## Comment on usage
I use this tool to create a kind of preview of a material.
It helps you to choose the style the material should have.
It could be more precise, but it's fast.

## How it works
The first step is to generate a grayscale.
For the next part it uses the sobel operator for edge detection.
With the help of linear algebra and numpy this data is used to calculate the normalmap.

## Example
Stone surface photographed and modified by me.

### input
![input](Example/demo.png)

### output
![output](Example/demo_nrm.png)

### Complete material, with circling lightsource
![Complete material, with circling lightsource](Example/showcase.gif)
