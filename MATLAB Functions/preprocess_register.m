function x = preprocess_register(image_path)
image = imread(image_path);
grayImage = rgb2gray(image);
binaryImage = imbinarize(grayImage, 0.95);
[height, width] = size(binaryImage);

col = 1;
row = 121; 
found = false;

while(found == false)
    if (width - col >= 4)
        if (height - row >= 4)
            val1 = binaryImage(row, col);

            if (val1 == 0)
                val2 = binaryImage(row, col + 1);
                val3 = binaryImage(row, col + 2);
                val4 = binaryImage(row, col + 3);
                val5 = binaryImage(row, col + 4);
                val6 = binaryImage(row + 1, col);
                val7 = binaryImage(row + 2, col);
                val8 = binaryImage(row + 3, col);
                val9 = binaryImage(row + 4, col);

                if (val2 == 0 && val3 == 0 && val4 == 0 && val5 == 0 && val6 == 0 && val7 == 0 && val8 == 0 && val9 == 0)
                    cropImage = imcrop(binaryImage, [col row width-col height-row]);
                    [height2, width2] = size(cropImage);
                    whiteSect = imcrop(cropImage, [192.5 35.5 69 176]);
                    mean = round(mean2(whiteSect), 2);

                    if ((height2 >= 712) && (width2 >= 559) && (mean == 0.99 || mean == 1))
                        found = true;

                    else
                        [col, row] = cont(col, row, width);

                    end
                else
                    [col, row] = cont(col, row, width);

                end  
            elseif (val1 == 1)
                [col, row] = cont(col, row, width);

            end
        else
            break;
            
        end
    else
        col = 1;
        row = row + 1;

    end
end

if (found == true)
    imwrite(cropImage, image_path);
    x = image_path;
    
elseif (found == false)
    x = 'FAILED';
    
end
end

function [a, b] = cont(col, row, width)
if (col < width)
    col = col + 1;
            
elseif (col == width)
    col = 1;
    row = row + 1;
            
end

a = col;
b = row;
end