import { NodeModel, DefaultPortModel } from '@projectstorm/react-diagrams';
export class TSCustomNodeModel extends NodeModel {
    constructor(options = {}) {
        super(Object.assign(Object.assign({}, options), { type: 'ts-custom-node' }));
        this.color = options.color || 'red';
        // setup an in and out port
        this.addPort(new DefaultPortModel({
            in: true,
            name: 'in'
        }));
        this.addPort(new DefaultPortModel({
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
