import React from "react";

function ArtifactTable({
  artifacts = []
}) {

  return (
    <div className="card">

      <div className="section-heading">
        <div>
          <p className="section-label">CASE HISTORY</p>
          <h2>Recovered artifacts</h2>
        </div>
        <span className="table-meta">{artifacts.length} cases tracked</span>
      </div>

      <table>

        <thead>

          <tr>
            <th>Filename</th>
            <th>Type</th>
            <th>Fragments</th>
            <th>Missing</th>
            <th>Corrupted</th>
            <th>Confidence</th>
          </tr>

        </thead>

        <tbody>

          {artifacts.map(
            (artifact) => (

              <tr
                key={
                  artifact.artifact_id
                }
              >

                <td>
                  {artifact.filename}
                </td>

                <td>
                  {artifact.file_type}
                </td>

                <td>
                  {artifact.total_fragments}
                </td>

                <td>
                  {
                    artifact
                      .missing_fragments
                      ?.length || 0
                  }
                </td>

                <td>
                  {
                    artifact
                      .corrupted_fragments
                      ?.length || 0
                  }
                </td>

                <td>
                  <span className="confidence-pill">{artifact.recovery_confidence ?? "—"}%</span>
                </td>

              </tr>

            )
          )}

        </tbody>

      </table>

    </div>
  );
}

export default ArtifactTable;