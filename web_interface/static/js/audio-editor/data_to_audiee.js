function data_to_audiee(json_object, audiee_instance) {
    for (let i = 0; i < json_object.Collections.Tracks.models.length; i++) {
        audiee_instance.Collections.Tracks.models.push({
            attributes: {
                buffer: {
                    duration: json_object.Collections.Tracks.models[i].attributes.buffer.duration,
                    length: json_object.Collections.Tracks.models[i].attributes.buffer.length,
                    numberOfChannels: json_object.Collections.Tracks.models[i].attributes.buffer.numberOfChannels,
                    sampleRate: json_object.Collections.Tracks.models[i].attributes.buffer.sampleRate //number depends, could be 41000 or 48000, or 96000
                },
                color: json_object.Collections.Tracks.models[i].attributes.color,
                file: {
                    lastModified: json_object.Collections.Tracks.models[i].attributes.file.lastModified,
                    name: json_object.Collections.Tracks.models[i].attributes.file.name,
                    size: json_object.Collections.Tracks.models[i].attributes.file.size,
                    type: json_object.Collections.Tracks.models[i].attributes.file.type,
                    webkitRelativePath: json_object.Collections.Tracks.models[i].attributes.file.webkitRelativePath // i saw path so i tought it was useful
                },
                gain: json_object.Collections.Tracks.models[i].attributes.gain,
                length: json_object.Collections.Tracks.models[i].attributes.length,
                muted: json_object.Collections.Tracks.models[i].attributes.muted,
                name: json_object.Collections.Tracks.models[i].attributes.name,
                pan: json_object.Collections.Tracks.models[i].attributes.pan,
                solo: json_object.Collections.Tracks.models[i].attributes.solo,
                cid: json_object.Collections.Tracks.models[i].attributes.cid //code
            }
        });
    }
}
export { data_to_audiee };
