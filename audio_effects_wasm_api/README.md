This folder contains a crate that allow the usage of the audio_effects crate trough web assembly.
It's built for usage inside the inoft_vocal_engine. 

You are free the code of the wasm_api under the MIT license, but no support will be offered towards the usage
of the wasm_api. Strictly no notice before implementations of potential breaking changes will be given regarding the
audio effects wasm_api. Use it at your own risks.

Build instructions :

```
cd .../inoft_vocal_framework/audio_effects_wasm_api
wasm-pack build --target bundler
```

The first time on a new system :
```
cd .../inoft_vocal_framework/audio_effects_wasm_api/pkg
npm link
```

After compiling the audio_effects_wasm_api, the editor or audio_editor needs to be compiled again
```
cd .../inoft_vocal_engine/web_interface
npm run build:dev:editor
```
or 
```
cd .../inoft_vocal_engine/web_interface
npm run build:dev:audio-editor
```


In depth Rust to WASM step-by-step tutorial : https://developer.mozilla.org/en-US/docs/WebAssembly/Rust_to_wasm