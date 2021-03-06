#!/usr/bin/env python
# 
# Take a set of view images and place them in a single standard quilt image.
# 
# https://forum.lookingglassfactory.com/t/combining-32-views/501/2
# The views go from the bottom left as the leftmost view, to the top right being the furthest right
# E.g. for a 4x8 quilt:
# 
# 28  29  30  31
# 24  25  26  27
# 20  21  22  23
# 16  17  18  19
# 12  13  14  15
#  8   9  10  11
#  4   5   6   7
#  0   1   2   3
#  
#
# Copyright (c) 2019, SURFsara BV
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of SURFsara BV nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SURFSARA BV BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys, random, colorsys
from PIL import Image, ImageDraw

def usage():
    print('usage: %s <quilt-image> <tiles-h> <tiles-v> <tile-pattern> <first> <last>' % sys.argv[0])
    print()
    sys.exit(-1)

if len(sys.argv) != 7:
    usage()
    
quilt_image_file = sys.argv[1]
tiles_h = int(sys.argv[2])
tiles_v = int(sys.argv[3])
tile_pattern = sys.argv[4]
tile_first = int(sys.argv[5])
tile_last = int(sys.argv[6])

# Open a tile image to get resolution
tile_img = Image.open(tile_pattern % tile_first)

tile_w, tile_h = tile_img.size

quilt_w = tile_w * tiles_h
quilt_h = tile_h * tiles_v

print('Quilt size based on tile dimensions and count: %d x %d' % (quilt_w, quilt_h))

# https://www.geeksforgeeks.org/smallest-power-of-2-greater-than-or-equal-to-n/
def nextPowerOf2(n): 
    count = 0;
    # First n in the below  
    # condition is for the  
    # case where n is 0 
    if (n and not(n & (n - 1))): 
        return n 
      
    while( n != 0): 
        n >>= 1
        count += 1
      
    return 1 << count

quilt_w = nextPowerOf2(quilt_w)
quilt_h = nextPowerOf2(quilt_h)
print('Quilt size: %d x %d' % (quilt_w, quilt_h))

outimg = Image.new('RGB', (quilt_w, quilt_h))

tile_idx = tile_first
tile_top = quilt_h - tile_h

for j in range(tiles_v):
    
    tile_left = 0
    
    for i in range(tiles_h):

        tile_img = Image.open(tile_pattern % tile_idx)
        
        outimg.paste(tile_img, (tile_left, tile_top))

        tile_idx += 1
        tile_left += tile_w
        
    tile_top -= tile_h
        
outimg.save(quilt_image_file)
