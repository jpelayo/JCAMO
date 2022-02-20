###########################################
# Created By  : jcamo at infinitecontext dot com
# Created Date: 17 Feb 2022
# version = 0.1.0
# Pixelated Noise Camouflage Pattern Generator
# (c) 2022 jcamo at infinitecontext dot com
# Author attribution requested
###########################################
# Permission is hereby granted, free of charge, to any non-commercial, non-institutional user obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish and distribute copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: the above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software; mention to "jcamo at infinitecontext dot com" shall be included in derived artwork.
#
#For commercial or institutional use, contact by email: jcamo at infinitecontext dot com
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###########################################


from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from perlin_noise import PerlinNoise
from colormap import rgb2hex
from pathlib import Path
import random
import string
import time
import json
from datetime import datetime
import cv2
import noise
import os
import argparse

def random_num(length):
	digits = string.digits
	result_str = ''.join((random.choice(digits) for i in range(length)))
	return int(result_str)

def picmaker1(xpix,ypix, octaves=[3,6,12,24], granul=[0.5,0.25,0.5]):
	val = max (xpix,ypix)
	noise1 = PerlinNoise(octaves=octaves[0],seed=random_num(16))
	noise2 = PerlinNoise(octaves=octaves[1],seed=random_num(16))
	noise3 = PerlinNoise(octaves=octaves[2],seed=random_num(16))
	noise4 = PerlinNoise(octaves=octaves[3],seed=random_num(16))
	pict = []
	for i in range(val):
		row = []
		for j in range(val):
			noise_val = noise1([i/val, j/val])
			noise_val += granul[0] * noise2([i/val, j/val])
			noise_val += granul[1] * noise3([i/val, j/val])
			noise_val += granul[2] * noise4([i/val, j/val])
			row.append(noise_val)
		pict.append(row)
		if j>=ypix or i>= xpix: return pict

	return pict

def getcolortuple(name):
	with open('palette.json', 'r') as f:
		data = json.load(f)
	return (data['colors'][name][0],data['colors'][name][1],data['colors'][name][2])

def cmapmaker(zone, v, cuts):
	global palette

	with open('palette.json', 'r') as f:
		data = json.load(f)

	name = "macro1"
	macro1 = rgb2hex(data['colors'][data['palettes'][zone][name]][0], data['colors'][data['palettes'][zone][name]][1], data['colors'][data['palettes'][zone][name]][2])
	name = "macro2"
	macro2 = rgb2hex(data['colors'][data['palettes'][zone][name]][0], data['colors'][data['palettes'][zone][name]][1], data['colors'][data['palettes'][zone][name]][2])
	name = "micro1"
	micro1 = rgb2hex(data['colors'][data['palettes'][zone][name]][0], data['colors'][data['palettes'][zone][name]][1], data['colors'][data['palettes'][zone][name]][2])
	name = "micro2"
	micro2 = rgb2hex(data['colors'][data['palettes'][zone][name]][0], data['colors'][data['palettes'][zone][name]][1], data['colors'][data['palettes'][zone][name]][2])

	lim = 0.000000000000001

	if cuts[2] == 0.0 :
		cmap = LinearSegmentedColormap.from_list('JCAMO',
	                                        [(0, macro1),
	                                         (cuts[1], macro1),
	                                         (cuts[1]+lim, macro2),
	                                         (1, macro2)])
	elif cuts[1] == 0.0 :
		cmap = LinearSegmentedColormap.from_list('JCAMO',
	                                        [(0, micro2),
	                                         (0+lim, micro2),
	                                         (cuts[2], micro2),
	                                         (1, micro2)])
	elif cuts[0] == 0.0 :
		cmap = LinearSegmentedColormap.from_list('JCAMO',
	                                        [(0, micro1),
	                                         (0+lim, micro1),
	                                         (cuts[1], micro1),
	                                         (1, micro1)])
	else:
		cmap = LinearSegmentedColormap.from_list('JCAMO',
	                                        [(0, macro1),
	                                         (cuts[0], macro1),
	                                         (cuts[0]+lim, macro2),
	                                         (cuts[1], macro2),
	                                         (cuts[1]+lim, micro1),
	                                         (cuts[2], micro1),
	                                         (cuts[2]+lim, micro2),
	                                         (1, micro2)])

	if v >0 : cmap.set_under(alpha=0)
	return cmap

def genimage(name,vm,dp=24,zone="multiterrain",c=[0.3,0.5,0.75], height=200, width=200, oct=[3,6,12,24], g=[0.5,0.25,0.5]):
	plt.imshow(picmaker1(height,width,octaves=oct,granul=g), cmap=cmapmaker(zone,v=vm,cuts=c), vmin = vm)
	plt.axis('off')
	plt.savefig(name, dpi=dp, transparent=True, pad_inches=0, bbox_inches='tight')
	plt.clf()
	return str(Path(__file__).parent.absolute()) + "/" + name

def specklenoise(imagefile):
	img = cv2.imread(imagefile)
	gauss = np.random.normal(0,1,img.size)
	gauss = gauss.reshape(img.shape[0],img.shape[1],img.shape[2]).astype('uint8')
	noise = img + img * gauss
	cv2.imwrite(imagefile, noise)

