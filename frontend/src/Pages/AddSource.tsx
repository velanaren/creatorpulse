import React, { useState } from "react";
import { Button } from "../components/ui/Button";
import { Dialog } from "@headlessui/react";
import { useNavigate } from "react-router-dom";

const AddSource: React.FC = () => {
  const [platform, setPlatform] = useState("RSS");
  const [topic, setTopic] = useState("");
  const [sourceUrl, setSourceUrl] = useState("");
  const [message, setMessage] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");

    try {
      const params = new URLSearchParams({
        platform,
        topic,
        source_url: sourceUrl,
      });
      const res = await fetch(`http://localhost:8000/api/feeds/sources?${params}`, {
        method: "POST",
      });
      const data = await res.json();

      if (res.ok) {
        setMessage("✅ Source added successfully!");
        setIsOpen(true);

        // Redirect to dashboard after 3 seconds
        setTimeout(() => {
          setIsOpen(false);
          navigate("/");
        }, 3000);
      } else {
        setMessage(`❌ ${data.detail || "Error adding source"}`);
      }
    } catch {
      setMessage("❌ Network error");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-md w-full max-w-md space-y-4"
      >
        <h2 className="text-2xl font-bold text-center">Add New Source</h2>

        <div>
          <label className="block text-sm mb-1">Platform</label>
          <select
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            className="w-full border rounded-lg p-2 text-sm bg-white dark:bg-gray-700"
          >
            <option value="RSS">RSS</option>
            <option value="YouTube">YouTube</option>
          </select>
        </div>

        <div>
          <label className="block text-sm mb-1">Topic</label>
          <input
            type="text"
            placeholder="e.g. Artificial Intelligence"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            required
            className="w-full border rounded-lg p-2 text-sm bg-white dark:bg-gray-700"
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Source URL or Channel ID</label>
          <input
            type="text"
            placeholder="https://rss.nytimes.com/ai.xml"
            value={sourceUrl}
            onChange={(e) => setSourceUrl(e.target.value)}
            required
            className="w-full border rounded-lg p-2 text-sm bg-white dark:bg-gray-700"
          />
        </div>

        <Button type="submit" className="w-full">
          Add Source
        </Button>

        {message && (
          <div className="text-center text-sm mt-2">
            {message}
          </div>
        )}
      </form>

      {/* ✅ Success Modal */}
      <Dialog
        open={isOpen}
        onClose={() => setIsOpen(false)}
        className="fixed inset-0 z-50 flex items-center justify-center p-4"
      >
        <Dialog.Overlay className="fixed inset-0 bg-black opacity-50" />
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 max-w-sm mx-auto text-center z-10">
          <h3 className="text-lg font-semibold mb-2 text-green-600">
            Source Added Successfully!
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            Redirecting to your dashboard...
          </p>
          <Button onClick={() => navigate("/")} className="w-full">
            Go to Dashboard
          </Button>
        </div>
      </Dialog>
    </div>
  );
};

export default AddSource;