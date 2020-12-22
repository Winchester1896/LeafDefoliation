how to use it

The exe file is under the path "dist\leaf_labelling\leaf_labelling.exe".

The first selection is for a txt file containing defoliation labels (i.e. leaf_classes.txt).

The second selection is for the image folder containing all raw images that needs to be cropped and classified (In the tool, 
you need to hold and drag your mouse to select an area, select a defoliation rate on the right and hit the apply button).

The third selection is for a folder to contain the final output file that contains all the areas and labels.


In the tool, you will see an image on the left, leaf defoliation selections on the right and three buttons(cancel, apply, and next) at the bottom.
option1 and option2 buttons are not used in this tool, just ignore them.
The basic procedure is that:
	1. select an area in the image(a bounding box in red)
	2. select the correct defoliation rate on the right
	3. click the "Apply" button to finalize the label for this area(the bounding box will turn green with defoliation rate written in it)
	4. drag the two scroll bars for the image to select other areas in the image and do step 1 to step 3
	5. Once you finish labeling the current image, you can click the "Next" button to label the next image in the folder
	6. The "Next" button will turn into "Finish" when you get to the last image in the folder. After labeling for the last image, click
		the "Finish" button will close the program

All I need is the output file that should be named "dataset.txt" located in the third selection path you choose.