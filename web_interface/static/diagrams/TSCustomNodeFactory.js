"use strict";
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const React = __importStar(require("react"));
const TSCustomNodeModel_1 = require("./TSCustomNodeModel");
const TSCustomNodeWidget_1 = require("./TSCustomNodeWidget");
const react_canvas_core_1 = require("@projectstorm/react-canvas-core");
class TSCustomNodeFactory extends react_canvas_core_1.AbstractReactFactory {
    constructor() {
        super('ts-custom-node');
    }
    generateModel(initialConfig) {
        return new TSCustomNodeModel_1.TSCustomNodeModel();
    }
    generateReactWidget(event) {
        return React.createElement(TSCustomNodeWidget_1.TSCustomNodeWidget, { engine: this.engine, node: event.model });
    }
}
exports.TSCustomNodeFactory = TSCustomNodeFactory;
