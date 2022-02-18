
# JCAMO Pixelated Noise Camouflage Pattern Generator

I you want to use JCAMO's seamless camouflage pattern, this function will generate a new, unique, randomized image for you. This particular camouflage pattern is a 5 color (2 for macro, 2 for micro, 1 for shadow) computer generated image designed to be a macro/micro pattern composite that both breaks the silhouette at long distance by employing a heavy contrast macro pattern, and uses a random confusion 3d-mimicking overlay for short distance concealment. The motives of the pattern are shredded in order to blur the edges, while keeping the layered arrangement of big, solid pixels when using a low DPI function parameter (less than 64 for this purpose) in order to keep modern military aesthetics and a low price printing method.

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

## Dedication

To the Spanish Army (I don't like our woodland pixel camo; it is a micro-only dark mix).
