function [a, b] = matric_course(image_path)
image = imread(image_path);

matric = getMatric(image);
course = getCourse(image);

a = matric;
b = course;
end

function x = getMatric(image)
matricSection = imcrop(image, [71.5 112.5 257 144]);

xmin = 0.5;
ymin = 0.5;
xIteration = 17.5;
yIteration = 14.3;
matricArray = [];

for row = 1:10
    switch row
        case 1
            column = 7;
            [matricIndex, lengthMarkRMeanval] = findIndex(matricSection, column, xmin, ymin, xIteration);
            
            if (lengthMarkRMeanval > 1)
                break
            else
                values = 'BCDFHLYX';
                matric = values(matricIndex);
            end
            
        case 2
            column = 15;
            [matricIndex, lengthMarkRMeanval] = findIndex(matricSection, column, xmin, ymin, xIteration);
            
            if (lengthMarkRMeanval > 1)
                break
            else
                values = 'ABCEFGIKMNPRSTYX';
                matric = values(matricIndex);
            end
            
        otherwise
            column = 10;
            [matricIndex, lengthMarkRMeanval] = findIndex(matricSection, column, xmin, ymin, xIteration);
            
            if (lengthMarkRMeanval > 1)
                break
            else
                values = '0123456789';
                matric = values(matricIndex);
            end      
    end
    
    matricArray = [matricArray, matric];
    ymin = ymin + yIteration;
end

x = matricArray;
end

function y = getCourse(image)
courseSection = imcrop(image, [75.5 340.5 503 105]);

xmin = 0.5;
ymin = 1.5;
xIteration = 19.5;
yIteration = 14.5;
courseArray = [];

for row = 1:7
    switch row
        case {1, 2}
            column = 26;
            [courseIndex, lengthMarkRMeanval] = findIndex(courseSection, column, xmin, ymin, xIteration);
            
            if (lengthMarkRMeanval > 1)
                break
            else
                values = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
                course = values(courseIndex);
            end     
            
        otherwise
            column = 10;
            [courseIndex, lengthMarkRMeanval] = findIndex(courseSection, column, xmin, ymin, xIteration);
            
            if (lengthMarkRMeanval > 1)
                break
            else
                values = '0123456789';
                course = values(courseIndex);
            end             
    end
    
    courseArray = [courseArray, course];
    ymin = ymin + yIteration;    
end

y = courseArray;
end

function [m, n] = findIndex(cropSection, c, xmin, ymin, xi)
width = 15;
height = 15;
meanvalArray = [];
rMeanvalArray = [];

for column = 1:c
    rect = [xmin ymin width height];
    option = imcrop(cropSection, rect);
    skeletonOption  = bwmorph(~option, 'open');
    meanval = mean2(~skeletonOption);
    meanvalArray = [meanvalArray, meanval];
    xmin = xmin + xi;
    
    rMeanval = round(meanval, 1);
    rMeanvalArray = [rMeanvalArray, rMeanval];
end

minMeanval = min(meanvalArray);
index = find(meanvalArray == minMeanval);

rMinMeanval = round(minMeanval, 1);
markRMeanval = find(rMeanvalArray - rMinMeanval == 0); 
lengthMarkRMeanval = length(markRMeanval);

m = index;
n = lengthMarkRMeanval;
end