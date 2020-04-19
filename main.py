# main.py

import argparse
from pyfiglet import Figlet

DATA = 'data/raw'
DATA_TEST = 'data/test'
DATA_TRAIN = 'data/train'

parser = argparse.ArgumentParser(description='Train a model to pick the right partners for you.')

parser.add_argument("mode", type=str, choices=["train", "test", "infer", "data"], help="choose between train, infer and data modes")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("--train-data-dir", help="imagenet-style train data directory; defaults to 'data/train'")
parser.add_argument("--test-data-dir", help="imagenet-style test data directory; defaults to 'data/test'")
parser.add_argument("--save-data-dir", help="directory in which the two class folders (left and right) will be created; defaults to 'data/raw'")


args = parser.parse_args()

if args.verbose:
	f = Figlet(font='slant')
	print(f.renderText('The Wing Man'))

if args.mode == "train":
	print("-> Now entering training mode")
	predictor = Libido()
    predictor.train_model(pretrained=True, feature_extraction=True)



if args.mode == "infer" or args.mode == "data"

	# Instantiate swiper object
	swiper = Swiper()

	# Facebook login
    if swiper.fb_login():
        
    	# If valid, Tinder login
        if swiper.tinder_login:
			print("-> Now entering inference mode")
			print("-> Now entering data extraction mode")

		else:
        print('Tinder login failed')
        return -1

	else:
        print('Facebook login failed')
        return -1

    return 1