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
class TSCustomNodeWidget extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }
    render() {
        return (`
			<div className="custom-node">
				<PortWidget engine={this.props.engine} port={this.props.node.getPort('in')}>
					<div className="circle-port" />
				</PortWidget>
				<PortWidget engine={this.props.engine} port={this.props.node.getPort('out')}>
					<div className="circle-port" />
				</PortWidget>
				<div className="custom-node-color" style={{ backgroundColor: this.props.node.color }} />
			</div>
		`);
    }
}
exports.TSCustomNodeWidget = TSCustomNodeWidget;
