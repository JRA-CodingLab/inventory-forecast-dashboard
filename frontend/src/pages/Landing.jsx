import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <section className="flex flex-col items-center justify-center text-center px-4 py-24 lg:py-36">
      {/* Hero badge */}
      <span className="inline-block mb-4 px-4 py-1.5 text-sm font-medium text-blue-700 dark:text-blue-300 bg-blue-100 dark:bg-blue-900/40 rounded-full">
        Smart Inventory Management
      </span>

      {/* Headline */}
      <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight max-w-3xl">
        Know Your Stock.{" "}
        <span className="text-blue-600 dark:text-blue-400">Predict Demand.</span>
      </h1>

      {/* Sub-headline */}
      <p className="mt-6 text-lg text-gray-600 dark:text-gray-400 max-w-2xl">
        Track inventory in real time, spot low-stock items instantly, and prepare
        for AI-powered demand forecasting — all in one lightweight dashboard.
      </p>

      {/* CTAs */}
      <div className="mt-10 flex flex-col sm:flex-row gap-4">
        <Link
          to="/dashboard"
          className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-lg shadow-blue-600/25 transition-all"
        >
          Open Dashboard
        </Link>
        <a
          href="https://github.com/JRA-CodingLab/inventory-forecast-dashboard"
          target="_blank"
          rel="noopener noreferrer"
          className="px-8 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-semibold rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-all"
        >
          View on GitHub
        </a>
      </div>

      {/* Feature highlights */}
      <div className="mt-20 grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-4xl w-full">
        {[
          {
            icon: "📊",
            title: "Live Metrics",
            desc: "Total products, stock value, and low-stock alerts at a glance.",
          },
          {
            icon: "🔔",
            title: "Low Stock Alerts",
            desc: "Items below threshold are flagged so you never miss a reorder.",
          },
          {
            icon: "🤖",
            title: "Forecast Ready",
            desc: "Architecture prepared for ML-driven demand prediction.",
          },
        ].map((feat) => (
          <div
            key={feat.title}
            className="p-6 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700"
          >
            <div className="text-3xl mb-3">{feat.icon}</div>
            <h3 className="font-bold text-lg mb-1">{feat.title}</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">{feat.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
