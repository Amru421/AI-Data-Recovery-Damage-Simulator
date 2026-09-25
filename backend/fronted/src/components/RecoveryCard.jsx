import React from "react";

function RecoveryCard({
  artifact
}) {

  return (
    <div className="card">

      <h2>
        {artifact?.filename ||
          "Recovered Artifact"}
      </h2>

      <p>
        File Type:
        {" "}
        {artifact?.file_type ||
          "Unknown"}
      </p>

      <p>
        Integrity:
        {" "}
        {artifact?.integrity_score ??
          0}%
      </p>

      <p>
        Missing Fragments:
        {" "}
        {artifact
          ?.missing_fragments
          ?.length || 0}
      </p>

      <p>
        Corrupted Fragments:
        {" "}
        {artifact
          ?.corrupted_fragments
          ?.length || 0}
      </p>

    </div>
  );
}

export default RecoveryCard;