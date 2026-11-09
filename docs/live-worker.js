// Runs the Exercise 2 agent (real Python) in the browser with Pyodide, off the main thread.
importScripts("https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js");

const FILES = ["config2.py", "grid_gen2.py", "agent2.py", "export_replay.py", "live.py"];
let ready = null;

function init() {
  if (!ready) ready = (async () => {
    postMessage({ type: "status", text: "Loading Python runtime (first time only)..." });
    const py = await loadPyodide();
    for (const f of FILES) {
      const res = await fetch("py/" + f);
      if (!res.ok) throw new Error("could not load py/" + f);
      py.FS.writeFile("/home/pyodide/" + f, await res.text());
    }
    py.runPython("import sys; sys.path.insert(0, '/home/pyodide')");
    return py.pyimport("live");
  })();
  return ready;
}

onmessage = async (e) => {
  const m = e.data;
  if (m.type !== "run") return;
  try {
    const live = await init();
    postMessage({ type: "status", text: "Running the agent..." });
    const json = live.run_live(m.seed, m.rows, m.cols, m.probing, m.lastLife);
    postMessage({ type: "result", json });
  } catch (err) {
    postMessage({ type: "error", message: String(err && err.message || err) });
  }
};
