# main.py

import argparse
from pyfiglet import Figlet
from libido import Libido
from swiper import Swiper

CURRENT_PREDICTION_MODEL = 'trained_models/5fbd352c-adac-11ea-89e4-cc2f71f824a0.pth'
DATA = 'data/raw'
DATA_TEST = 'data/test'
DATA_TRAIN = 'data/train'

# Temporary test folders
_DATA_TRAIN = 'data/sorted'
_DATA_TEST = 'data/sorted/test'
_DATA = ''

def main():
	
	parser = argparse.ArgumentParser(description='Train a model to pick the right partners for you.')

	parser.add_argument("mode", type=str, choices=["train", "test", "infer", "data"], help="choose between train, infer and data modes")
	parser.add_argument("--train-data-dir", type=str, default=_DATA_TRAIN, help="imagenet-style train data directory; defaults to 'data/train'")
	parser.add_argument("--test-data-dir", type=str, default=_DATA_TEST, help="imagenet-style test data directory; defaults to 'data/test'")
	parser.add_argument("--save-data-dir", type=str, default=_DATA, help="directory in which the two class folders (left and right) will be created; defaults to 'data/raw'")


	args = parser.parse_args()

	f = Figlet(font='slant')
	print(f.renderText('The Wing Man'))

	if args.mode == "train":
		print("-> Now entering training mode")
		print("Current training folder: " + _DATA_TRAIN)
		predictor = Libido(train_data_dir=_DATA_TRAIN, pretrained=True, feature_extraction=True)
		predictor.train_model()

	elif args.mode == "test":
		tester = Libido(pretrained=True, feature_extraction=True)
		tester.show_pretrained_model(CURRENT_PREDICTION_MODEL)

	elif args.mode == "infer":

		# Instantiate swiper object
		swiper = Swiper()

		libido = Libido(pretrained=True, feature_extraction=True)
		libido.load_pretrained(CURRENT_PREDICTION_MODEL)

		swiper.smart_swipe(libido.model_ft, libido.data_transforms['test'])
		exit()

		# Facebook login
		if swiper.fb_login():

			# If valid, Tinder login
			if swiper.tinder_login:

				print("-> Now entering inference mode")

				# Load the model
				tester = Libido(pretrained=True, feature_extraction=True)

				# Pass model to swiper object's smart_swipe
				Swipe.smart_swipe(tester.model_ft, tester.data_transforms['test'])



			else:
				print('Tinder login failed')

		else:
			print('Facebook login failed')

	elif args.mode == "data":
		print("-> Now entering data extraction mode")
		# TODO
	exit()

if __name__ == '__main__':
    main()