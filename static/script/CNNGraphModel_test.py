import json
from collections import OrderedDict

def mapping():
    jsonPath = "C:/Users/Rosenblatt/Desktop/model.json"

    c = 0
    with open(jsonPath, "r") as data_file:
        data = json.load(data_file)
    f = 0
    posX = 300
    posY = 550
    gmodel = "{ \n"
    for i in range(len(data["config"])):
        if (i % 6 is 0):
            posY = 550
            posX = posX + 140
        
        opT = data["config"][i]["class_name"]
        posY = posY + 100
        posX = posX + 20
        f = i + 1

        if i is 0:
            gmodel = gmodel + "     \"op_0" + "\" : {\n"
            gmodel = gmodel + "         \"dimention_ordering\": \"default\",\n"
            gmodel = gmodel + "         \"operator_title\": \"InputLayer\",\n"
            # inS = str(inSape[1:3])
            # gmodel = gmodel + "         \"input_shape\": \"" + inS + "\",\n"
            gmodel = gmodel + "         \"input_port\": \"input_port\",\n"
            gmodel = gmodel + "         \"left\": \"" + str(posX) + "\",\n"
            gmodel = gmodel + "         \"top\": \"" + str(posY) + "\"\n"
            gmodel = gmodel + "         },\n"

        if 'Conv2D' in opT:
            # NM = data["config"][i]["config"]["name"]
            # if "conv2d_1" == NM:
                # inSape = data["config"][i]["config"]["batch_input_shape"]
                
            Stride = data["config"][i]["config"]["strides"]
            Filters = data["config"][i]["config"]["filters"]
            kernelSize = data["config"][i]["config"]["kernel_size"]
            Activation = data["config"][i]["config"]["activation"]

            gmodel = gmodel + "     \"op_" + str(i + 1) + "\" : {\n"
            gmodel = gmodel + "         \"regularizer_for_input_weight\": \"None\",\n"
            gmodel = gmodel + "         \"number_of_filters\": \"" + str(Filters) + "\",\n"
            gmodel = gmodel + "         \"activity_regularizer\": \"None\",\n"
            gmodel = gmodel + "         \"tb_button_3\": \"on\",\n"
            gmodel = gmodel + "         \"border_mode\": \"valid\",\n"
            gmodel = gmodel + "         \"operator_title\": \"Convolution2D\",\n"
            gmodel = gmodel + "         \"weight_constraint\": \"None\",\n"
            gmodel = gmodel + "         \"input_shape\": \"" + Activation + "\",\n"
            gmodel = gmodel + "         \"weight_initialization_function\": \"zero\",\n"
            gmodel = gmodel + "         \"dimension_ordering\": \"default\",\n"
            gmodel = gmodel + "         \"weight\": \"None\",\n"
            gmodel = gmodel + "         \"subsampling\": \"(" + str(Stride[0]) + "," + str(Stride[0]) + ")\",\n"
            gmodel = gmodel + "         \"filter_columns\": \"" + str(str(kernelSize[0])) + "\",\n"
            gmodel = gmodel + "         \"bias_regularizer\": \"None\",\n"
            gmodel = gmodel + "         \"bias\": \"true\",\n"
            gmodel = gmodel + "         \"filter_rows\": \"" + str(str(kernelSize[1])) + "\",\n"
            gmodel = gmodel + "         \"left\": \"" + str(posX + 20) + "\",\n"
            gmodel = gmodel + "         \"top\": \"" + str(posY + 100) + "\"\n"
            gmodel = gmodel + "         },\n"

        elif 'MaxPooling2D' in opT:
            poolSize = data["config"][i]["config"]["pool_size"]
            Padding = data["config"][i]["config"]["padding"]
            Strides = data["config"][i]["config"]["strides"]

            gmodel = gmodel + "     \"op_" + str(i + 1) + "\" : {\n"
            gmodel = gmodel + "         \"strides\": \"(" + str(Strides[0]) + "," + str(Strides[1]) + ")\",\n"
            gmodel = gmodel + "         \"dimension_ordering\": \"default\",\n"
            gmodel = gmodel + "         \"number_of_filters\": \"" + str(poolSize[0]) + "\",\n"
            gmodel = gmodel + "         \"border_mode\": \"valid\",\n"
            gmodel = gmodel + "         \"operator_title\": \"MaxPooling2D\",\n"
            gmodel = gmodel + "         \"tb_button_5\": \"on\",\n"
            gmodel = gmodel + "         \"left\": \"" + str(posX + 20) + "\",\n"
            gmodel = gmodel + "         \"top\": \"" + str(posY + 100) + "\"\n"
            gmodel = gmodel + "         },\n"

        elif 'ZeroPadding2D' in opT:
            # poolSize = data["config"][i]["config"]["pool_size"]
            # Padding = data["config"][i]["config"]["padding"]
            # Strides = data["config"][i]["config"]["strides"]

            gmodel = gmodel + "     \"op_" + str(i + 1) + "\" : {\n"
            gmodel = gmodel + "         \"strides\": \"(" + "," + ")\",\n"
            gmodel = gmodel + "         \"dimension_ordering\": \"default\",\n"
            gmodel = gmodel + "         \"number_of_filters\": \"" + "\",\n"
            gmodel = gmodel + "         \"border_mode\": \"valid\",\n"
            gmodel = gmodel + "         \"operator_title\": \"MaxPooling2D\",\n"
            gmodel = gmodel + "         \"tb_button_5\": \"on\",\n"
            gmodel = gmodel + "         \"left\": \"" + str(posX + 20) + "\",\n"
            gmodel = gmodel + "         \"top\": \"" + str(posY + 100) + "\"\n"
            gmodel = gmodel + "         },\n"

        elif 'Dropout' in opT:
            Rate = data["config"][i]["config"]["rate"]
            gmodel = gmodel + "     \"op_" + str(i + 1) + "\" : {\n"
            gmodel = gmodel + "         \"operator_title\": \"Dropout\",\n"
            gmodel = gmodel + "         \"seed\": \"None\",\n"
            gmodel = gmodel + "         \"number_of_filters\": \"" + str(Rate) + "\",\n"
            gmodel = gmodel + "         \"tb_button_6\": \"on\",\n"
            gmodel = gmodel + "         \"noise_shape\": \"None\",\n"
            gmodel = gmodel + "         \"left\": \"" + str(posX + 20) + "\",\n"
            gmodel = gmodel + "         \"top\": \"" + str(posY + 100) + "\"\n"
            gmodel = gmodel + "         },\n"

        elif 'Flatten' in opT:
            gmodel = gmodel + "     \"op_" + str(i + 1) + "\" : {\n"
            gmodel = gmodel + "         \"operator_title\": \"Flatten\",\n"
            gmodel = gmodel + "         \"left\": \"" + str(posX + 20) + "\",\n"
            gmodel = gmodel + "         \"top\": \"" + str(posY + 100) + "\"\n"
            gmodel = gmodel + "         },\n"

        elif 'Dense' in opT:
            Activation = data["config"][i]["config"]["activation"]
            Units = data["config"][i]["config"]["units"]
            gmodel = gmodel + "     \"op_" + str(i + 1) + "\" : {\n"
            gmodel = gmodel + "         \"operator_title\": \"Dense\",\n"
            gmodel = gmodel + "         \"input_dimention\": \"None\",\n"
            gmodel = gmodel + "         \"input_shape\": \"" + Activation + "\",\n"
            gmodel = gmodel + "         \"bias_constraint\": \"None\",\n"
            gmodel = gmodel + "         \"weight_initialization_function\": \"zero\",\n"
            gmodel = gmodel + "         \"activitiy_regularizer\": \"None\",\n"
            gmodel = gmodel + "         \"number_of_filters\": \"" + str(Units) + "\",\n"
            gmodel = gmodel + "         \"weight\": \"None\",\n"
            gmodel = gmodel + "         \"weights\": \"None\",\n"
            gmodel = gmodel + "         \"bias_regularizer\": \"None\",\n"
            gmodel = gmodel + "         \"bias\": \"None\",\n"
            gmodel = gmodel + "         \"regularizer_for_input_wegiht\": \"None\",\n"
            gmodel = gmodel + "         \"tb_button_2\": \"on\",\n"
            gmodel = gmodel + "         \"left\": \"" + str(posX + 20) + "\",\n"
            gmodel = gmodel + "         \"top\": \"" + str(posY + 100) + "\"\n"
            gmodel = gmodel + "         },\n"

    gmodel = gmodel + "     \"op_" + str(f + 1) + "\" : {\n"
    gmodel = gmodel + "         \"operator_title\": \"OutputLayer\",\n"
    gmodel = gmodel + "         \"output_port\": \"output_port\",\n"
    gmodel = gmodel + "         \"activation\": \"softmax\",\n"
    gmodel = gmodel + "         \"classes\": \"10\",\n"
    gmodel = gmodel + "         \"left\": \"" + str(posX + 20) + "\",\n"
    gmodel = gmodel + "         \"top\": \"" + str(posY + 100) + "\"\n"
    gmodel = gmodel + "         }\n"
    gmodel = gmodel + "}"
    print(gmodel)

    f = open("C:/Users/Rosenblatt/Desktop/graph.json", 'w')
    f.write(gmodel)
    f.close()