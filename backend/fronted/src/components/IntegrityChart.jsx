import React, {
  PieChart,
  Pie,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function IntegrityChart({
  integrity = 0
}) {

  const data = [
    {
      name: "Integrity",
      value: integrity
    },
    {
      name: "Damage",
      value: 100 - integrity
    }
  ];

  return (
    <div className="card">

      <h2>Integrity Score</h2>

      <div
        style={{
          width: "100%",
          height: 250
        }}
      >

        <ResponsiveContainer>

          <PieChart>

            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              outerRadius={90}
              label
            />

            <Tooltip />

          </PieChart>

        </ResponsiveContainer>

      </div>

      <h3>
        {integrity}%
      </h3>

    </div>
  );
}

export default IntegrityChart;