import { useState } from "react";

/**
 * Diagnostic options and their required fields.
 * Modular, easy to extend.
 */
const DIAGNOSTICS = [
  {
    label: "Low Suction Pressure",
    value: "low_suction",
    fields: [
      { name: "suction_pressure", label: "Suction Pressure (psi)", default: 38 },
      { name: "superheat", label: "Superheat (F)", default: 25 },
      { name: "compressor_temp", label: "Compressor Temp (F)", default: 230 }
    ]
  },
  {
    label: "High Head Pressure",
    value: "high_head",
    fields: [
      { name: "head_pressure", label: "Head (Discharge) Pressure (psi)", default: 280 },
      { name: "ambient_temp", label: "Ambient Temp (F)", default: 85 }
    ]
  },
  {
    label: "High Superheat",
    value: "high_superheat",
    fields: [
      { name: "superheat", label: "Superheat (F)", default: 25 },
      { name: "suction_pressure", label: "Suction Pressure (psi)", default: 38 }
    ]
  },
  {
    label: "Low Subcooling",
    value: "low_subcooling",
    fields: [
      { name: "subcooling", label: "Subcooling (F)", default: 3 }
    ]
  }
];

export default function Home() {
  const [diagType, setDiagType] = useState(DIAGNOSTICS[0].value);
  const [inputs, setInputs] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Get the fields for the selected diagnostic
  const fields = DIAGNOSTICS.find(d => d.value === diagType).fields;

  // Handle input changes
  const handleInput = (name, value) => {
    setInputs({ ...inputs, [name]: value });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    // Call the FastAPI backend
    const res = await fetch("/api/diagnose", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: diagType, inputs })
    });
    setResult(await res.json());
    setLoading(false);
  };

  return (
    <main style={{
      maxWidth: 600,
      margin: "2rem auto",
      fontFamily: "sans-serif",
      background: "#fff",
      borderRadius: 8,
      boxShadow: "0 2px 8px #eee",
      padding: 24
    }}>
      <h1 style={{ textAlign: "center", marginBottom: 24 }}>
        Supermarket Refrigeration Diagnostics
      </h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
        <label>
          <b>Diagnostic Type:</b>
          <select
            value={diagType}
            onChange={e => { setDiagType(e.target.value); setInputs({}); }}
            style={{ marginLeft: 8, marginBottom: 16 }}
          >
            {DIAGNOSTICS.map(d => (
              <option key={d.value} value={d.value}>{d.label}</option>
            ))}
          </select>
        </label>
        <div style={{ marginTop: 16 }}>
          {fields.map(f => (
            <div key={f.name} style={{ marginBottom: 12 }}>
              <label>
                {f.label}:{" "}
                <input
                  type="number"
                  defaultValue={f.default}
                  onChange={e => handleInput(f.name, parseFloat(e.target.value))}
                  style={{ width: 120, padding: 4, borderRadius: 4, border: "1px solid #ccc" }}
                  required
                />
              </label>
            </div>
          ))}
        </div>
        <button
          type="submit"
          disabled={loading}
          style={{
            marginTop: 16,
            padding: "8px 24px",
            borderRadius: 4,
            border: "none",
            background: "#2563eb",
            color: "#fff",
            fontWeight: "bold",
            cursor: "pointer"
          }}
        >
          {loading ? "Diagnosing..." : "Get Diagnosis"}
        </button>
      </form>
      {result && (
        <div style={{
          background: "#f9f9f9",
          padding: 20,
          borderRadius: 8,
          border: "1px solid #eee"
        }}>
          <h2>Diagnosis Result</h2>
          <p><b>Diagnosis:</b> {result.diagnosis}</p>
          <p><b>Confidence:</b> {result.confidence}</p>
          <p><b>Next Steps:</b> {result.next_steps && result.next_steps.join(", ")}</p>
          {result.safety_warnings && result.safety_warnings.length > 0 && (
            <p style={{ color: "red" }}><b>Safety Warnings:</b> {result.safety_warnings.join(", ")}</p>
          )}
          <p><b>Manual Reference:</b> {result.manual_reference}</p>
          <h3>LLM Summary</h3>
          <pre style={{ whiteSpace: "pre-wrap" }}>{result.llm_summary}</pre>
          <h3>Manual Chunks</h3>
          <ul>
            {result.manual_chunks && result.manual_chunks.map((c, i) => (
              <li key={i}><small>{c.content.slice(0, 120)}...</small></li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
} 