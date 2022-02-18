
# JCAMO Pixelated Noise Camouflage Pattern Generator

I you want to use JCAMO's seamless camouflage pattern, this function will generate the image for you. This particular camouflage pattern is designed to be a macro/micro pattern composite that both breaks the silhouette at long distance using a heavy contrast macro pattern and uses a random confusion 3d-mimicking overlay for short distance. The motives of the pattern are shredded in order to blur the edges, while keeping the layered arrangemento of big,solid pixels when using low DPI parameter (less than 64 for this purpose) in order to keep modern military aesthetics and a low price printing method.

## Usage

Edit the parameters in the call to the function "jcamo"; then:

python3 jcamo.py


## Installation

python3 -m pip install PIL numpy matplotlib perlin_noise colormap cv2 noise

Then just download the source folder.

## License

Open/free use license for non-commercial, non-institutional use. See main file header.

## Examples

![jcamo_multiterrain_2022-02-17_14-16-42](https://user-images.githubusercontent.com/10059639/154687313-d6c4199d-eaeb-4c39-a379-ff73df949010.png)
