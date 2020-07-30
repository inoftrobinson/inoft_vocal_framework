import * as React from 'react';
import { TSCustomNodeModel } from './TSCustomNodeModel';
import { TSCustomNodeWidget } from './TSCustomNodeWidget';
import { AbstractReactFactory, GenerateModelEvent, GenerateWidgetEvent} from '@projectstorm/react-canvas-core';
import { DiagramEngine } from '@projectstorm/react-diagrams-core';

export class TSCustomNodeFactory extends AbstractReactFactory<TSCustomNodeModel, DiagramEngine> {
	constructor() {
		super('ts-custom-node');
	}

	generateModel(initialConfig: GenerateModelEvent) {
		return new TSCustomNodeModel();
	}

	generateReactWidget(event: GenerateWidgetEvent<any>): JSX.Element {
		return <TSCustomNodeWidget engine={this.engine as DiagramEngine} node={event.model} />;
	}
}