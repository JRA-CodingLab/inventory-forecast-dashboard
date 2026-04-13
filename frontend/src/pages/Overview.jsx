import { useState, useEffect } from "react";

const API_BASE = "/products/";

function MetricCard({ label, value, accent }) {
  return (
    <div className="p-5 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm">
      <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
      <p className={`text-2xl font-bold mt-1 ${accent || "text-gray-900 dark:text-white"}`}>
        {value}
      </p>
    </div>
  );
}

function StockBadge({ stock }) {
  const isLow = stock < 10;
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
        isLow
          ? "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300"
          : "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300"
      }`}
    >
      {stock}
    </span>
  );
}

export default function Overview() {
  const [products, setProducts] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchProducts() {
      try {
        const res = await fetch(`${API_BASE}?page=1&page_size=100`);
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        const data = await res.json();
        setProducts(data.items);
        setTotal(data.total);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchProducts();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-blue-500 border-t-transparent" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <p className="text-red-500 text-lg">Failed to load inventory: {error}</p>
        <p className="text-sm text-gray-500 mt-2">Make sure the backend is running on port 8000.</p>
      </div>
    );
  }

  const totalValue = products.reduce((sum, p) => sum + p.price * p.current_stock, 0);
  const lowStockCount = products.filter((p) => p.current_stock < 10).length;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold mb-6">Inventory Overview</h1>

      {/* Metric cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <MetricCard label="Total Products" value={total} />
        <MetricCard
          label="Stock Value"
          value={`$${totalValue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
          accent="text-green-600 dark:text-green-400"
        />
        <MetricCard
          label="Low Stock Items"
          value={lowStockCount}
          accent={lowStockCount > 0 ? "text-red-600 dark:text-red-400" : undefined}
        />
      </div>

      {/* Inventory table */}
      <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-800">
            <tr>
              {["ID", "Name", "Category", "Price", "Stock"].map((col) => (
                <th
                  key={col}
                  className="px-6 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-100 dark:divide-gray-800">
            {products.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-gray-400">
                  No products yet. Add some via the API.
                </td>
              </tr>
            ) : (
              products.map((p) => (
                <tr key={p.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{p.id}</td>
                  <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">{p.name}</td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{p.category}</td>
                  <td className="px-6 py-4 text-sm text-gray-700 dark:text-gray-300">
                    ${p.price.toFixed(2)}
                  </td>
                  <td className="px-6 py-4">
                    <StockBadge stock={p.current_stock} />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
