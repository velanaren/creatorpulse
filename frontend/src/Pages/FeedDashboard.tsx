import React, { useEffect, useState } from "react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { MoonIcon, SunIcon, MagnifyingGlassIcon, ArrowPathIcon } from "@heroicons/react/24/outline";

interface FeedItem {
  id: number;
  source: string;
  title: string;
  link: string;
  summary?: string;
  published_at: string;
  topic?: string;
}

const FeedDashboard: React.FC = () => {
  const [feeds, setFeeds] = useState<FeedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [platform, setPlatform] = useState("");
  const [topic, setTopic] = useState("");
  const [query, setQuery] = useState("");
  const [dark, setDark] = useState(false);

  const fetchFeeds = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (platform) params.append("platform", platform);
    if (topic) params.append("topic", topic);
    if (query) params.append("q", query);

    const res = await fetch(`http://localhost:8000/api/feeds?${params}`);
    const data = await res.json();
    setFeeds(Array.isArray(data) ? data : []);
    setLoading(false);
  };

  useEffect(() => {
    fetchFeeds();
  }, [platform, topic]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchFeeds();
  };

  return (
    <div className={dark ? "dark bg-gray-950 text-white min-h-screen" : "bg-gray-50 min-h-screen"}>
      {/* 🔹 Top Navbar */}
      <header className="sticky top-0 z-20 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-4 py-3 flex items-center justify-between shadow-sm">
        <h1 className="text-2xl font-bold">CreatorPulse</h1>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="flex items-center space-x-2 w-full max-w-md ml-4">
          <input
            type="text"
            placeholder="Search feeds..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <Button type="submit" className="flex items-center space-x-1">
            <MagnifyingGlassIcon className="h-4 w-4" />
            <span>Search</span>
          </Button>
        </form>

        {/* Dark mode + Refresh */}
        <div className="flex items-center space-x-2 ml-4">
          <Button onClick={() => fetchFeeds()} className="flex items-center space-x-1 bg-green-600 hover:bg-green-700">
            <ArrowPathIcon className="h-4 w-4" />
            <span>Refresh</span>
          </Button>
          <Button
            onClick={() => setDark(!dark)}
            className="bg-gray-700 hover:bg-gray-600 px-3"
          >
            {dark ? <SunIcon className="h-5 w-5" /> : <MoonIcon className="h-5 w-5" />}
          </Button>
        </div>
      </header>

      {/* 🔹 Filter Section */}
      <section className="flex flex-wrap items-center justify-center md:justify-start gap-4 px-6 py-4 bg-gray-100 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
        <div>
          <label className="block text-xs text-gray-600 dark:text-gray-400">Platform</label>
          <select
            className="border rounded-lg p-2 text-sm bg-white dark:bg-gray-800"
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
          >
            <option value="">All</option>
            <option value="RSS">RSS</option>
            <option value="YouTube">YouTube</option>
          </select>
        </div>

        <div>
          <label className="block text-xs text-gray-600 dark:text-gray-400">Topic</label>
          <select
            className="border rounded-lg p-2 text-sm bg-white dark:bg-gray-800"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          >
            <option value="">All</option>
            <option value="AI">AI</option>
            <option value="Technology">Technology</option>
            <option value="Business">Business</option>
            <option value="Science">Science</option>
          </select>
        </div>
      </section>

      {/* 🔹 Main Feed Grid */}
      <main className="p-6">
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
            {[...Array(6)].map((_, i) => (
              <div
                key={i}
                className="rounded-2xl bg-gray-200 dark:bg-gray-800 h-48 shadow-sm"
              ></div>
            ))}
          </div>
        ) : feeds.length === 0 ? (
          <div className="text-center text-gray-500 mt-10">No feeds found.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {feeds.map((feed) => (
              <Card key={feed.id}>
                <div className="flex justify-between items-center mb-2">
                  <span
                    className={`text-xs font-semibold px-2 py-1 rounded-full ${
                      feed.source === "YouTube"
                        ? "bg-red-100 text-red-600"
                        : "bg-blue-100 text-blue-600"
                    }`}
                  >
                    {feed.source}
                  </span>
                  <span className="text-xs text-gray-400 dark:text-gray-500">
                    {feed.topic || "General"}
                  </span>
                </div>

                <a
                  href={feed.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block text-lg font-semibold text-blue-600 dark:text-blue-400 hover:underline mb-2 line-clamp-2"
                >
                  {feed.title}
                </a>

                <p className="text-sm text-gray-700 dark:text-gray-300 mb-3 line-clamp-3 leading-relaxed">
                  {feed.summary?.slice(0, 200) || "No summary available..."}
                </p>

                <div className="text-xs text-gray-500">
                  {new Date(feed.published_at).toLocaleString()}
                </div>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default FeedDashboard;