import * as React from 'react';
import { TSCustomNodeModel } from './TSCustomNodeModel';
import { TSCustomNodeWidget } from './TSCustomNodeWidget';
import { AbstractReactFactory } from '@projectstorm/react-canvas-core';
export class TSCustomNodeFactory extends AbstractReactFactory {
    constructor() {
        super('ts-custom-node');
    }
    generateModel(initialConfig) {
        return new TSCustomNodeModel();
    }
    generateReactWidget(event) {
        return React.createElement(TSCustomNodeWidget, { engine: this.engine, node: event.model });
    }
}
