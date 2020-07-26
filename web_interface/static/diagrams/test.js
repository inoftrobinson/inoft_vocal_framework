"use strict";
/*
import createEngine, {
    DefaultLinkModel,
    DefaultNodeModel,
    DiagramModel
} from '@projectstorm/react-diagrams';

import {
    CanvasWidget
} from '@projectstorm/react-canvas-core';


// create an instance of the engine with all the defaults
const engine = createEngine();


// node 1
const node1 = new DefaultNodeModel({
    name: 'Node 1',
    color: 'rgb(0,192,255)',
});
node1.setPosition(100, 100);
let port1 = node1.addOutPort('Out');

// node 2
const node2 = new DefaultNodeModel({
    name: 'Node 1',
    color: 'rgb(0,192,255)',
});
node2.setPosition(100, 100);
let port2 = node2.addOutPort('Out');


// link them and add a label to the link
const link = port1.link<DefaultLinkModel>(port2);
link.addLabel('Hello World!');


const model = new DiagramModel();
model.addAll(node1, node2, link);
engine.setModel(model);
*/
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const ReactDOM = __importStar(require("react-dom"));
require("./main.css");
const react_diagrams_1 = __importStar(require("@projectstorm/react-diagrams"));
const TSCustomNodeFactory_1 = require("./TSCustomNodeFactory");
const TSCustomNodeModel_1 = require("./TSCustomNodeModel");
// create an instance of the engine
const engine = react_diagrams_1.default();
// register the two engines
// engine.getNodeFactories().registerFactory(new JSCustomNodeFactory() as any);
engine.getNodeFactories().registerFactory(new TSCustomNodeFactory_1.TSCustomNodeFactory());
// create a diagram model
const model = new react_diagrams_1.DiagramModel();
//####################################################
// now create two nodes of each type, and connect them
// const node1 = new JSCustomNodeModel({ color: 'rgb(192,255,0)' });
// node1.setPosition(50, 50);
const node2 = new TSCustomNodeModel_1.TSCustomNodeModel({ color: 'rgb(0,192,255)' });
node2.setPosition(200, 50);
const link1 = new react_diagrams_1.DefaultLinkModel();
// link1.setSourcePort(node1.getPort('out'));
// link1.setTargetPort(node2.getPort('in'));
// model.addAll(node1, node2, link1);
model.addAll(node2);
//####################################################
// install the model into the engine
engine.setModel(model);
document.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(engine, { engine } /  > , document.querySelector('#application'));
});
