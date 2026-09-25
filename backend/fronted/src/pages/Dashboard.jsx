import React, { useEffect, useState } from "react";
import axios from "axios";

import Upload from "../components/Upload";
import ArtifactTable from "../components/ArtifactTable";

const API =
  import.meta.env.VITE_API_URL ||
  "/api";

function Dashboard() {

  const [artifacts, setArtifacts] =
    useState([]);

  const [uploadedFile, setUploadedFile] =
    useState(null);

  useEffect(() => {

    loadArtifacts();

  }, []);

  async function loadArtifacts() {

    try {

      const [artifactResponse, uploadResponse] = await Promise.all([
        axios.get(`${API}/artifacts/demo`),
        axios.get(`${API}/uploads`),
      ]);

      const knownArtifacts = artifactResponse.data.artifacts || [];
      const uploadedArtifacts = (uploadResponse.data.uploads || []).map((upload) => {
        const analysis = upload.analysis || {};
        return {
          artifact_id: upload.file_id,
          filename: upload.filename,
          file_type: analysis.classification || upload.content_type || "Unknown",
          total_fragments: analysis.fragment_count || 0,
          missing_fragments: [],
          corrupted_fragments: [],
          recovery_confidence: analysis.recovery_confidence,
          integrity_score: analysis.integrity_score,
          uploaded_at: upload.uploaded_at,
          source: "uploaded",
        };
      });

      const combined = [...knownArtifacts, ...uploadedArtifacts];
      setArtifacts(Array.from(new Map(combined.map((artifact) => [artifact.artifact_id, artifact])).values()));

    } catch (error) {

      console.error(error);
    }
  }

  return (
    <main className="container">

      <section className="hero">
        <div>
          <p className="eyebrow">CASE OVERVIEW / LIVE WORKSPACE</p>
          <h1>Make damaged data<br /><em>legible again.</em></h1>
          <p className="hero-copy">RecoverX maps fragments, tests their integrity, and explains what can realistically be restored.</p>
        </div>
        <div className="hero-note">
          <span className="note-line" />
          <span>Analyst mode<br /><strong>Explainable recovery</strong></span>
        </div>
      </section>

      <div className="stats">

        <div className="stat-card stat-accent">
          <span>Recovered artifacts</span>
          <strong>
            {artifacts.length}
          </strong>
        </div>

        <div className="stat-card">
          <span>Recovery engine</span>
          <strong className="text-green">ACTIVE</strong>
        </div>

        <div className="stat-card">
          <span>Analysis layer</span>
          <strong>AI + rules</strong>
        </div>

      </div>

      <Upload
        onUploaded={setUploadedFile}
      />

      {uploadedFile && (
        <section className="analysis-card">
          <div className="analysis-heading">
            <div>
              <p className="upload-kicker">LATEST ANALYSIS</p>
              <h2>{uploadedFile.filename}</h2>
            </div>
            <span className="analysis-status">UPLOADED</span>
          </div>

          <div className="analysis-grid">
            <div>
              <span>Storage</span>
              <strong>Saved</strong>
            </div>
            <div>
              <span>File type</span>
              <strong>{uploadedFile.analysis?.classification || "Unknown"}</strong>
            </div>
            <div>
              <span>Integrity</span>
              <strong>{uploadedFile.analysis?.integrity_score}%</strong>
            </div>
            <div>
              <span>Fragments</span>
              <strong>{uploadedFile.analysis?.fragment_count}</strong>
            </div>
            <div>
              <span>Confidence</span>
              <strong>{uploadedFile.analysis?.recovery_confidence}%</strong>
            </div>
            <div>
              <span>Priority</span>
              <strong>{uploadedFile.analysis?.priority}</strong>
            </div>
            <div>
              <span>Recoverability</span>
              <strong>{uploadedFile.analysis?.recoverability}</strong>
            </div>
          </div>

          <div className="recovery-explainer">
            <div>
              <span className="section-label">RECOVERY STATUS</span>
              <strong>{uploadedFile.analysis?.recovery_status}</strong>
              <p>{uploadedFile.analysis?.recovery_method}</p>
            </div>
            <div>
              <span className="section-label">WHAT CAN BE RECOVERED</span>
              <ul>
                {(uploadedFile.analysis?.recoverable_items || []).map((item) => <li key={item}>{item}</li>)}
              </ul>
            </div>
          </div>
        </section>
      )}

      <ArtifactTable
        artifacts={artifacts}
      />

    </main>
  );
}

export default Dashboard;