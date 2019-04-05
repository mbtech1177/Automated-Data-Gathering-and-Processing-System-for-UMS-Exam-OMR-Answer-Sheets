function x = preprocess_register(image_path, template_path)
image = imread(image_path);
grayImage = rgb2gray(image);
template = imread(template_path);
grayTemplate = rgb2gray(template);

[optimizer, metric] = imregconfig('multimodal');
optimizer.MaximumIterations = 400;
alignedImage = imregister(grayImage, grayTemplate, 'similarity', optimizer, metric);

binaryImage = imbinarize(alignedImage, 0.90);
imwrite(binaryImage, image_path);

x = image_path;
end