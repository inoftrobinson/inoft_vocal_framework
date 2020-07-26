function load_data_2() {
    let data: { [index: string]: any; } = {
        collections: {
            tracks:
                {
                    models:
                        [{
                            attributes:
                                {
                                    buffer:
                                        {
                                            duration: 217.1178231292517,
                                            length: 9574896,
                                            numberOfChannels: 2,
                                            sampleRate: 44100
                                        },
                                    color: '#00a0b0',
                                    file:
                                        {
                                            lastModified: 1587987671814,
                                            name: 'In Her Sleep.mp3',
                                            size: 3474075,
                                            type: 'audio/mpeg',
                                            webkitRelativePath: ''
                                        },
                                    gain: 1,
                                    length: 1920,
                                    muted: false,
                                    name: 'Track 1',
                                    pan: 0.5,
                                    solo: false
                                }
                        }]
                }
        }
    }

    for (let key in data) {
        let value = data[key];
        console.log(value);
        // Use `key` and `value`
    }
}
