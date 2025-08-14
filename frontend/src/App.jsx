import React, { useEffect, useMemo, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import "./App.css";

// THIS IS THE CORRECTED FUNCTION
const fetcher = async (path) => {
  // We are now hardcoding the correct backend URL to guarantee it works.
  const baseUrl = "https://emergent-labs-va.onrender.com";
  const url = `${baseUrl}${path}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
};

const Section = ({ children }) => (
  <div className="p-4 md:p-6 space-y-6">
    {children}
  </div>
);

function Dashboard() {
  const [kpis, setKpis] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetcher("/api/kpis").then(setKpis).catch(setError);
  }, []);

  if (error) return <div className="text-red-600">Failed to load KPIs</div>;
  if (!kpis) return <div className="text-gray-500">Loading...</div>;

  const warmPalette = ["#4CAF50", "#8BC34A", "#A5D6A7", "#C8E6C9"]; // sector palette
  const sentimentPalette = ["#4CAF50", "#9E9E9E", "#B71C1C"]; // positive, neutral, negative

  const sentimentData = [
    { name: "Positive", value: kpis.sentiment.positive },
    { name: "Neutral", value: kpis.sentiment.neutral },
    { name: "Negative", value: kpis.sentiment.negative },
  ];

  return (
    <Section>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <div className="kpi-number">{kpis.callVolume}</div>
          <div className="kpi-label">Monthly Call Volume</div>
        </div>
        <div className="card">
          <div className="kpi-number">{Math.round(kpis.resolutionRate * 100)}%</div>
          <div className="kpi-label">Resolution Rate</div>
        </div>
        <div className="card">
          <div className="kpi-number">{Math.round(kpis.sentiment.positive * 100)}%</div>
          <div className="kpi-label">Positive Sentiment</div>
        </div>
        <div className="card">
          <div className="kpi-number">{kpis.jobTypeDistribution.reduce((a, b) => a + b.count, 0)}</div>
          <div className="kpi-label">Jobs Categorized</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="card lg:col-span-2">
          <div className="font-semibold mb-2">Weekly Call Trend</div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={kpis.trend} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <XAxis dataKey="day" stroke="#9E9E9E" />
                <YAxis stroke="#9E9E9E" />
                <Tooltip />
                <Line type="monotone" dataKey="calls" stroke="#4CAF50" strokeWidth={3} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="card">
          <div className="font-semibold mb-2">Sentiment Breakdown</div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={sentimentData} innerRadius={50} outerRadius={70} paddingAngle={4} dataKey="value">
                  {sentimentData.map((entry, i) => (
                    <Cell key={`cell-${i}`} fill={sentimentPalette[i]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="font-semibold mb-2">Job Type Distribution</div>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={kpis.jobTypeDistribution}>
              <XAxis dataKey="type" stroke="#9E9E9E"/>
              <YAxis stroke="#9E9E9E"/>
              <Tooltip />
              <Bar dataKey="count" radius={[8, 8, 0, 0]}>
                {kpis.jobTypeDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={warmPalette[index % warmPalette.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </Section>
  );
}

function CallRecords() {
  const [records, setRecords] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetcher("/api/calls").then((d) => setRecords(d.items)).catch(setError);
  }, []);

  if (error) return <div className="text-red-600">Failed to load calls</div>;

  return (
    <Section>
      <div className="card overflow-x-auto">
        <table className="min-w-full">
          <thead>
            <tr className="text-left text-gray-500">
              <th className="p-3">Caller Name</th>
              <th className="p-3">Call Type</th>
              <th className="p-3">Date/Time</th>
              <th className="p-3">Sentiment</th>
              <th className="p-3">Resolution Status</th>
            </tr>
          </thead>
          <tbody>
            {records.map((r) => (
              <tr key={r.id} className="table-row">
                <td className="p-3 text-textblack">{r.callerName}</td>
                <td className="p-3">{r.callType}</td>
                <td className="p-3">{new Date(r.datetime).toLocaleString()}</td>
                <td className="p-3">
                  <span className="badge-green capitalize">{r.sentiment}</span>
                </td>
                <td className="p-3">{r.resolutionStatus}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Section>
  );
}

function ServiceInsights() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetcher("/api/service-insights").then(setData).catch(setError);
  }, []);

  if (error) return <div className="text-red-600">Failed to load service insights</div>;
  if (!data) return <div className="text-gray-500">Loading...</div>;

  return (
    <Section>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {data.categories.map((c) => (
          <div key={c.name} className="card">
            <div className="font-semibold text-textblack">{c.name}</div>
            <div className="mt-2 text-sm text-gray-500">Cases</div>
            <div className="kpi-number">{c.count}</div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
              <div className="p-3 bg-warmgreen/5 rounded-xl">
                <div className="text-gray-600">Avg Handle</div>
                <div className="font-semibold text-textblack">{c.avgHandleTime} min</div>
              </div>
              <div className="p-3 bg-warmgreen/5 rounded-xl">
                <div className="text-gray-600">FCR</div>
                <div className="font-semibold text-textblack">{Math.round(c.firstCallResolution * 100)}%</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Section>
  );
}

function PostCallSummaries() {
  const [summaries, setSummaries] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetcher("/api/summaries").then((d) => setSummaries(d.items)).catch(setError);
  }, []);

  if (error) return <div className="text-red-600">Failed to load summaries</div>;

  return (
    <Section>
      <div className="space-y-4 max-h-[70vh] overflow-auto pr-2">
        {summaries.map((s) => (
          <div key={s.id} className="card">
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="font-semibold text-textblack">{s.caller}</div>
                <div className="text-sm text-gray-600 mt-1">{s.transcriptPreview}</div>
              </div>
              <div className="flex gap-2">
                <button className="tab bg-warmgreen text-white tab-active">Assign</button>
                <button className="tab">Follow-up</button>
              </div>
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              {s.actionItems.map((a) => (
                <span key={a} className="badge-green bg-warmgreen/10 text-textblack border border-warmgreen/30">
                  {a}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </Section>
  );
}

function Integrations() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetcher("/api/integrations").then((d) => setItems(d.items)).catch(setError);
  }, []);

  if (error) return <div className="text-red-600">Failed to load integrations</div>;

  return (
    <Section>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {items.map((i, idx) => (
          <div key={idx} className="card flex items-center justify-between">
            <div className="font-semibold text-textblack">{i.name}</div>
            <Toggle enabled={i.enabled} onChange={(v) => {
              setItems((prev) => prev.map((p, pi) => pi === idx ? { ...p, enabled: v } : p));
            }} />
          </div>
        ))}
      </div>
    </Section>
  );
}

function Toggle({ enabled, onChange }) {
  return (
    <button
      role="switch"
      aria-checked={enabled}
      className={`toggle ${enabled ? "toggle-on" : "toggle-off"}`}
      onClick={() => onChange(!enabled)}
    >
      <span className={`toggle-dot ${enabled ? "translate-x-6" : "translate-x-1"}`}></span>
    </button>
  );
}

function Settings() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetcher("/api/settings").then(setData).catch(setError);
  }, []);

  if (error) return <div className="text-red-600">Failed to load settings</div>;
  if (!data) return <div className="text-gray-500">Loading...</div>;

  const Card = ({ title, children }) => (
    <div className="card">
      <div className="font-semibold mb-2 text-textblack">{title}</div>
      {children}
    </div>
  );

  return (
    <Section>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card title="Security">
          <div className="text-sm text-gray-600 space-y-2">
            <div>MFA: <span className="font-semibold text-textblack">{data.security.mfa ? "Enabled" : "Disabled"}</span></div>
            <div>SSO: <span className="font-semibold text-textblack">{data.security.sso ? "Enabled" : "Disabled"}</span></div>
            <div>IP Allowlist: <span className="font-semibold text-textblack">{data.security.ipAllowlist ? "On" : "Off"}</span></div>
          </div>
        </Card>
        <Card title="Data Retention">
          <div className="text-sm text-gray-600 space-y-2">
            <div>Transcripts: <span className="font-semibold text-textblack">{data.dataRetention.transcriptsDays} days</span></div>
            <div>Analytics: <span className="font-semibold text-textblack">{data.dataRetention.analyticsMonths} months</span></div>
          </div>
        </Card>
        <Card title="Access Controls">
          <div className="text-sm text-gray-600 space-y-2">
            <div>Roles: <span className="font-semibold text-textblack">{data.accessControls.roles.join(', ')}</span></div>
            <div>Default Role: <span className="font-semibold text-textblack">{data.accessControls.defaultRole}</span></div>
          </div>
        </Card>
      </div>
    </Section>
  );
}

export default function App() {
  const tabs = [
    "Dashboard",
    "Call Records",
    "Service Insights",
    "Post-Call Summaries",
    "Integrations & Workflows",
    "Settings & Compliance",
  ];
  const [active, setActive] = useState(tabs[0]);

  const render = () => {
    switch (active) {
      case "Dashboard":
        return <Dashboard />;
      case "Call Records":
        return <CallRecords />;
      case "Service Insights":
        return <ServiceInsights />;
      case "Post-Call Summaries":
        return <PostCallSummaries />;
      case "Integrations & Workflows":
        return <Integrations />;
      case "Settings & Compliance":
        return <Settings />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <header className="sticky top-0 z-10 bg-white/70 backdrop-blur border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-xl bg-warmgreen shadow-card" />
            <div className="font-bold text-textblack">Voice Agenda</div>
          </div>
          <div className="hidden md:flex gap-2">
            {tabs.map((t) => (
              <button
                key={t}
                onClick={() => setActive(t)}
                className={`tab ${active === t ? "tab-active" : ""}`}
              >
                {t}
              </button>
            ))}
          </div>
          <div className="md:hidden">
            <select value={active} onChange={(e) => setActive(e.target.value)} className="tab">
              {tabs.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto">
        {render()}
      </main>

      <footer className="py-6 text-center text-sm text-gray-400">© {new Date().getFullYear()} Voice Agenda</footer>
    </div>
  );
}
