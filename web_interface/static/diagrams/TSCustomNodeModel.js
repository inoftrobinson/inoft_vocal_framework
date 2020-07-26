"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const react_diagrams_1 = require("@projectstorm/react-diagrams");
class TSCustomNodeModel extends react_diagrams_1.NodeModel {
    constructor(options = {}) {
        super(Object.assign(Object.assign({}, options), { type: 'ts-custom-node' }));
        this.color = options.color || 'red';
        // setup an in and out port
        this.addPort(new react_diagrams_1.DefaultPortModel({
            in: true,
            name: 'in'
        }));
        this.addPort(new react_diagrams_1.DefaultPortModel({
            in: false,
            name: 'out'
        }));
    }
    serialize() {
        return Object.assign(Object.assign({}, super.serialize()), { color: this.color });
    }
    deserialize(event) {
        super.deserialize(event);
        // this.color = event.data.color;
        // todo: readd color property setter
    }
}
exports.TSCustomNodeModel = TSCustomNodeModel;
