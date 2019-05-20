// 190513  14:45 saved
function substitudeGraph(json_data, outerGraph, currentLevel) {
    /**
     * substitudeGraph(outerGraph, currentLevel)
     * At currentLevel, substitude the articulable subgraph as a module in outerGraph.
     *
     * @param outerGraph: a `dictionary`
     * The outer graph.
     *
     * @param currentLevel: a `int`
     * the current level.
     */
    let isOverallGraph = false;
    let jsonData = Object.assign({}, json_data);

    // #0. Check the current level whether the level is '-1' or not.
    // If the current level is '-1' or the outerGraph is 'undefined', then substitude the overall graph.
    if (outerGraph == undefined || currentLevel == -1) {
        // overall graph
        isOverallGraph =  true;
        currentLevel = -1;
    }

    let adjacentList = [];      // the new adjacent list

    // #1. Change the 'from' and 'to' to the module(articulable subgraph) index.
    if (1) {
        if (isOverallGraph == true) {
            // 1-1) Initialize the adjacentList.
            for (let sKey of Object.keys(jsonData.source_graph)) {
                let tIndex = sKey.substring(3, sKey.length);

                let temp = {};
                temp[tIndex] = Object.assign([], jsonData.source_graph[sKey].toLayer);
                adjacentList.push(temp);
            }
        } else {
            for (let sKey of jsonData.articulable_subgraph[outerGraph]) {
                let temp = {};
                let tArr = [];
                deepCopy(jsonData.source_graph["op_" + sKey].toLayer, tArr);
                temp[sKey] = tArr;
                adjacentList.push(temp);
            }
        }

        console.log("adjList : ", adjacentList);
        // substitude a module from overall graph.

        // 1-1) Initialize the adjacentList.
        //

        // 1-2) substitude the indexes.
        for (let aKey of Object.keys(jsonData.abstract_graph)) {
            if (jsonData.abstract_graph[aKey].index_outerGraph != currentLevel) {
                // This abstract graph is not current level, then continue this loop.
                continue;
            } else {
                // when this abstract graph is at current level...
                let articulableSubgraph = Object.assign([], jsonData.abstract_graph[aKey].subgraph);

                for (let node of articulableSubgraph) {
                    // 3-1) check 'from'
                    for (let record of adjacentList) {
                        let from = Object.keys(record);
                        let to = record[from];

                        if (from == node) {
                            // delete this record
                            let tempIndex = adjacentList.indexOf(record);
                            let tempList = {};
                            let id = "ag_" + aKey;
                            tempList[id] = to;
                            adjacentList[tempIndex] = tempList;
                            break;
                        }
                    }

                    // 3-1) check 'to'
                    for (let record of adjacentList) {
                        let from = Object.keys(record);
                        let to = record[from];

                        for (let i of to) {
                            if (node == i) {
                                let tempIndex1 = adjacentList.indexOf(record);
                                let tempIndex2 = to.indexOf(i);
                                let id = "ag_" + aKey;
                                to.splice(tempIndex2, 1, id);
                                adjacentList[tempIndex1][from] = to;
                            }
                        }
                    }
                }
            }
        }
    } else {
        // substitude a module from articulable subgraph shape.
    }


    // #2. If 'from' equals 'to', then filter that record from the outerGraph.
    for (let record of adjacentList) {
        let from = Object.keys(record);
        let to = record[from];

        // 2-1) filter out ovelapped element in 'to'.
        to = to.filter(function(value, index, self) {
            return self.indexOf(value) === index;
        });

        let rIndex = adjacentList.indexOf(record);
        adjacentList[rIndex][from] = to;
    }

    let tempList = [];
    for (let record of adjacentList) {
        let from = Object.keys(record);
        let to = record[from];

        // 2-2) filter out(remove) the element which satisfy that 'from' equals to 'to'.
        if (to.length == 1 && from[0] == to[0]) {
            {#console.log("record, to, from", to[0], from[0], rIndex);#}
            {#adjacentList.splice(rIndex, 1);      // remove#}
            } else {
                tempList.push(record);
            }
        }

        return tempList;
    }






// 190513  22:00 saved
function drawOverallGraph(JSON_dict, flowchart, adjacentList, left, top) {
        /**
         * drawOverallGraph(JSON_dict, flowchart, adjacentList, left, top)
         * Draw overall graph which indicates the highest abstract graph.
         *
         * @param JSON_dict: a `dictionary`
         * The dictionary which includes the information of the layers.
         *
         * * @param flowchart: a `HTML element`
         * The HTML element which indicates the drawing sheet.
         *
         * @param adjacentList: a `array`
         * A graph which has adjacent list structure.
         *
         * @param left: a `int`
         * The offset which indicates left(x) position.
         *
         * @param top: a `int`
         * The offset which indicates top(y) position.
         *
         */

        {#substitudeGraph();#}
        let $flowchart = flowchart;

        // set the default starting offsets.
        if (left == undefined) {
            left = 470;
        }

        if (top == undefined) {
            top = 5000;
        }

        const abstract_graph = JSON_dict["abstract_graph"];
        const source_graph = JSON_dict["source_graph"];
        const articulable_subgraph = JSON_dict["articulable_subgraph"];


        // 1. Draw the layers by rounding the adjacent list.
        // the overall abstract architecture of the network will be linear shape.
        let count = 0;
        for (let key of Object.keys(adjacentList)) {
            let fromLayer = key;
            let toLayer = adjacentList[fromLayer];

            let tempToken = fromLayer.split('_');

            let layerName;
            if (tempToken[0] == "ag") {
                // this layer is a module.
                layerName = "Module_" + abstract_graph[tempToken[1]].index_articulableSubgraph;
            } else {
                // this layer is a standard layer.
                layerName = source_graph["op_" + fromLayer].operator_title;
            }

            // 1-1) draw operator
            let element = '<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">' + layerName + '</div>';
            let data = getOperatorData($(element));
            data.top = top;                         // set its offsets
            data.left = left + (count++ * 240);
            let tempOperatorId = "layer_" + op_count++;
            let $temp = $flowchart.flowchart('addOperator', tempOperatorId, data);  // add operator
            let type = $flowchart.flowchart('getOperatorTitle', tempOperatorId);
            appendOperatorParam(tempOperatorId, type);
            if (tempToken[0] == 'ag') {
                // draw sub operator's argument taps.
                drawArgumentTap_hidden(abstract_graph[tempToken[1]].index_articulableSubgraph, tempOperatorId);
            }
        }
        // 2) Draw the links
        for (let i = 0; i < op_count - 1; i++) {

            // 1-2) draw link
            let linkData = {
                fromOperator: "layer_" + i,
                fromConnector: "output_" + 0,
                fromSubConnetor: 0,
                toOperator: "layer_" + (i + 1),
                toConnector: "input_" + 0,
                toSubConnector: 0
            };

            linkId = $flowchart.flowchart('myLinkDiagram', linkId, linkData);
        }

        deepCopy($flowchart.flowchart('getData').links, currLinks);
        console.log("currLinks : ", currLinks);

        // 3) extend the drawing sheet
        {#let transform = $('.drawing_sheet').css('transform');#}
        {#let transition = $('.drawing_sheet').css('transition');#}
        {#let width = Number($('.drawing_sheet').css('width').substring(0, $('.drawing_sheet').css('width').length - 2)) + ((count - 4) * 240);#}
        {#let style = 'width: ' + width + 'px; transform: ' + transform + '; transition: ' + transition + '; transform-origin: 50% 50%; cursor: move';#}
        {#$('.drawing_sheet').attr('style', style);#}
    }



// 190514  10:37 saved
function getNodeLevel_subgraph(JSON_dict, subgraph, isAdjList) {
        /**
         * getNodeLevel(JSON_dict)
         * Get the level of each nodes in the graph for drawing on the sheet.
         *
         * @param JSON_dict: a `dictionary`
         * The dictionary which includes the information of the layers.
         *
         * @param subgraph: a `array`
         * The subgraph set.
         *
         * @return nodeLevel: a`dictionary`
         * The node level.
         */

        var nodeLevel = new Array();      // the node level needed to locate each nodes.

        /////////////////////////////////////////////////////////////////////////////////////
        var adjList = subgraph;
        {#var adjList = JSON_dict;#}

        if (isAdjList == true) {
            let arr2dict = function(src, dst) {
                for (i of src) {
                    dst[Object.keys(i)] = Object.values(i)[0];
                }
            }

            var adjList_dict = {};
            arr2dict(adjList, adjList_dict);


            nodeLevel[0] = [Number(Object.keys(subgraph[0])[0])];       // push the first node.
            var currLevel = 0;
            while (nodeLevel[currLevel] != undefined) {
                {#console.log("(nodeLevel[currLevel] : ", (nodeLevel[currLevel]));#}
                {#console.log(nodeLevel[currLevel].length, nodeLevel[currLevel][0], subgraph[subgraph.length - 1]);#}

                for (var i of nodeLevel[currLevel]) {
                    // 1-0) if the node in current level is the last node, stop pushing.
                    if (i == Object.keys(subgraph[subgraph.length - 1])[0]) {
                        continue;
                    }

                    // 1-1) concatenate every next nodes.
                    if (nodeLevel[currLevel + 1] == undefined) {
                        nodeLevel[currLevel + 1] = adjList_dict[i];
                    } else {
                        nodeLevel[currLevel + 1] = nodeLevel[currLevel + 1].concat(adjList_dict[i]);
                    }


                    // 1-2) filter out overlapped nodes.
                    nodeLevel[currLevel + 1] = nodeLevel[currLevel + 1].filter(function(value, index, self) {
                        return self.indexOf(value) === index;
                    });
                }

                currLevel++;

            }

            // 2) remove the overlapped nodes from next nodes.
            for (let i = 0; i < nodeLevel.length - 1; i++) {
                for (let j = i + 1; j < nodeLevel.length; j++) {
                    let filterNode = nodeLevel[j];
                    nodeLevel[i] = nodeLevel[i].filter(item => !filterNode.includes(item));     // remove overlapped elements.
                }
            }
            return nodeLevel;
        } else {
            var adjList = JSON_dict["source_graph"];
            {#var adjList = JSON_dict;#}

            nodeLevel[0] = [subgraph[0]];       // push the first node.
            var currLevel = 0;
            while (nodeLevel[currLevel] != undefined) {
                {#console.log("(nodeLevel[currLevel] : ", (nodeLevel[currLevel]));#}
                {#console.log(nodeLevel[currLevel].length, nodeLevel[currLevel][0], subgraph[subgraph.length - 1]);#}

                for (var i of nodeLevel[currLevel]) {
                    var dictKey = "op_" + i;        // the access key
                    // 1-0) if the node in current level is the last node, stop pushing.
                    if (i == subgraph[subgraph.length - 1]) {
                        break;
                    }

                    // 1-1) concatenate every next nodes.
                    if (nodeLevel[currLevel + 1] == undefined) {
                        nodeLevel[currLevel + 1] = adjList[dictKey].toLayer;
                    } else {
                        nodeLevel[currLevel + 1] = nodeLevel[currLevel + 1].concat(adjList[dictKey].toLayer);
                    }

                    // 1-2) filter out overlapped nodes.
                    nodeLevel[currLevel + 1] = nodeLevel[currLevel + 1].filter(function(value, index, self) {
                        return self.indexOf(value) === index;
                    });
                }

                currLevel++;

            }

            // 2) remove the overlapped nodes from next nodes.
            for (let i = 0; i < nodeLevel.length - 1; i++) {
                for (let j = i + 1; j < nodeLevel.length; j++) {
                    let filterNode = nodeLevel[j];
                    nodeLevel[i] = nodeLevel[i].filter(item => !filterNode.includes(item));     // remove overlapped elements.
                }
            }

            {#console.log("nodeLevel : ", nodeLevel);#}

            return nodeLevel;
        }
    }



// 190514  11:18 saved
function drawArticulableSubgraph(JSON_dict, articulableSubgraph_index, operatorId, flowchart, left, top) {
        /**
         * drawDiagrams(JSON_dict)
         * Draw the diagrams on the editor by the layer information which consist of json dictionary.
         *
         * @param JSON_dict: a `dictionary`
         * The dictionary which includes the information of the layers.
         *
         * @param articulableSubgraph: a `int`
         * The articulable subgraph index.
         */

        let count_1 = 0;
        {#var flowchartId = '#sheet_' + flowchart_index;#}
        var $flowchart = flowchart;

        if (left == undefined) {
            left = 470;
        }

        if (top == undefined) {
            top = 5000;
        }

        {#adjacentList = substitudeGraph(JSON_dict, 0, 0);#}


        {#var abstractData = JSON_dict["abstract_graph"][abstract_index];#}
        var articulableSubgraph = JSON_dict["articulable_subgraph"][articulableSubgraph_index];
        let adjList = substitudeGraph(json_data, 0, 0);
        {#var nodeLevel = getNodeLevel_subgraph(JSON_dict, adjList, true);#}
        var nodeLevel = getNodeLevel_adjList(JSON_dict, adjList);


        console.log("adjList : ", adjList);
        return;

        {#getNodeLevel_subgraph(JSON_dict, articulableSubgraph);#}

        // 1. Draw source graph
        // JSON dictionary 데이터가 끝날때까지 차례로 순회한다.
        {#var dict_index = articulableSubgraph[0];     // JSON dictionary 데이터에 접근할 인덱스 ("op_0", "op_1", ...)#}
            var accessKey = "source_graph";

            let leftLevel = function(arr, item) {
                let tempItem;
                if (typeof(item) == "string") {
                    let tempToken = item.split('_');
                    if (tempToken[0] != 'ag') {
                        tempItem = Number(item);
                    } else {
                        tempItem = item;
                    }
                    {#console.log("type : ", item, typeof(tempToken[0]), typeof(arr[0][0]));#}
                }

                var level = -1;

                for (var i in arr) {
                    {#console.log("aaaa : ", arr[i], arr[i].indexOf(Number(item)));#}
                    if (arr[i].indexOf(tempItem) != -1) {
                        level = i;
                        break;
                    }
                }
                return level;
            };
            let topLevel = function(arr, item) {
                let tempItem;
                if (typeof(item) == "string") {
                    let tempToken = item.split('_');
                    if (tempToken[0] != 'ag') {
                        tempItem = Number(item);
                    } else {
                        tempItem = item;
                    }
                    {#console.log("type : ", item, typeof(tempToken[0]), typeof(arr[0][0]));#}
                }

                var index = -1;

                for (i of arr) {
                    count_1++; //////////////////////////////////////////////////////
                    index = i.indexOf(tempItem);

                    if (index != -1) break;
                }

                return index;
            };
            let maxLength = function(arr) {
                var length = new Array();
                for (i of arr) {
                    count_1++; //////////////////////////////////////////////////////
                    length.push(i.length);
                }
                {#console.log("length : ", length);#}
                return Math.max.apply(null, length);
            }


            const abstract_graph = JSON_dict["abstract_graph"];
            const source_graph = JSON_dict["source_graph"];


            if (adjList != []) {
                // The graph has inner modules.
                var op = {'first':null, 'last':null};
                var op_index = 0;

                let queue = new Queue();        // the loop will do in a sequence of queue.

                queue.enqueue(adjList[0]);      // enqueue the first element of the 'adjList'.
                let loopCount = 0;
                while(!queue.empty()) {
                    let tempCurrentLayer = queue.dequeue();
                    let currentOpIndex = op_index;

                    console.log("loop count#", loopCount, "  tempCurrentLayer : ", tempCurrentLayer);

                    if (op_index == 0) {
                        // add the first node in articulable subgraph (starting node)
                        let layer = Object.keys(tempCurrentLayer)[0];
                        let tempToken = layer.split('_');

                        let layerName;
                        layerName = source_graph["op_" + layer].operator_title;

                        // 1-1) draw operator
                        let element = '<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">' + layerName + '</div>';
                        let data = getOperatorData($(element));

                        let topStart = top - maxLength(nodeLevel) / 2 * 140;
                        let leftStart;

                        // the top of the first node and last node should be same. And they should be located center of overall graph.
                        if (layer == articulableSubgraph[0] || layer == articulableSubgraph[articulableSubgraph.length - 1]) {
                            data.top = top;
                            console.log(maxLength(nodeLevel));
                        } else {
                            data.top = topStart + topLevel(nodeLevel, layer) * 140;
                        }
                        data.left = left + leftLevel(nodeLevel, layer) * 250;        // 레이어 노드의 좌표(left, top)

                        let tempOperatorId = operatorId + "_" + articulableSubgraph_index + "_" + op_index;
                        op.first = tempOperatorId;
                        let $temp = $flowchart.flowchart('addOperator', tempOperatorId, data, true);  // 레이어 노드를 추가한다.
                        let type = $flowchart.flowchart('getOperatorTitle', tempOperatorId);

                        op_index++;
                    }

                    if (op_index == adjList.length) {
                        // break point --> the last node (ending node)
                        let tempOperatorId = operatorId + "_" + articulableSubgraph_index + "_" + (op_index - 1);
                        op.last = tempOperatorId;
                        break;
                    }

                    ////// need to start from this
                    // draw adjacent nodes at current node.
                    for (let layer of Object.values(tempCurrentLayer)[0]) {
                        if (!queue.hasValue(layer)) {
                            // add adjacent node to the queue.
                            queue.enqueue(layer);
                        }

                        let adjacentOpIndex = op_index;
                        let fromLayer = Object.keys(layer)[0];
                        let operator = JSON_dict[accessKey]["op_" + Object.keys(layer)[0]];         // operator 객체 지정
                        console.log("leftLevel(nodeLevel, dict_index) : ", leftLevel(nodeLevel, fromLayer), fromLayer, nodeLevel);

                        let tempToken = fromLayer.split('_');

                        let layerName;
                        if (tempToken[0] == "ag") {
                            // this layer is a module.
                            layerName = "Module_" + abstract_graph[tempToken[1]].index_articulableSubgraph;
                        } else {
                            // this layer is a standard layer.
                            layerName = source_graph["op_" + fromLayer].operator_title;
                        }

                        // 1-1) draw operator
                        let element = '<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">' + layerName + '</div>';
                        let data = getOperatorData($(element));

                        let topStart = top - maxLength(nodeLevel) / 2 * 140;
                        let leftStart;

                        // the top of the first node and last node should be same. And they should be located center of overall graph.
                        if (fromLayer == articulableSubgraph[0] || fromLayer == articulableSubgraph[articulableSubgraph.length - 1]) {
                            data.top = top;
                            console.log(maxLength(nodeLevel));
                        } else {
                            data.top = topStart + topLevel(nodeLevel, fromLayer) * 140;
                        }
                        data.left = left + leftLevel(nodeLevel, fromLayer) * 250;        // 레이어 노드의 좌표(left, top)

                        let tempOperatorId = operatorId + "_" + articulableSubgraph_index + "_" + op_index;
                        if (fromLayer == articulableSubgraph[0] || fromLayer == articulableSubgraph[articulableSubgraph.length - 1]) {
                            if (fromLayer == articulableSubgraph[0]) {
                                // it may be ok if it is deleted
                                op.first = tempOperatorId;
                            } else {
                                // it may be ok if it is deleted
                                op.last = tempOperatorId;
                            }
                            let $temp = $flowchart.flowchart('addOperator', tempOperatorId, data, true);  // 레이어 노드를 추가한다.
                        } else {
                            let $temp = $flowchart.flowchart('addOperator', tempOperatorId, data);  // 레이어 노드를 추가한다.
                        }
                        let type = $flowchart.flowchart('getOperatorTitle', tempOperatorId);

                        op_index++;

                        // 1-2) Draw links
                        let from = currentOpIndex;
                        let to = adjacentOpIndex;
                        let from_tempOperatorId = operatorId + "_" + articulableSubgraph_index + "_" + from;
                        let to_tempOperatorId = operatorId + "_" + articulableSubgraph_index + "_" + to;
                        console.log("from_tempOperatorId, to_tempOperatorId", from_tempOperatorId, to_tempOperatorId);
                        let linkData = {
                            fromOperator: from_tempOperatorId,
                            fromConnector: "output_" + 0,
                            fromSubConnetor: 0,
                            toOperator: to_tempOperatorId,
                            toConnector: "input_" + 0,
                            toSubConnector: 0
                        };

                        linkId = $flowchart.flowchart('myLinkDiagram', linkId, linkData);
                    }

                    return;
                }

                return;
                /////////////////////////////////////////////////////////////////////////////
                // Link 그리는 부분
                var index = 0;
                op_index = 0;
                for (let record of adjList) {
                    let fromLayer = Object.keys(record)[0];
                    let toLayer = Object.values(record)[0];
                    for (let to of toLayer) {
                        var from_tempOperatorId = operatorId + "_" + articulableSubgraph_index + "_" + fromLayer;
                        var to_tempOperatorId = operatorId + "_" + articulableSubgraph_index + "_" + to;
                        console.log("from_tempOperatorId, to_tempOperatorId", from_tempOperatorId, to_tempOperatorId);
                        var linkData = {
                            fromOperator: from_tempOperatorId,
                            fromConnector: "output_" + 0,
                            fromSubConnetor: 0,
                            toOperator: to_tempOperatorId,
                            toConnector: "input_" + 0,
                            toSubConnector: 0
                        };

                        linkId = $flowchart.flowchart('myLinkDiagram', linkId, linkData);
                    }
                }
            } else {
                // There are no inner modules.
            }

            return;

            for (var dict_index of articulableSubgraph) {
                var operator = JSON_dict[accessKey]["op_" + dict_index];         // operator 객체 지정
                {#console.log("dict_index : ", dict_index);#}
                var data;        // 왼쪽 탭에 있는 data(레이어 종류)

                // var default_left = 400;
                // var default_top = 600;

                switch (operator.operator_title) {
                    case "InputLayer":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">InputLayer</div>'));
                        break;

                    case "OutputLayer":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">OutputLayer</div>'));
                        break;

                    case "Dense":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">Dense</div>'));
                        break;

                    case "Dropout":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">Dropout</div>'));
                        break;

                    case "Flatten":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">Flatten</div>'));
                        break;

                    case "Convolution2D":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">Convolution2D</div>'));
                        break;

                    case "ZeroPadding2D":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">ZeroPadding2D</div>'));
                        break;

                    case "MaxPool2D":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">MaxPool2D</div>'));
                        break;

                    case "AveragePooling2D":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">AveragePooling2D</div>'));
                        break;

                    case "LSTM":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">LSTM</div>'));
                        break;

                    case "SimpleRNN":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">SimpleRNN</div>'));
                        break;
                    case "LeakyReLU":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">LeakyReLU</div>'));
                        break;
                    case "GlobalAveragePooling2D":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">GlobalAveragePooling2D</div>'));
                        break;
                    case "Concatenate":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">Concatenate</div>'));
                        break;
                    case "Lambda":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">Lambda</div>'));
                        break;
                    case "Add":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">Add</div>'));
                        break;
                    case "BatchNormalization":
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">BatchNormalization</div>'));
                        break;
                    default:
                        data = getOperatorData($('<div class="draggable_operator ui-draggable ui-draggable-handle" data-nb-inputs="1" data-nb-outputs="1">noname</div>'));
                }

                {#// if the offset is undefined, locate the layers automatically.#}
                    {#if (data.left == undefined || data.top == undefined) {#}
                        {#    #}

                        var topStart = top - maxLength(nodeLevel) / 2 * 140;
                        var leftStart;

                        // the top of the first node and last node should be same. And they should be located center of overall graph.
                        if (dict_index == articulableSubgraph[0] || dict_index == articulableSubgraph[articulableSubgraph.length - 1]) {
                            data.top = top;
                            {#console.log(maxLength(nodeLevel));#}
                        } else {
                            data.top = topStart + topLevel(nodeLevel, dict_index) * 140;
                        }
                        data.left = left + leftLevel(nodeLevel, dict_index) * 250;        // 레이어 노드의 좌표(left, top)

                        //  레이어 파라미터 정보 설정하는 부분 추가해야됨
                        var tempOperatorId = operatorId + "_" + articulableSubgraph_index + "_" + op_index++;
                        if (dict_index == articulableSubgraph[0] || dict_index == articulableSubgraph[articulableSubgraph.length - 1]) {
                            var $temp = $flowchart.flowchart('addOperator', tempOperatorId, data, true);  // 레이어 노드를 추가한다.
                        } else {
                            var $temp = $flowchart.flowchart('addOperator', tempOperatorId, data);  // 레이어 노드를 추가한다.
                        }
                        var type = $flowchart.flowchart('getOperatorTitle', tempOperatorId);
                        {#appendOperatorParam(tempOperatorId, type);#}
                    }   // for end

                    // Link 그리는 부분
                    {#var index = 0;#}
                    var op = {'first':null, 'last':null};
                    for (var i = 0; i < articulableSubgraph.length - 1; i++) {
                        var layer = JSON_dict[accessKey]["op_" + articulableSubgraph[i]];

                        for (var j = 0; j < Object.keys(layer["toLayer"]).length; j++) {
                            var from_tempOperatorId = operatorId + "_" + articulableSubgraph_index + "_" + i;
                            var to_tempOperatorId = operatorId + "_" + articulableSubgraph_index + "_" + articulableSubgraph.indexOf(layer["toLayer"][j])
                            if (i == 0) {
                                op['first'] = from_tempOperatorId;
                            }
                            var linkData = {
                                fromOperator: from_tempOperatorId,
                                fromConnector: "output_" + 0,
                                fromSubConnetor: 0,
                                toOperator: to_tempOperatorId,
                                toConnector: "input_" + 0,
                                toSubConnector: 0
                            };

                            linkId = $flowchart.flowchart('myLinkDiagram', linkId, linkData);

                            count_1++; //////////////////////////////////////////////////////
                        }
                    }
                    op['last'] = operatorId + "_" + articulableSubgraph_index + "_" + (articulableSubgraph.length - 1);

                    console.log("count_1 :", count_1);
                    console.log("asdassdfa : ", getLayerSequenceFromEditor());


                    return op;
                }



                $(document).on("click", '.plus_button', function () {
                    // if the 'plus button' is clicked, re-draw the graphs.
                    let count = 0;

                    // redraw();
                    var operatorId = this.getAttribute('operatorId');
                    var $operator = $('#' + operatorId);
                    {#var operator = document.getElementById(this.getAttribute('operatorId'));#}
                    {#console.log("operator : ", operator.top);#}

                    // To get the operator's position...
                    var temp = $operator.attr('style').split('; ');
                    var position = {};
                    for (record of temp) {
                        var key = record.split(': ')[0];
                        var val;
                        if (key == 'top') {
                            val = $flowchart.flowchart('getOperatorData', this.getAttribute('operatorId')).top;
                            {#val = Number(record.split(': ')[1].substring(0, record.split(': ')[1].length - 2));#}
                        } else {
                            {#val = Number(record.split(': ')[1].substring(0, record.split(': ')[1].length - 3));#}
                            val = $flowchart.flowchart('getOperatorData', this.getAttribute('operatorId')).left;
                        }

                        position[key] = val;

                        count++;    ////////////////////////////////////////////////////////////////////////////////////////////////////////////
                    }

                    var before = [];
                    var after = [];
                    for (var i of Object.keys($flowchart.flowchart('getData').links)) {
                        if ($flowchart.flowchart('getData').links[i].toOperator == operatorId) {
                            var temp = {};
                            temp["index"] = i;
                            temp["data"] = $flowchart.flowchart('getData').links[i];
                            before.push(temp);
                        }
                        if ($flowchart.flowchart('getData').links[i].fromOperator == operatorId) {
                            var temp = {};
                            temp["index"] = i;
                            temp["data"] = $flowchart.flowchart('getData').links[i];
                            after.push(temp);
                        }

                        count++;    ////////////////////////////////////////////////////////////////////////////////////////////////////////////
                    }

                    var addNewLink = function(from, to, linkId) {
                        var linkData = {
                            fromOperator: from,
                            fromConnector: "output_" + 0,
                            fromSubConnetor: 0,
                            toOperator: to,
                            toConnector: "input_" + 0,
                            toSubConnector: 0
                        };
                        linkId = $flowchart.flowchart('myLinkDiagram', linkId, linkData);
                    };

                    // draw that module.
                    {#console.log("$flowchart.flowchart('getOperatorTitle', operatorId).split('_') : ", $flowchart.flowchart('getOperatorTitle', operatorId).split('_'));#}
                    var articulableSubgraph_index = $flowchart.flowchart('getOperatorTitle', operatorId).split('_')[1];

                    var op = drawArticulableSubgraph(json_data, articulableSubgraph_index, operatorId, $flowchart, position.left, position.top);

                    // delete that module.
                    $flowchart.flowchart('deleteOperator', operatorId);

                    // add before links
                    for (var i of before) {
                        addNewLink(i.data.fromOperator, op.first, i.index);

                        count++;    ////////////////////////////////////////////////////////////////////////////////////////////////////////////
                    }

                    // add after links
                    for (var i of after) {
                        addNewLink(op.last, i.data.toOperator, i.index);

                        count++;    ////////////////////////////////////////////////////////////////////////////////////////////////////////////
                    }


                    // re-locate the nodes.
                    var queue = new Queue();
                    queue.enqueue(op.last);
                    var dist = $flowchart.flowchart('getOperatorData', op.last).left - $flowchart.flowchart('getOperatorData', op.first).left;
                    while (!queue.empty()) {
                        var curr = queue.dequeue();

                        for (var i of Object.keys($flowchart.flowchart('getData').links)) {
                            count++;
                            var data = $flowchart.flowchart('getData').links[i];
                            if (data.fromOperator == curr) {
                                // that node 'i' would be located after 'curr' node.
                                var operatorData = $flowchart.flowchart('getOperatorData', data.toOperator);
                                {#console.log("operatorData : ", $flowchart.flowchart('getOperatorData', data.toOperator));#}
                                {#let operatorData = {};#}
                                let tempId = data.toOperator;
                                operatorData['left'] = document.getElementById(tempId).offsetLeft;
                                operatorData['top'] = document.getElementById(tempId).offsetTop;
                                {#console.log("operatorData.top : ", operatorData.top);#}

                                if (!queue.hasValue(data.toOperator)) {
                                    operatorData.left += dist;
                                    if (data.toOperator.substr(0, 5) == 'layer') {
                                        var token = data.toOperator.split('_');
                                        if (token.length >= 3) {


                                            if (json_data["articulable_subgraph"][articulableSubgraph_index].length - 1 == token[3] || token[3] == 0) {
                                                $flowchart.flowchart('setOperatorData', data.toOperator, operatorData, true);
                                                queue.enqueue(data.toOperator);
                                                console.log("json_data[\"articulable_subgraph\"][token[2]] : ", json_data["articulable_subgraph"][token[2]]);
                                                continue;
                                            }
                                        }
                                        $flowchart.flowchart('setOperatorData', data.toOperator, operatorData);
                                        queue.enqueue(data.toOperator);
                                    }
                                } else {
                                    continue;
                                }
                            }
                        }
                    }

                    // expand the drawing sheet.
                    {#var transform = $('.drawing_sheet').css('transform');#}
                    {#var transition = $('.drawing_sheet').css('transition');#}
                    {#var width = Number($('.drawing_sheet').css('width').substring(0, $('.drawing_sheet').css('width').length - 2)) + dist;#}
                    {#var style = 'width: ' + width + 'px; transform: ' + transform + '; transition: ' + transition + '; transform-origin: 50% 50%; cursor: move; ';#}
                    {#$('.drawing_sheet').attr('style', style);#}
                    let tempOperatorData = $flowchart.flowchart('getOperatorData', "layer_2");
                    $flowchart.flowchart('myMoveOperator', "layer_2", {"top":4840, "left":1111});
                });
