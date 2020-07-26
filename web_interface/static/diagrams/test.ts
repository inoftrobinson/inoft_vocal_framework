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

import * as React from 'react';
import * as ReactDOM from 'react-dom';
import './main.css';
import createEngine, { DiagramEngine, DefaultLinkModel, DiagramModel } from '@projectstorm/react-diagrams';
import { TSCustomNodeFactory } from "./TSCustomNodeFactory";
import { TSCustomNodeModel } from "./TSCustomNodeModel";
import { BodyWidget } from './BodyWidget';

// create an instance of the engine
const engine: DiagramEngine = createEngine();

// register the two engines
// engine.getNodeFactories().registerFactory(new JSCustomNodeFactory() as any);
engine.getNodeFactories().registerFactory(new TSCustomNodeFactory());

// create a diagram model
const model = new DiagramModel();

//####################################################
// now create two nodes of each type, and connect them

// const node1 = new JSCustomNodeModel({ color: 'rgb(192,255,0)' });
// node1.setPosition(50, 50);

const node2 = new TSCustomNodeModel({ color: 'rgb(0,192,255)' });
node2.setPosition(200, 50);

const link1 = new DefaultLinkModel();
// link1.setSourcePort(node1.getPort('out'));
// link1.setTargetPort(node2.getPort('in'));

// model.addAll(node1, node2, link1);
model.addAll(node2);

//####################################################

// install the model into the engine
engine.setModel(model);

document.addEventListener('DOMContentLoaded', () => {
	ReactDOM.render(<BodyWidget engine={engine} />, document.querySelector('#application'));
});
