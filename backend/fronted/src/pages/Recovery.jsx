import React, {
  useState
} from "react";

import axios from "axios";

import ScanProgress
  from "../components/ScanProgress";

const API =
  import.meta.env.VITE_API_URL ||
  "/api";

function Recovery() {

  const [status, setStatus] =
    useState("ready");

  const [scan, setScan] =
    useState(null);

  const [result, setResult] =
    useState(null);

  async function startRecovery() {

    try {

      setStatus("scan");

      const scanResponse = await axios.post(
        `${API}/scan/demo`
      );

      setScan(scanResponse.data.result);

      setStatus("match");
      setStatus("reconstruct");

      const response =
        await axios.post(
          `${API}/recover/demo`
        );

      setResult(
        response.data.result
      );

      setStatus("completed");

    } catch (error) {

      console.error(error);

      setStatus("failed");
    }
  }

  return (
    <main className="container">

      <section className="hero recovery-hero">
        <div>
          <p className="eyebrow">CONTROLLED RECONSTRUCTION / DEMO CASE</p>
          <h1>Trace the recovery<br /><em>before trusting it.</em></h1>
          <p className="hero-copy">Every result is built from observable fragment evidence, then scored with clear limitations.</p>
        </div>
        <button onClick={startRecovery} disabled={status !== "ready" && status !== "completed" && status !== "failed"}>
          {status === "completed" ? "Run again" : "Start recovery"}
        </button>
      </section>

      <ScanProgress
        status={status}
      />

      {scan && <div className="scan-fact"><strong>{scan.fragment_count}</strong><span>fragments scanned</span><strong>{scan.relationships?.length || 0}</strong><span>relationship candidates</span></div>}

      {result && (

        <div className="recovery-results">
          <div className="section-heading"><div><p className="section-label">RECOVERY OUTPUT</p><h2>What the engine could restore</h2></div><span className="analysis-status">VERIFIED RUN</span></div>
          {(result.artifacts || []).map((artifact) => (
            <article className="result-artifact" key={artifact.artifact_id}>
              <div><h3>{artifact.filename}</h3><p>{artifact.reconstruction_explanation}</p></div>
              <div className="result-metrics"><span><b>{artifact.integrity_score}%</b> integrity</span><span><b>{artifact.recovery_confidence}%</b> confidence</span><span><b>{artifact.priority}</b> priority</span></div>
              <div className="result-limit"><strong>Restored:</strong> {artifact.recovered_fragment_count} fragments. <strong>Missing:</strong> {artifact.missing_fragments?.length || 0}. <strong>Changed:</strong> {artifact.corrupted_fragments?.length || 0}. Output: {artifact.recovered_file}</div>
            </article>
          ))}
        </div>

      )}

    </main>
  );
}

export default Recovery;