import React from "react";

function ScanProgress({ status }) {

  const stages = [
    ["upload", "Input preserved", "Original bytes are stored without executing the file."],
    ["scan", "Scan fragments", "Read each damaged fragment, hash it, and detect signatures."],
    ["match", "Map relationships", "Compare fragment boundaries and rank likely next fragments."],
    ["reconstruct", "Reconstruct", "Write the highest-confidence ordered fragment path."],
    ["integrity", "Assess integrity", "Compare size, headers, damage, and recovered hash."],
    ["report", "Explain result", "Separate verified facts from algorithmic interpretation."],
  ];
  const activeIndex = status === "completed" ? stages.length : status === "failed" ? 0 : Math.max(0, stages.findIndex(([key]) => key === status));
  const progress = status === "completed" ? 100 : Math.max(8, ((activeIndex + 1) / stages.length) * 100);

  return (
    <div className="recovery-path">
      <div className="path-heading">
        <div>
          <p className="section-label">RECOVERY PATH</p>
          <h2>From damaged bytes to verified evidence</h2>
        </div>
        <span className="path-percent">{Math.round(progress)}%</span>
      </div>
      <div className="progress"><div className="progress-bar" style={{ width: `${progress}%` }} /></div>
      <div className="path-stages">
        {stages.map(([key, title, description], index) => (
          <div className={`path-stage ${index < activeIndex || status === "completed" ? "done" : ""} ${index === activeIndex && status !== "completed" ? "active" : ""}`} key={key}>
            <span className="stage-number">{index < activeIndex || status === "completed" ? "✓" : String(index + 1).padStart(2, "0")}</span>
            <div><strong>{title}</strong><p>{description}</p></div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ScanProgress;