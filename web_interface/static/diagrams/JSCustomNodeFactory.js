"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
var React = __importStar(require("react"));
var JSCustomNodeModel_1 = require("./JSCustomNodeModel");
var JSCustomNodeWidget_1 = require("./JSCustomNodeWidget");
var react_canvas_core_1 = require("@projectstorm/react-canvas-core");
var JSCustomNodeFactory = /** @class */ (function (_super) {
    __extends(JSCustomNodeFactory, _super);
    function JSCustomNodeFactory() {
        return _super.call(this, 'js-custom-node') || this;
    }
    JSCustomNodeFactory.prototype.generateModel = function (event) {
        return new JSCustomNodeModel_1.JSCustomNodeModel();
    };
    JSCustomNodeFactory.prototype.generateReactWidget = function (event) {
        return React.createElement(JSCustomNodeWidget_1.JSCustomNodeWidget, { engine: this.engine, node: event.model });
    };
    return JSCustomNodeFactory;
}(react_canvas_core_1.AbstractReactFactory));
exports.JSCustomNodeFactory = JSCustomNodeFactory;
