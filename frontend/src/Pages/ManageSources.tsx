import React, { useEffect, useState } from "react";
import { Button } from "../components/ui/Button";

interface Source {
  id: number;
  platform: string;
  topic: string;
  source_url: string;
  active: boolean;
}

const ManageSources: React.FC = () => {
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchSources = async () => {
    setLoading(true);
    const res = await fetch("http://localhost:8000/api/feeds/sources");
    const data = await res.json();
    setSources(data);
    setLoading(false);
  };

  const toggleSource = async (id: number) => {
    await fetch(`http://localhost:8000/api/feeds/source/${id}/toggle`, {
      method: "PATCH",
    });
    fetchSources();
  };

  const deleteSource = async (id: number) => {
    if (!window.confirm("Are you sure you want to delete this source?")) return;
    await fetch(`http://localhost:8000/api/feeds/source/${id}`, {
      method: "DELETE",
    });
    fetchSources();
  };

  useEffect(() => {
    fetchSources();
  }, []);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-center md:text-left">Manage Sources</h1>

            {/* 🔄 Sync Now Button */}
            <div className="flex justify-end mb-4">
        <Button
          className="bg-blue-600 hover:bg-blue-500 px-4 py-2 text-white rounded-md"
          onClick={async () => {
            try {
              const res = await fetch("http://localhost:8000/api/feeds/sync/", {
                method: "POST",
              });
              const data = await res.json();
              alert(`${data.message}: ${data.count} feeds updated.`);
            } catch (err) {
              alert("❌ Sync failed. Please check backend connection.");
              console.error(err);
            }
          }}
        >
          🔄 Sync Now
        </Button>
      </div>

      {loading ? (
        <div className="text-gray-500 text-center">Loading...</div>
      ) : sources.length === 0 ? (
        <div className="text-gray-500 text-center">No sources added yet.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {sources.map((src) => (
            <div
              key={src.id}
              className="border p-4 rounded-lg shadow-sm bg-white flex flex-col justify-between"
            >
              <div>
                <h3 className="text-lg font-semibold mb-1">{src.topic}</h3>
                <p className="text-sm text-gray-600 mb-2">{src.platform}</p>
                <a
                  href={src.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-blue-600 hover:underline break-all"
                >
                  {src.source_url}
                </a>
              </div>

              <div className="mt-4 flex justify-between items-center">
                <Button
                  className={`px-3 py-1 text-sm rounded-md ${
                    src.active
                      ? "bg-green-600 hover:bg-green-500"
                      : "bg-gray-400 hover:bg-gray-300"
                  }`}
                  onClick={() => toggleSource(src.id)}
                >
                  {src.active ? "Active" : "Inactive"}
                </Button>

                <Button
                  className="bg-red-600 hover:bg-red-500 text-sm px-3 py-1"
                  onClick={() => deleteSource(src.id)}
                >
                  Delete
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ManageSources;