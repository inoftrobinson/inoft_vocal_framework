export function data_to_audiee(json_object, audiee_instance) {
    for (let i = 0; i < json_object.Collections.Tracks.models.length; i++) {
        audiee_instance.Collections.Tracks.models.push({
            attributes: {
                buffer: {
                    duration: json_object.Collections.Tracks.models[i].attributes.buffer.duration, //number
                    length: json_object.Collections.Tracks.models[i].attributes.buffer.length, //number
                    numberOfChannels: json_object.Collections.Tracks.models[i].attributes.buffer.numberOfChannels, //should be 2 if stereo or 1 if mono, or >2 if you're a genius
                    sampleRate: json_object.Collections.Tracks.models[i].attributes.buffer.sampleRate //number depends, could be 41000 or 48000, or 96000
                },
                color: json_object.Collections.Tracks.models[i].attributes.color, //hex : #FFFFFF
                file: {
                    lastModified: json_object.Collections.Tracks.models[i].attributes.file.lastModified, //freaking bid int
                    name: json_object.Collections.Tracks.models[i].attributes.file.name, //string file name
                    size: json_object.Collections.Tracks.models[i].attributes.file.size, //also a big int
                    type: json_object.Collections.Tracks.models[i].attributes.file.type, //string type of audio : "audio/<type>"
                    webkitRelativePath: json_object.Collections.Tracks.models[i].attributes.file.webkitRelativePath // i saw path so i tought it was useful
                },
                gain: json_object.Collections.Tracks.models[i].attributes.gain, //number (float)
                length: json_object.Collections.Tracks.models[i].attributes.length,
                muted: json_object.Collections.Tracks.models[i].attributes.muted, //bool
                name: json_object.Collections.Tracks.models[i].attributes.name, //string track name
                pan: json_object.Collections.Tracks.models[i].attributes.pan, //number (float)
                solo: json_object.Collections.Tracks.models[i].attributes.solo, //bool
                cid: json_object.Collections.Tracks.models[i].attributes.cid //code
            }
        });
    }
}