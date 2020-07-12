"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_diagrams_1 = require("@projectstorm/react-diagrams");
// create an instance of the engine with all the defaults
var engine = react_diagrams_1.default();
// node 1
var node1 = new react_diagrams_1.DefaultNodeModel({
    name: 'Node 1',
    color: 'rgb(0,192,255)',
});
node1.setPosition(100, 100);
var port1 = node1.addOutPort('Out');
// node 2
var node2 = new react_diagrams_1.DefaultNodeModel({
    name: 'Node 1',
    color: 'rgb(0,192,255)',
});
node2.setPosition(100, 100);
var port2 = node2.addOutPort('Out');
