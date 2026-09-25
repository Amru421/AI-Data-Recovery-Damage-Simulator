import React, {
  useEffect,
  useState
} from "react";

import {
  useParams
} from "react-router-dom";

import axios from "axios";

import RecoveryCard
  from "../components/RecoveryCard";

import ReportViewer
  from "../components/ReportViewer";

const API =
  import.meta.env.VITE_API_URL ||
  "/api";

function Artifact() {

  const { id } = useParams();

  const [artifact, setArtifact] =
    useState(null);

  const [report, setReport] =
    useState(null);

  useEffect(() => {

    loadData();

  }, [id]);

  async function loadData() {

    try {

      const artifactResponse =
        await axios.get(
          `${API}/artifact/${id}`
        );

      const reportResponse =
        await axios.get(
          `${API}/report/${id}`
        );

      setArtifact(
        artifactResponse.data.artifact
      );

      setReport(
        reportResponse.data.report
      );

    } catch (error) {

      console.error(error);
    }
  }

  return (
    <main className="container">

      <h1>
        Artifact Investigation
      </h1>

      <RecoveryCard
        artifact={artifact}
      />

      <ReportViewer
        report={report}
      />

    </main>
  );
}

export default Artifact;