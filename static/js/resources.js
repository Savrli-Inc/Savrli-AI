async function refreshList() {
  const res = await fetch("/api/resources/list");
  const items = await res.json();
  const ul = document.getElementById("resourceList");
  ul.innerHTML = "";
  for (const it of items) {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = `/api/resources/download/${it.id}`;
    a.textContent = it.filename;
    a.target = "_blank";
    li.appendChild(a);
    ul.appendChild(li);
  }
}

document.getElementById("uploadBtn").addEventListener("click", async () => {
  const fileInput = document.getElementById("uploadFile");
  if (!fileInput.files.length) return alert("Choose a file");
  const fd = new FormData();
  fd.append("file", fileInput.files[0]);
  const res = await fetch("/api/resources/upload", { method: "POST", body: fd });
  if (!res.ok) return alert("Upload failed");
  await refreshList();
});

document.getElementById("importBtn").addEventListener("click", async () => {
  const fileInput = document.getElementById("importFile");
  if (!fileInput.files.length) return alert("Choose a JSON file to import");
  const fd = new FormData();
  fd.append("file", fileInput.files[0]);
  const res = await fetch("/api/resources/import", { method: "POST", body: fd });
  const data = await res.json();
  alert(`Imported ${data.imported} items`);
  await refreshList();
});

document.getElementById("exportBtn").addEventListener("click", async () => {
  const res = await fetch("/api/resources/export");
  if (!res.ok) return alert("Export failed");
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "resources-index.json";
  a.click();
  URL.revokeObjectURL(url);
});

refreshList().catch(console.error);
