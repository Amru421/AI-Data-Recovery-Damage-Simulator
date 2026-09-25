import React from "react";

function ReportViewer({
  report
}) {

  if (!report) {

    return (
      <div className="card">
        <p>
          No report available.
        </p>
      </div>
    );
  }

  return (
    <div className="card">

      <h2>
        Investigation Report
      </h2>

      <p>
        {report.summary ||
          "No summary available."}
      </p>

      <h3>
        Missing Fragments
      </h3>

      <ul>

        {(report.missing_fragments ||
          []).map(
            (item, index) => (
              <li key={index}>
                {item}
              </li>
            )
          )}

      </ul>

      <h3>
        Corrupted Fragments
      </h3>

      <ul>

        {(report.corrupted_fragments ||
          []).map(
            (item, index) => (
              <li key={index}>
                {item}
              </li>
            )
          )}

      </ul>

    </div>
  );
}

export default ReportViewer;