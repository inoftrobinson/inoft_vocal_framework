var audioContext, source, sourceAudio, graphicEqualizer, splitter, analyzer, analyzerType, merger, pendingUrls, chkSource, ignoreNextConvolverChange = false;
//fakeAudioContext was created only to act as a "null audio context", making at least the graph work in other browsers
function fakeAudioContext() {
}
fakeAudioContext.prototype = {
    sampleRate: 44100,
    createChannelSplitter: function () {
        return {};
    },
    createChannelMerger: function () {
        return {};
    },
    createBufferSource: function () {
        return {};
    },
    createBuffer: function (channels, filterLength, sampleRate) {
        if (sampleRate === undefined)
            return this.createBuffer(2, 1024, this.sampleRate);
        return {
            duration: filterLength / sampleRate,
            gain: 1,
            length: filterLength,
            numberOfChannels: channels,
            sampleRate: sampleRate,
            data: (function () {
                var a = new Array(channels), i;
                for (i = channels - 1; i >= 0; i--)
                    a[i] = new Float32Array(filterLength);
                return a;
            })(),
            getChannelData: function (index) { return this.data[index]; }
        };
    },
    createConvolver: function () {
        var mthis = this;
        return {
            buffer: null,
            context: mthis,
            normalize: true,
            numberOfInputs: 1,
            numberOfOutputs: 1
        };
    }
};
function main() {
    console.log("Init equa");
    pendingUrls = [];
    attachMouse($("btnPlay"), "click", play);
    attachMouse($("btnStop"), "click", stop);
    attachMouse($("btnProcess"), "click", processAndDownload);
    chkSource = [$("chkSource0"), $("chkSource1"), $("chkSource2")];
    chkSource[0].addEventListener("change", chkSource_Change);
    chkSource[1].addEventListener("change", chkSource_Change);
    chkSource[2].addEventListener("change", chkSource_Change);
    $("txtFile").addEventListener("change", txtFile_Change);
    $("txtURL").addEventListener("change", txtURL_Change);
    $("cbFilterLength").addEventListener("change", filterLengthChanged);
    $("cbAnalyzer").addEventListener("change", updateConnections);
    audioContext = (window.AudioContext ? new AudioContext() : (window.webkitAudioContext ? new webkitAudioContext() : new fakeAudioContext()));
    graphicEqualizer = new GraphicalFilterEditorControl(2048, audioContext, updateConnections);
    graphicEqualizer.createControl($("equalizerPlaceholder"));
    analyzerType = null;
    analyzer = null;
    splitter = audioContext.createChannelSplitter();
    merger = audioContext.createChannelMerger();
    return true;
}
function chkSource_Change() {
    var e = (chkSource[1].checked ? "disabled" : "");
    $("cbLoadType").disabled = e;
    $("btnProcess").disabled = e;
    return true;
}
function selectSource(index) {
    chkSource[index].checked = true;
    return chkSource_Change();
}
function txtFile_Change() {
    return selectSource(0);
}
function txtURL_Change() {
    return selectSource(1);
}
function cleanUpAnalyzer() {
    if (analyzer) {
        analyzer.stop();
        analyzer.destroyControl();
    }
    splitter.disconnect(0);
    splitter.disconnect(1);
    if (analyzer) {
        analyzer.analyzerL.disconnect(0);
        analyzer.analyzerR.disconnect(0);
        analyzerType = null;
        analyzer = null;
    }
    merger.disconnect(0);
    return true;
}
function enableButtons(enable) {
    var e = (enable ? "" : "disabled");
    $("btnPlay").disabled = e;
    $("btnProcess").disabled = e;
    $("btnStop").disabled = e;
    chkSource[0].disabled = e;
    chkSource[1].disabled = e;
    chkSource[2].disabled = e;
    return true;
}
function showLoader(show) {
    $("imgLoader").className = (show ? "" : "HID");
    return true;
}
function createObjURL(obj, opts) {
    var url = (window.URL || window.webkitURL), objurl = (opts ? url.createObjectURL(obj, opts) : url.createObjectURL(obj));
    pendingUrls.push(objurl);
    return objurl;
}
function freeObjURLs() {
    if (pendingUrls.length) {
        var i, url = (window.URL || window.webkitURL);
        for (i = pendingUrls.length - 1; i >= 0; i--)
            url.revokeObjectURL(pendingUrls[i]);
        pendingUrls.splice(0, pendingUrls.length);
    }
    return true;
}
function stop() {
    enableButtons(true);
    if (sourceAudio) {
        sourceAudio.pause();
        sourceAudio = null;
        source.disconnect(0);
        source = null;
    } else if (source) {
        source.stop(0);
        source.disconnect(0);
        source = null;
    }
    graphicEqualizer.filter.convolver.disconnect(0);
    //Free all created URL's only at safe moments!
    freeObjURLs();
    return cleanUpAnalyzer();
}
function handleError(e) {
    showLoader(false);
    enableButtons(true);
    //Free all created URL's only at safe moments!
    freeObjURLs();
    alert(e);
    return true;
}
function updateConnections() {
    var t = $("cbAnalyzer").value;
    if (!source || ignoreNextConvolverChange) return false;
    source.disconnect(0);
    source.connect(graphicEqualizer.filter.convolver, 0, 0);
    graphicEqualizer.filter.convolver.disconnect(0);
    switch (t) {
        case "soundParticles":
        case "fft":
        case "wl":
            if (analyzerType !== t) {
                if (analyzer) cleanUpAnalyzer();
                analyzerType = t;
                switch (t) {
                    case "soundParticles":
                        analyzer = new SoundParticles(audioContext, graphicEqualizer.filter);
                        break;
                    case "fft":
                        analyzer = new Analyzer(audioContext, graphicEqualizer.filter);
                        break;
                    case "wl":
                        analyzer = new AnalyzerWL(audioContext, graphicEqualizer.filter);
                        break;
                }
                analyzer.createControl($("analyzerPlaceholder"));
            }

            graphicEqualizer.filter.convolver.connect(splitter, 0, 0);
            splitter.connect(analyzer.analyzerL, 0, 0);
            splitter.connect(analyzer.analyzerR, 1, 0);

            analyzer.analyzerL.connect(merger, 0, 0);
            analyzer.analyzerR.connect(merger, 0, 1);

            merger.connect(audioContext.destination, 0, 0);
            return analyzer.start();
        default:
            graphicEqualizer.filter.convolver.connect(audioContext.destination, 0, 0);
            return cleanUpAnalyzer();
    }
}
function filterLengthChanged() {
    graphicEqualizer.changeFilterLength(parseInt($("cbFilterLength").value));
    return true;
}
function finishLoadingIntoMemoryAndPlay(array, name, offline) {
    try {
        //Decode the array asynchronously
        audioContext.decodeAudioData(array, function (buffer) {
            try {
                if (offline) {
                    //Start processing the decoded buffer offline
                    var offlineAudioContext = (window.OfflineAudioContext ? new OfflineAudioContext(buffer.numberOfChannels, buffer.length, buffer.sampleRate) : (window.webkitOfflineAudioContext ? new webkitOfflineAudioContext(buffer.numberOfChannels, buffer.length, buffer.sampleRate) : null));
                    if (!offlineAudioContext)
                        return handleError("Offline audio processing is not supported!");
                    source = offlineAudioContext.createBufferSource();
                    source.buffer = buffer;
                    source.loop = false;
                    ignoreNextConvolverChange = true;
                    graphicEqualizer.changeAudioContext(offlineAudioContext);
                    ignoreNextConvolverChange = false;
                    source.connect(graphicEqualizer.filter.convolver, 0, 0);
                    graphicEqualizer.filter.convolver.connect(offlineAudioContext.destination, 0, 0);
                    source.start(0);
                    offlineAudioContext.oncomplete = function (renderedData) {
                        var worker = new Worker("WaveExporterWorker.js"),
                            leftBuffer = renderedData.renderedBuffer.getChannelData(0).buffer,
                            rightBuffer = ((renderedData.renderedBuffer.numberOfChannels > 1) ? renderedData.renderedBuffer.getChannelData(1).buffer : null);
                        worker.onmessage = function (e) {
                            showLoader(false);
                            enableButtons(true);
                            //Massive workaround to save the file (simulate a click on a link)!
                            //(From: http://updates.html5rocks.com/2011/08/Saving-generated-files-on-the-client-side)
                            var a = document.createElement("a"), i = name.lastIndexOf("."), evt;
                            a.href = createObjURL(new Blob(e.data, { type: "application/octet-stream" }));
                            a.download = ((i > 0) ? (name.substring(0, i) + " - (Filtered).wav") : "FilteredFile.wav");
                            //a.click(); //Works on Chrome, but not on Firefox...
                            evt = document.createEvent("MouseEvents");
                            evt.initMouseEvent("click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                            a.dispatchEvent(evt);
                            return true;
                        };
                        worker.postMessage({
                            left: leftBuffer,
                            right: rightBuffer,
                            length: renderedData.renderedBuffer.length,
                            sampleRate: (renderedData.renderedBuffer.sampleRate | 0)
                        }, [ leftBuffer, rightBuffer ]);
                        return true;
                    };
                    offlineAudioContext.startRendering();
                } else {
                    //Play the decoded buffer
                    source = audioContext.createBufferSource();
                    source.buffer = buffer;
                    source.loop = true;
                    graphicEqualizer.changeAudioContext(audioContext);
                    updateConnections();
                    source.start(0);
                    showLoader(false);
                    $("btnStop").disabled = "";
                }
            } catch (e) {
                handleError(e);
            }
            return true;
        }, function () {
            return handleError("Error decoding the file!");
        });
    } catch (e) {
        handleError(e);
    }
    return true;
}
function loadIntoMemoryAndPlay(offline) {
    var r, f, done = false;
    showLoader(true);
    if (chkSource[2].checked) {
        //Read the sample file into memory
        r = new XMLHttpRequest();
        r.open("GET", "midnightride.mp3", true);
        r.responseType = "arraybuffer";
        r.onreadystatechange = function () {
            if (r.readyState === 4 && !done) {
                done = true;
                finishLoadingIntoMemoryAndPlay(r.response, "Midnight Ride.mp3", offline);
            }
            return true;
        };
        r.send();
    } else {
        f = $("txtFile").files[0];
        //Read the chosen file into memory
        r = new FileReader();
        r.onload = function () {
            done = true;
            finishLoadingIntoMemoryAndPlay(r.result, f.name, offline);
            return true;
        };
        r.onerror = function () {
            return handleError("Error reading the file!");
        };
        r.onloadend = function () {
            if (!offline && !done)
                showLoader(false);
            return true;
        };
        r.readAsArrayBuffer(f);
    }
    return true;
}
function prepareStreamingAndPlay() {
    //Chrome now supports processing audio played over streamings (tested with Chrome v29.0.1547.76)
    if (chkSource[0].checked) {
        //If chkSource[0] is checked, create a temporary URL for the chosen file
        sourceAudio = new Audio(createObjURL($("txtFile").files[0]));
    } else if (chkSource[1].checked) {
        // sourceAudio = new Audio($("txtURL").value);
        sourceAudio = new Audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3");
    } else {
        sourceAudio = new Audio("midnightride.mp3");
    }
    sourceAudio.loop = true;
    source = audioContext.createMediaElementSource(sourceAudio);
    sourceAudio.load();
    graphicEqualizer.changeAudioContext(audioContext);
    updateConnections();
    sourceAudio.play();
    $("btnStop").disabled = "";
    return true;
}
function audioContextResumed() {
    stop();
    enableButtons(false);
    try {
        if (!chkSource[1].checked && parseInt($("cbLoadType").value))
            loadIntoMemoryAndPlay(false);
        else
            prepareStreamingAndPlay();
    } catch (e) {
        handleError(e);
    }
}
function play() {
    if (chkSource[0].checked) {
        if ($("txtFile").files.length === 0) {
            alert("Please, select a file to play!");
            return true;
        }
    } else if (chkSource[1].checked) {
        if ($("txtURL").value.length === 0) {
            alert("Please, type the address of a file to be played :(");
            return true;
        }
    }
    if (!window.AudioContext && !window.webkitAudioContext) {
        alert("Your browser does not seem to support the Web Audio API! :(");
        return true;
    }
    if (audioContext.resume)
        audioContext.resume().then(audioContextResumed);
    else
        audioContextResumed();
    return true;
}
function processAndDownload() {
    if (chkSource[0].checked) {
        if ($("txtFile").files.length === 0) {
            alert("Please, select a file to process!");
            return true;
        }
    } else if (chkSource[1].checked) {
        //We can't load an entire stream into memory... as far as we know, a few URL's
        //point to infinite streams ;)
        alert("Sorry, but that action is not available for streams :(");
        return true;
    }
    if (!window.AudioContext && !window.webkitAudioContext) {
        alert("Your browser does not seem to support the Web Audio API! :(");
        return true;
    }
    if (!window.Worker) {
        alert("Your browser does not seem to support the Web Worker API! :(");
        return true;
    }
    stop();
    enableButtons(false);
    try {
        loadIntoMemoryAndPlay(true);
    } catch (e) {
        handleError(e);
    }
    return true;
}
