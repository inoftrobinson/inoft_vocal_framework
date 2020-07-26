"use strict";
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_diagrams_1 = __importStar(require("@projectstorm/react-diagrams"));
// create an instance of the engine with all the defaults
const engine = react_diagrams_1.default();
// node 1
const node1 = new react_diagrams_1.DefaultNodeModel({
    name: 'Node 1',
    color: 'rgb(0,192,255)',
});
node1.setPosition(100, 100);
let port1 = node1.addOutPort('Out');
// node 2
const node2 = new react_diagrams_1.DefaultNodeModel({
    name: 'Node 1',
    color: 'rgb(0,192,255)',
});
node2.setPosition(100, 100);
let port2 = node2.addOutPort('Out');
