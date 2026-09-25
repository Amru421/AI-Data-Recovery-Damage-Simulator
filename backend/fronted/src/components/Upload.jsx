import React, { useState } from "react";
import axios from "axios";

const API =
  import.meta.env.VITE_API_URL ||
  "/api";

function Upload({ onUploaded }) {

  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("waiting");
  const [message, setMessage] = useState(
    "Recovery status: Waiting for a file."
  );

  function formatBytes(bytes) {

    if (bytes === 0) return "0 B";

    const units = ["B", "KB", "MB", "GB"];
    const index = Math.min(
      Math.floor(Math.log(bytes) / Math.log(1024)),
      units.length - 1
    );

    return `${(bytes / 1024 ** index).toFixed(index ? 1 : 0)} ${units[index]}`;
  }

  function selectFile(selectedFile) {

    if (!selectedFile) return;

    setFile(selectedFile);
    setStatus("waiting");
    setMessage(
      `Recovery status: ${selectedFile.name} is ready to upload.`
    );
  }

  function handleDrop(event) {

    event.preventDefault();
    selectFile(event.dataTransfer.files[0]);
  }

  async function uploadFile() {

    if (!file) {

      setStatus("waiting");
      setMessage(
        "Recovery status: Select a file before uploading."
      );

      return;
    }

    const formData = new FormData();

    formData.append(
      "file",
      file
    );

    try {

      setStatus("uploading");
      setMessage("Recovery status: Uploading file...");

      const response =
        await axios.post(
          `${API}/upload`,
          formData
        );

      setMessage(
        `Uploaded: ${response.data.filename}. Analysis is ready.`
      );
      setStatus("uploaded");
      onUploaded?.(response.data);

    } catch (error) {

      const detail =
        error.response?.data?.detail ||
        "The file could not be uploaded.";

      setStatus("failed");
      setMessage(
        `Recovery status: Upload failed. ${detail}`
      );
    }
  }

  return (
    <section className="upload-card">

      <div className="upload-heading">
        <div>
          <p className="upload-kicker">EVIDENCE INTAKE</p>
          <h2>Upload any file</h2>
        </div>
        <span className="upload-badge">ALL TYPES</span>
      </div>

      <label
        className={`drop-zone ${file ? "has-file" : ""}`}
        onDragOver={(event) => event.preventDefault()}
        onDrop={handleDrop}
      >
        <input
          type="file"
          onChange={(event) => selectFile(event.target.files[0])}
        />
        <span className="drop-icon">+</span>
        <strong>{file ? file.name : "Drop a file here"}</strong>
        <span>{file ? formatBytes(file.size) : "or choose from your device"}</span>
      </label>

      {file && (
        <div className="selected-file">
          <span className="file-type">FILE</span>
          <span>{file.name}</span>
          <span className="file-size">{formatBytes(file.size)}</span>
        </div>
      )}

      <button
        onClick={uploadFile}
        disabled={status === "uploading"}
        className="upload-button"
      >
        {status === "uploading" ? "Uploading..." : "Upload"}
      </button>

      <div className={`upload-status ${status}`} role="status">
        <span className="status-dot" />
        <span>{message}</span>
      </div>

    </section>
  );
}

export default Upload;