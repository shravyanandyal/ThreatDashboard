import { useEffect, useState } from 'react';
import axios from 'axios';

function useDebounce(value, delay) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebounced(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debounced;
}

function Threats() {
  const [threats, setThreats] = useState([]);
  const [page, setPage] = useState(1);
  const [limit] = useState(10);
  const [category, setCategory] = useState('');
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 500);
  const [total, setTotal] = useState(0);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchThreats();
  }, [page, category, debouncedSearch]);

  useEffect(() => {
    // Fetch category list once for dropdown
    axios.get('http://localhost:5050/api/threats/stats')
      .then(res => setCategories(res.data.category_counts.map(c => c._id)))
      .catch(err => console.error("Failed to load categories", err));
  }, []);

  const fetchThreats = () => {
    let url = `http://localhost:5050/api/threats?page=${page}&limit=${limit}`;
    if (category) url += `&category=${encodeURIComponent(category)}`;
    if (debouncedSearch) url += `&search=${encodeURIComponent(debouncedSearch)}`;

    axios.get(url)
      .then(res => {
        setThreats(res.data.data);
        setTotal(res.data.total);
      })
      .catch(err => console.error("Failed to fetch threats", err));
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <div>
      <h2>Threats</h2>

      <div style={{ marginBottom: '10px' }}>
        <input
          type="text"
          placeholder="Search description"
          value={search}
          onChange={e => {
            setPage(1);
            setSearch(e.target.value);
          }}
        />

        <select value={category} onChange={e => {
          setPage(1);
          setCategory(e.target.value);
        }}>
          <option value="">All Categories</option>
          {categories.map((cat, idx) => (
            <option key={idx} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      <ul>
        {threats.map(threat => (
          <li key={threat._id}>
            <strong>{threat.threat_category}</strong> —{" "}
            {threat.cleaned_description?.slice(0, 100)}...
          </li>
        ))}
      </ul>

      <div style={{ marginTop: '20px' }}>
        <button onClick={() => setPage(p => Math.max(p - 1, 1))} disabled={page === 1}>
          ⬅ Prev
        </button>
        <span style={{ margin: '0 10px' }}>Page {page} of {totalPages}</span>
        <button onClick={() => setPage(p => Math.min(p + 1, totalPages))} disabled={page === totalPages}>
          Next ➡
        </button>
      </div>
    </div>
  );
}

export default Threats;
