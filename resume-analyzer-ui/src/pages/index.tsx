import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDesc, setJobDesc] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const analyzeResume = async () => {
    if (!file || !jobDesc) return alert("Upload a file and enter a job description.");

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDesc);

    try {
      const res = await axios.post("http://localhost:8000/analyze_resume/", formData);
      setResponse(res.data.answer);
    } catch (error) {
      alert("Something went wrong.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const compareAllCandidates = async () => {
    if (!jobDesc) return alert("Enter a job description.");

    setLoading(true);
    const descForm = new FormData();
    descForm.append("job_description", jobDesc);

    try {
      const res = await axios.post("http://localhost:8000/generate/", descForm);
      setResponse(res.data.answer);
    } catch (error) {
      alert("Comparison failed.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const saveResume = async () => {
    if (!file) return alert("Please select a resume to save.");
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/save_resume/", formData);
      alert(res.data.message);
    } catch (err) {
      alert("Failed to save resume.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };


  return (
    <main className="min-h-screen bg-white text-black flex items-center justify-center p-4">
      <div className="w-full max-w-3xl p-8 rounded shadow bg-white">
        <h1 className="text-3xl font-bold">AI Resume Analyzer</h1>

        <div className="space-y-2">
          <label className="block font-medium">Job Description:</label>
          <textarea
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            className="w-full p-2 border rounded text-black"
            rows={6}
            placeholder="Paste the job description here"
          />
        </div>

        <div className="space-y-2">
          <label className="block font-medium">Upload Resume (PDF):</label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="text-black"
          />
        </div>

        <div className="flex gap-4">
          <button
            onClick={analyzeResume}
            className="px-4 py-2 bg-blue-600 rounded"
          >
            Analyze
          </button>

          <button
            onClick={compareAllCandidates}
            className="px-4 py-2 bg-green-600 rounded"
          >
            Compare All Candidates
          </button>

          <button
            onClick={saveResume}
            className="px-4 py-2 bg-yellow-500 text-white rounded"
          >
            Save Resume for Future Reference
          </button>
        </div>

        {loading && <p>Loading..</p>}

        {response && (
          <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded mt-4">
            <h2 className="font-semibold mb-2 text-black dark:text-white">
              Gemini Summary:
            </h2>
            <p className="whitespace-pre-wrap text-black dark:text-white">{response}</p>
          </div>
        )}
      </div>
    </main>
  );
}