def gaussnoise(imagefile):
	img = cv2.imread(imagefile)
	gauss = np.random.normal(0,1,img.size)
	gauss = gauss.reshape(img.shape[0],img.shape[1],img.shape[2]).astype('uint8')
	img_gauss = cv2.add(img,gauss)
	cv2.imwrite(imagefile, img_gauss)

def offsetter(imagename,right,down):
	M = np.float32([
	[1, 0, right],
	[0, 1, down]
	])
	g = getcolortuple("shadow")
	fore = Image.open(imagename)
	image = cv2.imread(imagename)
	shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
	#newname = imagename.replace(".png","")+"_shifted.png"

	h, w, c = shifted.shape
	image_bgra = np.concatenate([shifted, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
	white = np.all(shifted == [255, 255, 255], axis=-1)
	image_bgra[white, -1] = 0
	black = np.all(shifted == [0, 0, 0], axis=-1)
	image_bgra[black, -1] = 0

	img = Image.fromarray(image_bgra)
	width = img.size[0]
	height = img.size[1]
	for i in range(0,width):# process all pixels
		for j in range(0,height):
			data = img.getpixel((i,j))
			if (data[0]!=255 and data[1]!=255 and data[2]!=255 and data[0]!=0 and data[1]!=0 and data[2]!=0): img.putpixel((i,j),g)

	composed = Image.alpha_composite(img,fore)
	composed.save(imagename)
	return composed

def jcamo(res=24,seamless=False, h=200, w=200, palette="multiterrain", dodelete=False):

	g = 0.2

	i1 = genimage('background.png', zone=palette, dp=res, vm=0.0, c=[0.0,0.07,0.0], height=h, width=w, oct=[6,12,16,72], g=[0.5,0.25,0.5])
	i2 = genimage('foreground1.png', zone=palette, dp=res, vm=g, c=[g,0.0,0.66], height=h, width=w, oct=[12,16,72,96], g=[0.5,0.25,0.5])
	i3 = genimage('foreground2.png', zone=palette, dp=res, vm=g, c=[0.0,g,0.66], height=h, width=w, oct=[12,16,72,96], g=[0.5,0.25,0.5])

	dtx = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	background = Image.open(i1)
	#foreground1 = Image.open(i2)
	#foreground2 = Image.open(i3)
	foreground1 = offsetter(i2,1,1)
	foreground2 = offsetter(i3,1,1)
	mid = str(Path(__file__).parent.absolute()) + "/" + "aux.png"
	tile = str(Path(__file__).parent.absolute()) + "/" + "tile.png"
	final = str(Path(__file__).parent.absolute()) + "/jcamo_" + palette + "_" + dtx + ".png"
	Image.alpha_composite(background, foreground1).save(mid)
	tile0 = Image.alpha_composite(Image.open(mid), foreground2)

	if seamless:
		tile0.save(tile)
		flip1 = tile0.transpose(Image.FLIP_LEFT_RIGHT)
		combo1 = Image.new('RGB', (tile0.width + flip1.width, tile0.height))
		combo1.paste(tile0, (0, 0))
		combo1.paste(flip1, (tile0.width, 0))
		flip11 = combo1.transpose(Image.FLIP_LEFT_RIGHT)
		combo11 = Image.new('RGB', (combo1.width + flip11.width, combo1.height))
		combo11.paste(combo1, (0, 0))
		combo11.paste(flip11, (combo1.width, 0))
		combo11.save(final)
	else:
		tile0.save(final)

	if dodelete and os.path.exists(i1): os.remove(i1)
	if dodelete and os.path.exists(i2): os.remove(i2)
	if dodelete and os.path.exists(i3): os.remove(i3)
	if dodelete and os.path.exists(mid): os.remove(mid)
	if dodelete and os.path.exists(tile): os.remove(tile)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dpi", type=int, help="resolution as DPI 32 64 72 150 300")
parser.add_argument("-y", "--height", type=int, help="composing field height that is affected by DPI")
parser.add_argument("-x", "--width", type=int, help="composing field width that is affected by DPI and tile copy")
parser.add_argument("-p", "--palette", type=str, help="name of the color palette in the json to use")
parser.add_argument("-s", "--seamless", type=int, help="0 1 boolean to compose 4 tiles horizontally")
parser.add_argument("-e", "--delete", type=int, help="0 1 boolean to remove temporary files")
args = parser.parse_args()

ires = 64
if args.dpi is not None and int(args.dpi) > 0: ires = int(args.dpi)
ih = 400
if args.height is not None and int(args.height) > 0: ih = int(args.height)
iw = 1200
if args.width is not None and int(args.width) > 0: iw = int(args.width)
ip = "desert"
if args.palette is not None: ip = str(args.palette)
ise = True
if args.seamless is not None and int(args.seamless) >= 0: ise = bool(int(args.seamless))
idel = True
if args.delete is not None and int(args.delete) >= 0: idel = bool(int(args.delete))


#Current palettes available: see palette.json
jcamo(res=ires, h=ih, w=iw, palette=ip, seamless=ise, dodelete=idel)
