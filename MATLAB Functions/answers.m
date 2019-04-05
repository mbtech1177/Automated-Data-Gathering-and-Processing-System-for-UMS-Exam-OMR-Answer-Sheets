function x = answers(image_path, total_questions)
image = imread(image_path);
answersSection = imcrop(image,[77.5 452.5 481 378]);

width = 11;
height = 11;
xIteration = 17.5;
yIteration = 14.9;
answersArray = [];

for row = 1:total_questions
    meanvalArray = [];
    rMeanvalArray = [];
    
    if (row >= 1) && (row <= 25)
        xmin = 21.5;
        
        if (row == 1)
            ymin = 6.5;
        end
        
    elseif (row >= 26) && (row <= 50)
        xmin = 147.5;
        
        if (row == 26)
            ymin = 4.5;
        end
        
    elseif (row >= 51) && (row <= 75)
        xmin = 269.5;
        
        if (row == 51)
            ymin = 4.75;
        end
         
    elseif (row >= 76) && (row <= 100)
        xmin = 395;
        
        if (row == 76)
            ymin = 2.75;
        end
    end  
    
    for column = 1:5
        rect = [xmin ymin width height];
        option = imcrop(answersSection, rect);
        skeletonOption  = bwmorph(~option, 'open');
        meanval = mean2(~skeletonOption);
        meanvalArray = [meanvalArray, meanval];
        xmin = xmin + xIteration;
        
        rMeanval = round(meanval, 1);
        rMeanvalArray = [rMeanvalArray, rMeanval];
    end 
    
    minMeanval = min(meanvalArray);
    rMinMeanval = round(minMeanval, 1);
    markRMeanval = find(rMeanvalArray - rMinMeanval == 0);
    lengthMarkRMeanval = length(markRMeanval);    
    
    if (lengthMarkRMeanval > 1)
        answer = 'X';
    else
        answerIndex = find(meanvalArray == minMeanval);
    
        values = 'ABCDE';
        answer = values(answerIndex);
    end
    
    answersArray = [answersArray, answer];
    ymin = ymin + yIteration;
end

x = answersArray;
end