# The Wing Man

The Wing Man aspires to be an intelligent Tinder web swiper. It logs into Tinder through your Facebook account.

The project has been tested by parts and is to be assembled into a pipeline.
The following list describes each of the project's parts and their respective roles.
Many of these parts and functions lack robustness.

- `main.py`: Sandbox, used for debugging, testing routines from different libraries, treating training data and trianing the models.
- `data.py`: Library with various functions for dataset treatment. Functions that take the `folder` parameter as input function in place, overwriting existing data.
  - `rename(folder)`: Renames all files in `folder` to 1,2 ... n.jpg in ascending order;
  - `convert(folder)`: Converts every picture inside `folder` to jpg;
  - `remove_duplicates(folder)`: Removes duplicates according to hash key;
  - `crop_to_square(folder)`: Crops every picture in `folder` to a square from the center outwards, side of the square being the picture's smallest side.
  - `resize(src, dst, w, h)`: Resizes pictures from `src` to `des` folder, with dimensions `w x h`
  - `split(folder, ratio)`: Give a `folder` with [class_1, class_2, ..., class_n] folder, splits the data into [train, test] according to `ratio`.
- `swiper.py`: Responsible for dealing with Facebook and Tinder logins and different modes of swiping.
_Disclaimer - some of the code in this file was not written by me, but I lost the source. If you come across the original please let me know so I can credit the programmer_
  - `dumb_swipe()`: Simply swipes right indefinetly.
  - `data_extraction(just_data=False)`: Allows the user to swipe `left` or `right` using keys `1` and `2`, which in turn saves pictures into the corresponding folder once swiped. The `just_data` flag allows the user to save pictures in correct label folder without actually swiping right on Tinder itself, to avoid running out of "likes".
- `neural.py`: Contains the "predicting" logic of the program. The correpondent `Libido()` object inside allows the user to train, visualize and save prediction models to be used later for automatic swiping.
