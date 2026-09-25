import React from "react";

function FragmentGraph({
  fragments = []
}) {

  return (
    <div className="card">

      <h2>Fragment Relationship</h2>

      <div className="fragment-list">

        {fragments.map(
          (fragment, index) => (

            <div
              className="fragment-node"
              key={
                fragment.fragment_id ||
                index
              }
            >

              {fragment.fragment_id ||
                `Fragment ${index + 1}`}

            </div>

          )
        )}

      </div>

    </div>
  );
}

export default FragmentGraph;